use std::{borrow::Cow, fmt, str::FromStr};

use evalexpr::Node;
use nonempty::NonEmpty;
use serde::{Deserialize, Deserializer};
use serde_json::Value as JsonValue;
use vecmap::VecSet;

use super::{Parameter, ParameterEvalContext, Type};

pub struct ParameterSeed<'a> {
    eval_context: &'a ParameterEvalContext,
}

impl<'a> ParameterSeed<'a> {
    pub const fn new(eval_context: &'a ParameterEvalContext) -> Self {
        Self { eval_context }
    }
}

impl<'de> serde::de::DeserializeSeed<'de> for ParameterSeed<'_> {
    type Value = Parameter;

    fn deserialize<D: serde::Deserializer<'de>>(
        self,
        deserializer: D,
    ) -> Result<Self::Value, D::Error> {
        serde::Deserializer::deserialize_struct(deserializer, "Parameter", FIELDS, self)
    }
}

const FIELDS: &[&str] = &["type", "value", "valueset", "min", "max", "expr"];

struct TypeField;

impl<'de> serde::Deserialize<'de> for TypeField {
    fn deserialize<D: serde::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        struct Visitor;

        impl serde::de::Visitor<'_> for Visitor {
            type Value = TypeField;

            fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
                formatter.write_str("a codec config type field identifier")
            }

            fn visit_str<E: serde::de::Error>(self, value: &str) -> Result<Self::Value, E> {
                if value == "type" {
                    return Ok(TypeField);
                }
                Err(serde::de::Error::custom(format!(
                    "unexpected field `{value}`, a parameter must start with a `type` field"
                )))
            }

            fn visit_bytes<E: serde::de::Error>(self, value: &[u8]) -> Result<Self::Value, E> {
                if value == b"type" {
                    return Ok(TypeField);
                }
                let value = String::from_utf8_lossy(value);
                Err(serde::de::Error::custom(format!(
                    "unexpected field `{value}`, a parameter must start with a `type` field"
                )))
            }
        }

        serde::Deserializer::deserialize_identifier(deserializer, Visitor)
    }
}

#[derive(Clone, Copy)]
enum Field {
    Value,
    ValueSet,
    Min,
    Max,
    Expr,
}

struct FieldSeed<const N: usize> {
    keys: &'static [&'static str; N],
    values: &'static [Field; N],
}

impl<const N: usize> FieldSeed<N> {
    fn with_deserialize_key<
        'de,
        A: serde::de::MapAccess<'de>,
        F: FnOnce(&mut A, Field) -> Result<Option<Q>, A::Error>,
        Q,
    >(
        self,
        map: &mut A,
        inner: F,
    ) -> Result<Q, A::Error> {
        let keys = self.keys.as_slice();

        let mode = if let Some(field) = map.next_key_seed(self)? {
            match inner(map, field) {
                Ok(Some(result)) => return Ok(result),
                Ok(None) => "expected",
                Err(err) => return Err(err),
            }
        } else {
            "missing"
        };

        match keys {
            [] => Err(serde::de::Error::custom(format!(
                "{mode} an impossible field"
            ))),
            [a] => Err(serde::de::Error::custom(format!("{mode} field `{a}`"))),
            [a, b] => Err(serde::de::Error::custom(format!(
                "{mode} field `{a}` or `{b}`"
            ))),
            [a @ .., b] => {
                let mut msg = String::from("expected ");
                msg.push_str(mode);
                msg.push(' ');
                for a in a {
                    msg.push('`');
                    msg.push_str(a);
                    msg.push_str("`, ");
                }
                msg.push_str("or `");
                msg.push_str(b);
                msg.push('`');
                Err(serde::de::Error::custom(msg))
            },
        }
    }
}

impl<'de, const N: usize> serde::de::DeserializeSeed<'de> for FieldSeed<N> {
    type Value = Field;

    fn deserialize<D: serde::Deserializer<'de>>(
        self,
        deserializer: D,
    ) -> Result<Self::Value, D::Error> {
        serde::Deserializer::deserialize_identifier(deserializer, self)
    }
}

impl<const N: usize> serde::de::Visitor<'_> for FieldSeed<N> {
    type Value = Field;

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("a codec config field identifier")
    }

    fn visit_str<E: serde::de::Error>(self, value: &str) -> Result<Self::Value, E> {
        if let Some(field) = self
            .keys
            .iter()
            .position(|key| value == *key)
            .and_then(|index| self.values.get(index))
        {
            return Ok(*field);
        }

        Err(serde::de::Error::unknown_field(value, self.keys))
    }

    fn visit_bytes<E: serde::de::Error>(self, value: &[u8]) -> Result<Self::Value, E> {
        if let Some(field) = self
            .keys
            .iter()
            .position(|key| value == key.as_bytes())
            .and_then(|index| self.values.get(index))
        {
            return Ok(*field);
        }

        let value = String::from_utf8_lossy(value);
        Err(serde::de::Error::unknown_field(&value, self.keys))
    }
}

impl<'de> serde::de::Visitor<'de> for ParameterSeed<'_> {
    type Value = Parameter;

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("a codec parameter")
    }

    #[expect(clippy::too_many_lines)] // FIXME
    fn visit_map<A: serde::de::MapAccess<'de>>(self, mut map: A) -> Result<Self::Value, A::Error> {
        let Some(TypeField) = map.next_key()? else {
            return Err(serde::de::Error::custom("expected field `type`"));
        };
        let r#type: Type = map.next_value()?;

        let parameter = match r#type {
            Type::Int => FieldSeed {
                keys: &["value", "valueset", "min", "expr"],
                values: &[Field::Value, Field::ValueSet, Field::Min, Field::Expr],
            }
            .with_deserialize_key(&mut map, |map, field| match field {
                Field::Value => Ok(Some(Parameter::IntValue {
                    value: map.next_value()?,
                })),
                Field::ValueSet => {
                    let values: VecSet<i64> = map.next_value()?;
                    NonEmpty::collect(values.into_iter()).map_or_else(
                        || Err(serde::de::Error::custom("empty int parameter value set")),
                        |values| Ok(Some(Parameter::IntSet { values })),
                    )
                },
                Field::Min => {
                    let range_min: i64 = map.next_value()?;
                    FieldSeed {
                        keys: &["max"],
                        values: &[Field::Max],
                    }
                    .with_deserialize_key(map, |_, _| Ok(Some(())))?;
                    let range_max: i64 = map.next_value()?;
                    if range_max >= range_min {
                        Ok(Some(Parameter::IntRange {
                            min: range_min,
                            max: range_max,
                        }))
                    } else {
                        Err(serde::de::Error::custom(
                            "empty int parameter min..=max range",
                        ))
                    }
                },
                Field::Max => Ok(None),
                Field::Expr => Ok(Some(Parameter::Expr {
                    ty: Type::Int,
                    expr: map.next_value_seed(ExprSeed {
                        ty: Type::Int,
                        context: self.eval_context,
                    })?,
                })),
            }),
            Type::Float => FieldSeed {
                keys: &["value", "valueset", "expr"],
                values: &[Field::Value, Field::ValueSet, Field::Expr],
            }
            .with_deserialize_key(&mut map, |map, field| match field {
                Field::Value => Ok(Some(Parameter::FloatValue {
                    value: map.next_value()?,
                })),
                Field::ValueSet => {
                    let values: VecSet<F64> = map.next_value()?;
                    NonEmpty::collect(values.into_iter().map(|f| f.0)).map_or_else(
                        || Err(serde::de::Error::custom("empty float parameter value set")),
                        |values| Ok(Some(Parameter::FloatSet { values })),
                    )
                },
                Field::Expr => Ok(Some(Parameter::Expr {
                    ty: Type::Float,
                    expr: map.next_value_seed(ExprSeed {
                        ty: Type::Float,
                        context: self.eval_context,
                    })?,
                })),
                _ => Ok(None),
            }),
            Type::Str => FieldSeed {
                keys: &["value", "valueset", "expr"],
                values: &[Field::Value, Field::ValueSet, Field::Expr],
            }
            .with_deserialize_key(&mut map, |map, field| match field {
                Field::Value => Ok(Some(Parameter::StrValue {
                    value: map.next_value()?,
                })),
                Field::ValueSet => {
                    let values: VecSet<String> = map.next_value()?;
                    NonEmpty::collect(values.into_iter()).map_or_else(
                        || Err(serde::de::Error::custom("empty str parameter value set")),
                        |values| Ok(Some(Parameter::StrSet { values })),
                    )
                },
                Field::Expr => Ok(Some(Parameter::Expr {
                    ty: Type::Str,
                    expr: map.next_value_seed(ExprSeed {
                        ty: Type::Str,
                        context: self.eval_context,
                    })?,
                })),
                _ => Ok(None),
            }),
            Type::Json => FieldSeed {
                keys: &["value", "valueset"],
                values: &[Field::Value, Field::ValueSet],
            }
            .with_deserialize_key(&mut map, |map, field| match field {
                Field::Value => Ok(Some(Parameter::JsonValue {
                    value: map.next_value::<JsonString>()?.0,
                })),
                Field::ValueSet => {
                    let values: VecSet<JsonString> = map.next_value()?;
                    let values: VecSet<JsonValue> =
                        values.into_iter().map(|value| value.0).collect();
                    NonEmpty::collect(values.into_iter()).map_or_else(
                        || Err(serde::de::Error::custom("empty json parameter value set")),
                        |values| Ok(Some(Parameter::JsonSet { values })),
                    )
                },
                _ => Ok(None),
            }),
        }?;

        map.next_key_seed(FieldSeed {
            keys: &[],
            values: &[],
        })?;

        Ok(parameter)
    }
}

#[derive(serde::Deserialize)]
#[repr(transparent)]
struct F64(f64);

impl PartialEq for F64 {
    fn eq(&self, other: &Self) -> bool {
        match self.0.total_cmp(&other.0) {
            std::cmp::Ordering::Equal => true,
            std::cmp::Ordering::Less | std::cmp::Ordering::Greater => false,
        }
    }
}

#[derive(PartialEq, Eq)]
struct JsonString(JsonValue);

impl<'de> Deserialize<'de> for JsonString {
    fn deserialize<D: Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        let json = Cow::<str>::deserialize(deserializer)?;
        let json: JsonValue = JsonValue::from_str(&json).map_err(serde::de::Error::custom)?;
        Ok(Self(json))
    }
}

impl Eq for F64 {}

struct ExprSeed<'a> {
    ty: Type,
    context: &'a ParameterEvalContext,
}

impl<'de> serde::de::DeserializeSeed<'de> for ExprSeed<'_> {
    type Value = Node;

    fn deserialize<D: serde::Deserializer<'de>>(
        self,
        deserializer: D,
    ) -> Result<Self::Value, D::Error> {
        deserializer.deserialize_str(self)
    }
}

impl serde::de::Visitor<'_> for ExprSeed<'_> {
    type Value = Node;

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("an expression string")
    }

    fn visit_str<E: serde::de::Error>(self, v: &str) -> Result<Self::Value, E> {
        let expr = evalexpr::build_operator_tree(v).map_err(serde::de::Error::custom)?;

        match self.ty {
            Type::Int => expr.eval_int_with_context(self.context).map(|_| ()),
            Type::Float => expr.eval_float_with_context(self.context).map(|_| ()),
            Type::Str => expr.eval_string_with_context(self.context).map(|_| ()),
            Type::Json => expr.eval_with_context(self.context).map(|_| ()),
        }
        .map_err(serde::de::Error::custom)?;

        Ok(expr)
    }
}
