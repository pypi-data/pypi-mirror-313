use std::{
    borrow::Cow,
    fmt,
    hash::{Hash, Hasher},
    ops::ControlFlow,
};

use evalexpr::{
    Context, ContextWithMutableFunctions, ContextWithMutableVariables, DefaultNumericTypes,
    EvalexprError, Function, HashMapContext, Node, Value,
};
use nonempty::NonEmpty;
use serde_json::Value as JsonValue;
use thiserror::Error;

mod config;
pub(super) use config::ParameterSeed;

#[derive(Debug, Clone)]
pub enum Parameter {
    IntValue { value: i64 },
    IntRange { min: i64, max: i64 },
    IntSet { values: NonEmpty<i64> },
    FloatValue { value: f64 },
    FloatSet { values: NonEmpty<f64> },
    StrValue { value: String },
    StrSet { values: NonEmpty<String> },
    JsonValue { value: JsonValue },
    JsonSet { values: NonEmpty<JsonValue> },
    Expr { ty: Type, expr: Node },
}

impl Parameter {
    #[must_use]
    pub const fn cyclic_iter(&self) -> ParameterIterator {
        match self {
            Self::IntValue { value } => ParameterIterator::IntValue { value: *value },
            Self::IntRange { min, max } => ParameterIterator::IntRange {
                min: *min,
                max: *max,
                value: *min,
            },
            Self::IntSet { values } => ParameterIterator::IntSet { values, index: 0 },
            Self::FloatValue { value } => ParameterIterator::FloatValue { value: *value },
            Self::FloatSet { values } => ParameterIterator::FloatSet { values, index: 0 },
            Self::StrValue { value } => ParameterIterator::StrValue { value },
            Self::StrSet { values } => ParameterIterator::StrSet { values, index: 0 },
            Self::JsonValue { value } => ParameterIterator::JsonValue { value },
            Self::JsonSet { values } => ParameterIterator::JsonSet { values, index: 0 },
            Self::Expr { ty, expr } => ParameterIterator::Expr { ty: *ty, expr },
        }
    }

    pub fn minimise(&mut self) {
        match self {
            Self::IntValue { .. }
            | Self::FloatValue { .. }
            | Self::StrValue { .. }
            | Self::JsonValue { .. }
            | Self::Expr { .. } => (),
            Self::IntRange { min, .. } => *self = Self::IntValue { value: *min },
            Self::IntSet { values } => *self = Self::IntValue { value: values.head },
            Self::FloatSet { values } => *self = Self::FloatValue { value: values.head },
            Self::StrSet { values } => {
                *self = Self::StrValue {
                    value: values.head.clone(),
                }
            },
            Self::JsonSet { values } => {
                *self = Self::JsonValue {
                    value: values.head.clone(),
                }
            },
        }
    }

    pub fn example(
        &self,
        codec: &str,
        parameter: &str,
        eval_context: &ParameterEvalContext,
    ) -> Result<ConcreteParameter, ParameterEvalError> {
        match self {
            Self::IntValue { value } => Ok(ConcreteParameter::Int { value: *value }),
            Self::IntRange { min, .. } => Ok(ConcreteParameter::Int { value: *min }),
            Self::IntSet { values } => Ok(ConcreteParameter::Int { value: values.head }),
            Self::FloatValue { value } => Ok(ConcreteParameter::Float { value: *value }),
            Self::FloatSet { values } => Ok(ConcreteParameter::Float { value: values.head }),
            Self::StrValue { value } => Ok(ConcreteParameter::Str {
                value: Cow::Borrowed(value),
            }),
            Self::StrSet { values } => Ok(ConcreteParameter::Str {
                value: Cow::Borrowed(&values.head),
            }),
            Self::JsonValue { value } => Ok(ConcreteParameter::Json {
                value: Cow::Borrowed(value),
            }),
            Self::JsonSet { values } => Ok(ConcreteParameter::Json {
                value: Cow::Borrowed(&values.head),
            }),
            Self::Expr { ty, expr } => match *ty {
                Type::Int => expr
                    .eval_int_with_context(eval_context)
                    .map(|value| ConcreteParameter::Int { value }),
                Type::Float => expr
                    .eval_float_with_context(eval_context)
                    .map(|value| ConcreteParameter::Float { value }),
                Type::Str => expr.eval_string_with_context(eval_context).map(|value| {
                    ConcreteParameter::Str {
                        value: Cow::Owned(value),
                    }
                }),
                Type::Json => {
                    return Err(ParameterEvalErrorInner::EvalJsonValue {
                        codec: String::from(codec),
                        parameter: String::from(parameter),
                    }
                    .into())
                },
            }
            .map_err(|source| {
                ParameterEvalErrorInner::Evaluate {
                    source,
                    codec: String::from(codec),
                    parameter: String::from(parameter),
                }
                .into()
            }),
        }
    }
}

impl fmt::Display for Parameter {
    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Self::IntValue { value } => value.fmt(fmt),
            Self::IntRange { min, max } => fmt.write_fmt(format_args!("{min}..={max}")),
            Self::IntSet { values } => fmt.debug_set().entries(values.iter()).finish(),
            Self::FloatValue { value } => value.fmt(fmt),
            Self::FloatSet { values } => fmt.debug_set().entries(values.iter()).finish(),
            Self::StrValue { value } => fmt.write_fmt(format_args!("{value:?}")),
            Self::StrSet { values } => fmt.debug_set().entries(values.iter()).finish(),
            Self::JsonValue { value } => fmt.write_fmt(format_args!("{:?}", format!("{value}"))),
            Self::JsonSet { values } => fmt
                .debug_set()
                .entries(values.iter().map(|value| format!("{value}")))
                .finish(),
            Self::Expr { ty: _, expr } => fmt.write_fmt(format_args!("{expr}")),
        }
    }
}

pub enum ParameterIterator<'a> {
    IntValue {
        value: i64,
    },
    IntRange {
        min: i64,
        max: i64,
        value: i64,
    },
    IntSet {
        values: &'a NonEmpty<i64>,
        index: usize,
    },
    FloatValue {
        value: f64,
    },
    FloatSet {
        values: &'a NonEmpty<f64>,
        index: usize,
    },
    StrValue {
        value: &'a String,
    },
    StrSet {
        values: &'a NonEmpty<String>,
        index: usize,
    },
    JsonValue {
        value: &'a JsonValue,
    },
    JsonSet {
        values: &'a NonEmpty<JsonValue>,
        index: usize,
    },
    Expr {
        ty: Type,
        expr: &'a Node,
    },
}

impl<'a> ParameterIterator<'a> {
    #[expect(clippy::too_many_lines)]
    pub fn next(
        &mut self,
        codec: &str,
        name: &str,
        eval_context: &ParameterEvalContext,
    ) -> Result<ControlFlow<ConcreteParameter<'a>, ConcreteParameter<'a>>, ParameterEvalError> {
        match self {
            Self::IntValue { ref value } => {
                Ok(ControlFlow::Break(ConcreteParameter::Int { value: *value }))
            },
            Self::IntRange {
                ref min,
                ref max,
                value,
            } => {
                let old_value = *value;
                if old_value < *max {
                    *value += 1;
                    Ok(ControlFlow::Continue(ConcreteParameter::Int {
                        value: old_value,
                    }))
                } else {
                    *value = *min;
                    Ok(ControlFlow::Break(ConcreteParameter::Int {
                        value: old_value,
                    }))
                }
            },
            Self::IntSet { values, index } => {
                let old_value = values.get(*index).copied().unwrap_or(values.head);
                if *index + 1 < values.len() {
                    *index += 1;
                    Ok(ControlFlow::Continue(ConcreteParameter::Int {
                        value: old_value,
                    }))
                } else {
                    *index = 0;
                    Ok(ControlFlow::Break(ConcreteParameter::Int {
                        value: old_value,
                    }))
                }
            },
            Self::FloatValue { ref value } => Ok(ControlFlow::Break(ConcreteParameter::Float {
                value: *value,
            })),
            Self::FloatSet { values, index } => {
                let old_value = values.get(*index).copied().unwrap_or(values.head);
                if *index + 1 < values.len() {
                    *index += 1;
                    Ok(ControlFlow::Continue(ConcreteParameter::Float {
                        value: old_value,
                    }))
                } else {
                    *index = 0;
                    Ok(ControlFlow::Break(ConcreteParameter::Float {
                        value: old_value,
                    }))
                }
            },
            Self::StrValue { value } => Ok(ControlFlow::Break(ConcreteParameter::Str {
                value: Cow::Borrowed(value),
            })),
            Self::StrSet { values, index } => {
                let old_value = values.get(*index).unwrap_or(&values.head);
                if *index + 1 < values.len() {
                    *index += 1;
                    Ok(ControlFlow::Continue(ConcreteParameter::Str {
                        value: Cow::Borrowed(old_value),
                    }))
                } else {
                    *index = 0;
                    Ok(ControlFlow::Break(ConcreteParameter::Str {
                        value: Cow::Borrowed(old_value),
                    }))
                }
            },
            Self::JsonValue { value } => Ok(ControlFlow::Break(ConcreteParameter::Json {
                value: Cow::Borrowed(value),
            })),
            Self::JsonSet { values, index } => {
                let old_value = values.get(*index).unwrap_or(&values.head);
                if *index + 1 < values.len() {
                    *index += 1;
                    Ok(ControlFlow::Continue(ConcreteParameter::Json {
                        value: Cow::Borrowed(old_value),
                    }))
                } else {
                    *index = 0;
                    Ok(ControlFlow::Break(ConcreteParameter::Json {
                        value: Cow::Borrowed(old_value),
                    }))
                }
            },
            Self::Expr { ty, expr } => match *ty {
                Type::Int => Ok(ControlFlow::Break(ConcreteParameter::Int {
                    value: expr.eval_int_with_context(eval_context).map_err(|source| {
                        ParameterEvalErrorInner::Evaluate {
                            source,
                            codec: String::from(codec),
                            parameter: String::from(name),
                        }
                    })?,
                })),
                Type::Float => Ok(ControlFlow::Break(ConcreteParameter::Float {
                    value: expr
                        .eval_float_with_context(eval_context)
                        .map_err(|source| ParameterEvalErrorInner::Evaluate {
                            source,
                            codec: String::from(codec),
                            parameter: String::from(name),
                        })?,
                })),
                Type::Str => Ok(ControlFlow::Break(ConcreteParameter::Str {
                    value: Cow::Owned(expr.eval_string_with_context(eval_context).map_err(
                        |source| ParameterEvalErrorInner::Evaluate {
                            source,
                            codec: String::from(codec),
                            parameter: String::from(name),
                        },
                    )?),
                })),
                Type::Json => Err(ParameterEvalErrorInner::EvalJsonValue {
                    codec: String::from(codec),
                    parameter: String::from(name),
                }
                .into()),
            },
        }
    }

    pub fn get(
        &self,
        codec: &str,
        name: &str,
        eval_context: &ParameterEvalContext,
    ) -> Result<ConcreteParameter<'a>, ParameterEvalError> {
        match self {
            Self::IntValue { value } | Self::IntRange { value, .. } => {
                Ok(ConcreteParameter::Int { value: *value })
            },
            Self::IntSet { values, index } => {
                let value = values.get(*index).copied().unwrap_or(values.head);
                Ok(ConcreteParameter::Int { value })
            },
            Self::FloatValue { value } => Ok(ConcreteParameter::Float { value: *value }),
            Self::FloatSet { values, index } => {
                let value = values.get(*index).copied().unwrap_or(values.head);
                Ok(ConcreteParameter::Float { value })
            },
            Self::StrValue { value } => Ok(ConcreteParameter::Str {
                value: Cow::Borrowed(value),
            }),
            Self::StrSet { values, index } => {
                let value = values.get(*index).unwrap_or(&values.head);
                Ok(ConcreteParameter::Str {
                    value: Cow::Borrowed(value),
                })
            },
            Self::JsonValue { value } => Ok(ConcreteParameter::Json {
                value: Cow::Borrowed(value),
            }),
            Self::JsonSet { values, index } => {
                let value = values.get(*index).unwrap_or(&values.head);
                Ok(ConcreteParameter::Json {
                    value: Cow::Borrowed(value),
                })
            },
            Self::Expr { ty, expr } => match *ty {
                Type::Int => Ok(ConcreteParameter::Int {
                    value: expr.eval_int_with_context(eval_context).map_err(|source| {
                        ParameterEvalErrorInner::Evaluate {
                            source,
                            codec: String::from(codec),
                            parameter: String::from(name),
                        }
                    })?,
                }),
                Type::Float => Ok(ConcreteParameter::Float {
                    value: expr
                        .eval_float_with_context(eval_context)
                        .map_err(|source| ParameterEvalErrorInner::Evaluate {
                            source,
                            codec: String::from(codec),
                            parameter: String::from(name),
                        })?,
                }),
                Type::Str => Ok(ConcreteParameter::Str {
                    value: Cow::Owned(expr.eval_string_with_context(eval_context).map_err(
                        |source| ParameterEvalErrorInner::Evaluate {
                            source,
                            codec: String::from(codec),
                            parameter: String::from(name),
                        },
                    )?),
                }),
                Type::Json => Err(ParameterEvalErrorInner::EvalJsonValue {
                    codec: String::from(codec),
                    parameter: String::from(name),
                }
                .into()),
            },
        }
    }
}

pub struct ParameterEvalContext {
    context: HashMapContext<DefaultNumericTypes>,
}

impl ParameterEvalContext {
    pub fn new() -> Result<Self, ParameterEvalError> {
        let mut context = HashMapContext::new();

        context
            .set_function(
                String::from("int"),
                Function::<DefaultNumericTypes>::new(|x| match x {
                    Value::Boolean(b) => Ok(Value::Int(i64::from(*b))),
                    Value::Int(i) => Ok(Value::Int(*i)),
                    #[expect(clippy::cast_precision_loss, clippy::cast_possible_truncation)]
                    Value::Float(f)
                        if f.is_finite() && *f >= (i64::MIN as f64) && *f <= (i64::MAX as f64) =>
                    {
                        Ok(Value::Int(*f as i64))
                    },
                    Value::Float(f) => Err(EvalexprError::expected_int(Value::Float(*f))),
                    Value::String(s) => s
                        .parse()
                        .map(Value::Int)
                        .map_err(|_| EvalexprError::expected_int(Value::String(s.clone()))),
                    Value::Tuple(t) => Err(EvalexprError::expected_int(Value::Tuple(t.clone()))),
                    Value::Empty => Err(EvalexprError::expected_int(Value::Empty)),
                }),
            )
            .map_err(|source| ParameterEvalErrorInner::InitialiseContext { source })?;
        context
            .set_function(
                String::from("float"),
                Function::new(|x| match x {
                    Value::Boolean(b) => Ok(Value::Float(f64::from(*b))),
                    #[expect(clippy::cast_precision_loss)]
                    Value::Int(i) => Ok(Value::Float(*i as f64)),
                    Value::Float(f) => Ok(Value::Float(*f)),
                    Value::String(s) => s
                        .parse()
                        .map(Value::Float)
                        .map_err(|_| EvalexprError::expected_float(Value::String(s.clone()))),
                    Value::Tuple(t) => Err(EvalexprError::expected_float(Value::Tuple(t.clone()))),
                    Value::Empty => Err(EvalexprError::expected_float(Value::Empty)),
                }),
            )
            .map_err(|source| ParameterEvalErrorInner::InitialiseContext { source })?;
        context
            .set_function(
                String::from("str"),
                Function::new(|x| match x {
                    Value::Boolean(b) => Ok(Value::String(format!("{b}"))),
                    Value::Int(i) => Ok(Value::String(format!("{i}"))),
                    Value::Float(f) => Ok(Value::String(format!("{f}"))),
                    Value::String(s) => Ok(Value::String(s.clone())),
                    t @ Value::Tuple(_) => Ok(Value::String(format!("{t}"))),
                    Value::Empty => Ok(Value::String(String::from("()"))),
                }),
            )
            .map_err(|source| ParameterEvalErrorInner::InitialiseContext { source })?;

        Ok(Self { context })
    }

    pub fn set_value(
        &mut self,
        codec: &str,
        parameter: &str,
        value: &ConcreteParameter,
    ) -> Result<(), ParameterEvalError> {
        let identifier = format!("{codec}.{parameter}");

        if let Some(prev) = self.context.get_value(&identifier) {
            return Err(ParameterEvalErrorInner::ValueAlreadySet {
                codec: String::from(codec),
                parameter: String::from(parameter),
                value: prev.clone(),
            }
            .into());
        }

        let value = match value {
            ConcreteParameter::Int { value } => Value::Int(*value),
            ConcreteParameter::Float { value } => Value::Float(*value),
            ConcreteParameter::Str { value } => Value::String(String::from(&**value)),
            // FIXME: JSON values are currently not stored in the context
            ConcreteParameter::Json { .. } => return Ok(()),
        };

        self.context
            .set_value(identifier, value.clone())
            .map_err(|source| {
                ParameterEvalErrorInner::SetValue {
                    source,
                    codec: String::from(codec),
                    parameter: String::from(parameter),
                    value,
                }
                .into()
            })
    }

    pub fn reset(&mut self) {
        self.context.clear_variables();
    }
}

impl Context for ParameterEvalContext {
    type NumericTypes = DefaultNumericTypes;

    fn get_value(&self, identifier: &str) -> Option<&Value> {
        self.context.get_value(identifier)
    }

    fn call_function(&self, identifier: &str, argument: &Value) -> Result<Value, EvalexprError> {
        self.context.call_function(identifier, argument)
    }

    fn are_builtin_functions_disabled(&self) -> bool {
        false
    }

    fn set_builtin_functions_disabled(&mut self, disabled: bool) -> Result<(), EvalexprError> {
        if disabled {
            Err(EvalexprError::BuiltinFunctionsCannotBeDisabled)
        } else {
            Ok(())
        }
    }
}

#[derive(Debug, Error)]
#[error(transparent)]
#[repr(transparent)]
pub struct ParameterEvalError(Box<ParameterEvalErrorInner>);

impl From<ParameterEvalErrorInner> for ParameterEvalError {
    fn from(err: ParameterEvalErrorInner) -> Self {
        Self(Box::new(err))
    }
}

impl From<ParameterEvalError> for ParameterEvalErrorInner {
    fn from(err: ParameterEvalError) -> Self {
        *err.0
    }
}

#[derive(Debug, Error)]
pub enum ParameterEvalErrorInner {
    #[error("failed to initialise parameter evaluation context")]
    InitialiseContext { source: EvalexprError },
    #[error("failed to set parameter `{codec}.{parameter}` value to {value}")]
    SetValue {
        source: EvalexprError,
        codec: String,
        parameter: String,
        value: Value,
    },
    #[error("cannot evaluate parameter `{codec}.{parameter}` into a JSON value")]
    EvalJsonValue { codec: String, parameter: String },
    #[error("parameter `{codec}.{parameter}` is already set to {value}")]
    ValueAlreadySet {
        codec: String,
        parameter: String,
        value: Value,
    },
    #[error("failed to evaluate parameter `{codec}.{parameter}`")]
    Evaluate {
        source: EvalexprError,
        codec: String,
        parameter: String,
    },
}

#[derive(Debug, Clone)]
pub enum ConcreteParameter<'a> {
    Int { value: i64 },
    Float { value: f64 },
    Str { value: Cow<'a, str> },
    Json { value: Cow<'a, JsonValue> },
}

impl<'a> ConcreteParameter<'a> {
    #[must_use]
    pub fn summary(&self) -> ConcreteParameterSummary<'a> {
        let inner = match self {
            Self::Int { value } => ConcreteParameterSummaryInner::Int {
                r#type: IntType::Int,
                value: *value,
            },
            Self::Float { value } => ConcreteParameterSummaryInner::Float {
                r#type: FloatType::Float,
                value: *value,
            },
            Self::Str { value } => ConcreteParameterSummaryInner::Str {
                r#type: StrType::Str,
                value: value.clone(),
            },
            Self::Json { value } => ConcreteParameterSummaryInner::Json {
                r#type: JsonType::Json,
                value: format!("{value}"),
            },
        };

        ConcreteParameterSummary { inner }
    }
}

impl Hash for ConcreteParameter<'_> {
    fn hash<H: Hasher>(&self, state: &mut H) {
        std::mem::discriminant(self).hash(state);

        match self {
            Self::Int { value } => value.hash(state),
            Self::Float { value } => {
                if value.is_nan() {
                    if value.is_sign_negative() {
                        f64::NAN.to_bits().hash(state);
                    } else {
                        (-f64::NAN).to_bits().hash(state);
                    }
                } else {
                    value.to_bits().hash(state);
                }
            },
            Self::Str { value } => value.hash(state),
            Self::Json { value } => value.hash(state),
        }
    }
}

impl fmt::Display for ConcreteParameter<'_> {
    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Self::Int { value } => value.fmt(fmt),
            Self::Float { value } => value.fmt(fmt),
            Self::Str { value } => fmt.write_fmt(format_args!("{value:?}")),
            Self::Json { value } => fmt.write_fmt(format_args!("{:?}", format!("{value}"))),
        }
    }
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
#[serde(rename = "Parameter")]
#[serde(transparent)]
pub struct ConcreteParameterSummary<'a> {
    #[serde(borrow)]
    inner: ConcreteParameterSummaryInner<'a>,
}

#[derive(Debug, Clone)]
enum ConcreteParameterSummaryInner<'a> {
    Int {
        r#type: IntType,
        value: i64,
    },
    Float {
        r#type: FloatType,
        value: f64,
    },
    Str {
        r#type: StrType,
        value: Cow<'a, str>,
    },
    Json {
        r#type: JsonType,
        value: String,
    },
}

// FIXME: eliminate extraneous clones
impl serde::Serialize for ConcreteParameterSummaryInner<'_> {
    fn serialize<S: serde::Serializer>(&self, serializer: S) -> Result<S::Ok, S::Error> {
        if serializer.is_human_readable() {
            match self {
                Self::Int {
                    r#type: IntType::Int,
                    value,
                } => ConcreteParameterSummaryInnerHumanReadable::Int {
                    r#type: IntType::Int,
                    value: *value,
                },
                Self::Float {
                    r#type: FloatType::Float,
                    value,
                } => ConcreteParameterSummaryInnerHumanReadable::Float {
                    r#type: FloatType::Float,
                    value: *value,
                },
                Self::Str {
                    r#type: StrType::Str,
                    value,
                } => ConcreteParameterSummaryInnerHumanReadable::Str {
                    r#type: StrType::Str,
                    value: value.clone(),
                },
                Self::Json {
                    r#type: JsonType::Json,
                    value,
                } => ConcreteParameterSummaryInnerHumanReadable::Json {
                    r#type: JsonType::Json,
                    value: Cow::Borrowed(value),
                },
            }
            .serialize(serializer)
        } else {
            match self {
                Self::Int {
                    r#type: IntType::Int,
                    value,
                } => ConcreteParameterSummaryInnerBinary::Int {
                    r#type: IntType::Int,
                    value: *value,
                },
                Self::Float {
                    r#type: FloatType::Float,
                    value,
                } => ConcreteParameterSummaryInnerBinary::Float {
                    r#type: FloatType::Float,
                    value: *value,
                },
                Self::Str {
                    r#type: StrType::Str,
                    value,
                } => ConcreteParameterSummaryInnerBinary::Str {
                    r#type: StrType::Str,
                    value: value.clone(),
                },
                Self::Json {
                    r#type: JsonType::Json,
                    value,
                } => ConcreteParameterSummaryInnerBinary::Json {
                    r#type: JsonType::Json,
                    value: Cow::Borrowed(value),
                },
            }
            .serialize(serializer)
        }
    }
}

impl<'a, 'de: 'a> serde::Deserialize<'de> for ConcreteParameterSummaryInner<'a> {
    fn deserialize<D: serde::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        if deserializer.is_human_readable() {
            match ConcreteParameterSummaryInnerHumanReadable::deserialize(deserializer)? {
                ConcreteParameterSummaryInnerHumanReadable::Int { r#type, value } => {
                    Ok(Self::Int { r#type, value })
                },
                ConcreteParameterSummaryInnerHumanReadable::Float { r#type, value } => {
                    Ok(Self::Float { r#type, value })
                },
                ConcreteParameterSummaryInnerHumanReadable::Str { r#type, value } => {
                    Ok(Self::Str { r#type, value })
                },
                ConcreteParameterSummaryInnerHumanReadable::Json { r#type, value } => {
                    Ok(Self::Json {
                        r#type,
                        value: value.into_owned(),
                    })
                },
            }
        } else {
            match ConcreteParameterSummaryInnerBinary::deserialize(deserializer)? {
                ConcreteParameterSummaryInnerBinary::Int { r#type, value } => {
                    Ok(Self::Int { r#type, value })
                },
                ConcreteParameterSummaryInnerBinary::Float { r#type, value } => {
                    Ok(Self::Float { r#type, value })
                },
                ConcreteParameterSummaryInnerBinary::Str { r#type, value } => {
                    Ok(Self::Str { r#type, value })
                },
                ConcreteParameterSummaryInnerBinary::Json { r#type, value } => Ok(Self::Json {
                    r#type,
                    value: value.into_owned(),
                }),
            }
        }
    }
}

#[derive(serde::Serialize, serde::Deserialize)]
#[serde(rename = "Parameter")]
#[serde(untagged)]
enum ConcreteParameterSummaryInnerHumanReadable<'a> {
    Int {
        r#type: IntType,
        value: i64,
    },
    Float {
        r#type: FloatType,
        value: f64,
    },
    Str {
        r#type: StrType,
        #[serde(borrow)]
        value: Cow<'a, str>,
    },
    Json {
        r#type: JsonType,
        #[serde(borrow)]
        value: Cow<'a, str>,
    },
}

#[derive(serde::Serialize, serde::Deserialize)]
#[serde(rename = "Parameter")]
enum ConcreteParameterSummaryInnerBinary<'a> {
    Int {
        r#type: IntType,
        value: i64,
    },
    Float {
        r#type: FloatType,
        value: f64,
    },
    Str {
        r#type: StrType,
        #[serde(borrow)]
        value: Cow<'a, str>,
    },
    Json {
        r#type: JsonType,
        #[serde(borrow)]
        value: Cow<'a, str>,
    },
}

#[derive(Debug, Clone, Copy, serde::Serialize, serde::Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum Type {
    Int,
    Float,
    Str,
    Json,
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
#[serde(rename = "Type")]
#[serde(rename_all = "lowercase")]
enum IntType {
    Int,
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
#[serde(rename = "Type")]
#[serde(rename_all = "lowercase")]
enum FloatType {
    Float,
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
#[serde(rename = "Type")]
#[serde(rename_all = "lowercase")]
enum StrType {
    Str,
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
#[serde(rename = "Type")]
#[serde(rename_all = "lowercase")]
enum JsonType {
    Json,
}
