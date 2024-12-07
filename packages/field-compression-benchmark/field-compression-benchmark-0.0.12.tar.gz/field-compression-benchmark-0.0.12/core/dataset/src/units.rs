use std::{
    borrow::Cow,
    fmt::{self, Write},
    hash::{Hash, Hasher},
};

use pyo3::{
    exceptions::PyAssertionError,
    ffi::PyTypeObject,
    intern,
    prelude::*,
    sync::GILOnceCell,
    types::{DerefToPyAny, IntoPyDict, PyFloat, PyInt, PyString, PyType},
    PyTypeInfo,
};
use vecmap::VecMap;

use core_error::LocationError;

#[repr(transparent)]
pub struct UnitRegistry {
    registry: PyAny,
}

pub trait UnitRegistryMethods<'py>: Sized {
    fn try_new(py: Python<'py>) -> Result<Self, LocationError<PyErr>>;

    fn resolve(&self, units: &str) -> Result<DataUnit, LocationError<PyErr>>;
}

impl<'py> UnitRegistryMethods<'py> for Bound<'py, UnitRegistry> {
    fn try_new(py: Python<'py>) -> Result<Self, LocationError<PyErr>> {
        let registry = pint_unit_registry(py)?.call0()?;
        registry.extract().map_err(LocationError::new)
    }

    fn resolve(&self, units: &str) -> Result<DataUnit, LocationError<PyErr>> {
        let py = self.py();

        // Fix up the units string to translate "m2 m-2" to "m**2 m**-2"
        let mut fixed_units = String::with_capacity(units.len());
        let mut last_unit = false;
        for c in units.chars() {
            if last_unit && matches!(c, '+' | '-' | '0'..='9') {
                fixed_units.push_str("**");
            }
            fixed_units.push(c);
            if matches!(c, '+' | '-' | '*' | '/' | '0'..='9') {
                last_unit = false;
            } else if !c.is_whitespace() {
                last_unit = true;
            }
        }
        let fixed_units = PyString::new(py, &fixed_units);

        let verbose_unit = self.call1((fixed_units.as_borrowed(),))?;
        let verbose = ParsedDataUnit::parse(
            py,
            self.as_borrowed(),
            fixed_units.as_borrowed(),
            verbose_unit.as_borrowed(),
        )?;

        let base_unit = verbose_unit.call_method0(intern!(py, "to_base_units"))?;
        let base_unit_str = base_unit.str()?;
        let base = ParsedDataUnit::parse(
            py,
            self.as_borrowed(),
            base_unit_str.as_borrowed(),
            base_unit.as_borrowed(),
        )?;

        Ok(DataUnit { verbose, base })
    }
}

impl DerefToPyAny for UnitRegistry {}

#[expect(unsafe_code)]
unsafe impl PyTypeInfo for UnitRegistry {
    const MODULE: Option<&'static str> = Some("pint");
    const NAME: &'static str = "UnitRegistry";

    #[inline]
    fn type_object_raw(py: Python) -> *mut PyTypeObject {
        #[expect(clippy::expect_used)]
        let ty =
            pint_unit_registry(py).expect("failed to access the `pint.UnitRegistry` type object");

        ty.as_type_ptr()
    }
}

fn pint_unit_registry(py: Python) -> Result<&Bound<PyType>, PyErr> {
    static PINT_UNIT_REGISTRY: GILOnceCell<Py<PyType>> = GILOnceCell::new();
    PINT_UNIT_REGISTRY.import(py, "pint", "UnitRegistry")
}

#[derive(Debug, Clone)]
pub struct DataUnit {
    verbose: ParsedDataUnit,
    base: ParsedDataUnit,
}

impl DataUnit {
    #[must_use]
    pub const fn verbose(&self) -> &ParsedDataUnit {
        &self.verbose
    }

    #[must_use]
    pub const fn base(&self) -> &ParsedDataUnit {
        &self.base
    }

    #[must_use]
    pub fn summary(&self) -> DataUnitSummary {
        DataUnitSummary {
            verbose: self.verbose.summary(),
            base: self.base.summary(),
        }
    }
}

impl Hash for DataUnit {
    fn hash<H: Hasher>(&self, state: &mut H) {
        // Note: we only hash verbose representation, since the base is derived from it
        self.verbose.hash(state);
    }
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
#[serde(rename = "DataUnit")]
#[serde(deny_unknown_fields)]
pub struct DataUnitSummary<'a> {
    #[serde(borrow)]
    verbose: ParsedDataUnitSummary<'a>,
    #[serde(borrow)]
    base: ParsedDataUnitSummary<'a>,
}

#[derive(Debug, Clone)]
pub struct ParsedDataUnit {
    magnitude: f64,
    units: VecMap<String, f64>,
    expression: Option<UnitExpression>,
}

impl ParsedDataUnit {
    #[must_use]
    pub const fn magnitude(&self) -> f64 {
        self.magnitude
    }

    #[must_use]
    pub fn units(&self) -> impl ExactSizeIterator<Item = (&str, f64)> {
        self.units
            .iter()
            .map(|(unit, exponent)| (&**unit, *exponent))
    }

    #[must_use]
    pub const fn expression(&self) -> Option<&UnitExpression> {
        self.expression.as_ref()
    }

    #[must_use]
    pub fn summary(&self) -> ParsedDataUnitSummary {
        ParsedDataUnitSummary {
            magnitude: self.magnitude,
            units: self
                .units
                .iter()
                .map(|(unit, exponent)| (Cow::Borrowed(unit.as_str()), *exponent))
                .collect(),
            expression: UnitExpression::summary(self.expression.as_ref()),
        }
    }

    fn parse<'py>(
        py: Python<'py>,
        registry: Borrowed<'_, 'py, UnitRegistry>,
        unit_str: Borrowed<'_, 'py, PyString>,
        pint_unit: Borrowed<'_, 'py, PyAny>,
    ) -> Result<Self, LocationError<PyErr>> {
        static PINT_EVAL_TOKENIZER: GILOnceCell<Py<PyAny>> = GILOnceCell::new();
        static PINT_BUILD_EVAL_TREE: GILOnceCell<Py<PyAny>> = GILOnceCell::new();
        static FUNCTOOLS_PARTIAL: GILOnceCell<Py<PyAny>> = GILOnceCell::new();

        macro_rules! once {
            ($py:ident, $module:literal, $name:literal) => {{
                fn once(py: Python) -> Result<&Bound<PyAny>, PyErr> {
                    static ONCE: GILOnceCell<Py<PyAny>> = GILOnceCell::new();
                    ONCE.import(py, $module, $name)
                }

                once($py)
            }};
        }

        let tree = match PINT_EVAL_TOKENIZER
            .import(py, "pint.pint_eval", "tokenizer")?
            .call1((unit_str,))
        {
            Ok(tokens) => Some(
                PINT_BUILD_EVAL_TREE
                    .import(py, "pint.pint_eval", "build_eval_tree")?
                    .call1((tokens,))?,
            ),
            Err(err) if err.is_instance_of::<PyAssertionError>(py) => None,
            Err(err) => return Err(err.into()),
        };

        let expression = if let Some(tree) = tree {
            let unary_operator_map = [
                (intern!(py, "+"), once!(py, "operator", "pos")?),
                (intern!(py, "-"), once!(py, "operator", "neg")?),
            ]
            .into_py_dict(py)?;

            let binary_operator_map = [
                (intern!(py, "**"), once!(py, "operator", "pow")?),
                (intern!(py, "*"), once!(py, "operator", "mul")?),
                (intern!(py, ""), once!(py, "operator", "mul")?),
                (intern!(py, "/"), once!(py, "operator", "truediv")?),
                (intern!(py, "+"), once!(py, "operator", "add")?),
                (intern!(py, "-"), once!(py, "operator", "sub")?),
                (intern!(py, "%"), once!(py, "operator", "mod")?),
                (intern!(py, "//"), once!(py, "operator", "floordiv")?),
            ]
            .into_py_dict(py)?;

            let kwargs = [
                (intern!(py, "un_op"), unary_operator_map),
                (intern!(py, "bin_op"), binary_operator_map),
            ]
            .into_py_dict(py)?;

            let expression: PyUnitExpression = tree
                .call_method(
                    intern!(py, "evaluate"),
                    (FUNCTOOLS_PARTIAL
                        .import(py, "functools", "partial")?
                        .call1((PyUnitExpression::type_object(py), registry))?,),
                    Some(&kwargs),
                )?
                .extract()?;

            expression.expression.map(UnitExpression::simplify)
        } else {
            None
        };

        let magnitude = pint_unit.getattr(intern!(py, "magnitude"))?.extract()?;

        let mut units = VecMap::new();
        for unit in pint_unit
            .getattr(intern!(py, "_units"))?
            .call_method0(intern!(py, "items"))?
            .try_iter()?
        {
            let (name, exponent) = unit?.extract()?;
            units.insert(name, exponent);
        }

        Ok(Self {
            magnitude,
            units,
            expression,
        })
    }
}

impl Hash for ParsedDataUnit {
    fn hash<H: Hasher>(&self, state: &mut H) {
        struct WriteHasher<'a, H: Hasher>(&'a mut H);

        impl<H: Hasher> fmt::Write for WriteHasher<'_, H> {
            fn write_str(&mut self, s: &str) -> fmt::Result {
                s.hash(self.0);
                Ok(())
            }
        }

        // Note: we only hash the expression, since the magnitude and units are derived
        //       from it
        let _ = write!(
            WriteHasher(state),
            "{}",
            UnitExpression::as_ascii(self.expression.as_ref())
        );
    }
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
#[serde(rename = "ParsedDataUnit")]
#[serde(deny_unknown_fields)]
pub struct ParsedDataUnitSummary<'a> {
    magnitude: f64,
    #[serde(borrow)]
    units: VecMap<Cow<'a, str>, f64>,
    #[serde(borrow)]
    expression: UnitExpressionSummary<'a>,
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
#[serde(rename = "UnitExpression")]
#[serde(deny_unknown_fields)]
pub struct UnitExpressionSummary<'a> {
    #[serde(borrow)]
    ascii: Cow<'a, str>,
    #[serde(borrow)]
    latex: Cow<'a, str>,
}

#[pyclass(frozen)]
#[derive(Clone)]
struct PyUnitExpression {
    expression: Option<UnitExpression>,
}

#[pymethods]
impl PyUnitExpression {
    #[new]
    fn define<'py>(
        py: Python<'py>,
        registry: &Bound<'py, PyAny>,
        expr: &Bound<'py, PyAny>,
    ) -> Result<Self, PyErr> {
        let expr = expr.getattr(intern!(py, "string"))?;

        let expression = if let Ok(float) = PyFloat::type_object(py).call1((&expr,)) {
            let int = PyInt::type_object(py).call1((&float,))?;

            if float.eq(&int)? {
                Some(UnitExpression::Integer(int.extract()?))
            } else {
                Some(UnitExpression::Float(float.extract()?))
            }
        } else if expr.eq("dimensionless")? {
            None
        } else {
            let unit = registry
                .call_method1(intern!(py, "get_symbol"), (expr,))?
                .extract()?;

            Some(UnitExpression::Unit(unit))
        };

        Ok(Self { expression })
    }

    const fn __pos__(this: PyRef<Self>) -> PyRef<Self> {
        this
    }

    fn __neg__(&self) -> Self {
        Self {
            expression: self
                .expression
                .as_ref()
                .map(|expr| UnitExpression::Negate(Box::new(expr.clone()))),
        }
    }

    fn __pow__(&self, rhs: Self, _modulo: Option<&Bound<PyAny>>) -> Self {
        Self {
            expression: match (&self.expression, rhs.expression) {
                (Some(base), Some(exp)) => Some(UnitExpression::Power {
                    base: Box::new(base.clone()),
                    exp: Box::new(exp),
                }),
                (Some(base), None) => Some(base.clone()),
                (None, _) => None,
            },
        }
    }

    fn __mul__(&self, rhs: Self) -> Self {
        Self {
            expression: match (&self.expression, rhs.expression) {
                (Some(left), Some(right)) => Some(UnitExpression::Multiply {
                    left: Box::new(left.clone()),
                    right: Box::new(right),
                }),
                (Some(left), None) => Some(left.clone()),
                (None, Some(right)) => Some(right),
                (None, None) => None,
            },
        }
    }

    fn __truediv__(&self, rhs: Self) -> Self {
        Self {
            expression: match (&self.expression, rhs.expression) {
                (Some(dividend), Some(divisor)) => Some(UnitExpression::Divide {
                    dividend: Box::new(dividend.clone()),
                    divisor: Box::new(divisor),
                }),
                (Some(dividend), None) => Some(dividend.clone()),
                (None, Some(divisor)) => Some(UnitExpression::Divide {
                    dividend: Box::new(UnitExpression::Integer(1)),
                    divisor: Box::new(divisor),
                }),
                (None, None) => None,
            },
        }
    }

    fn __add__(&self, rhs: Self) -> Self {
        Self {
            expression: match (&self.expression, rhs.expression) {
                (Some(left), Some(right)) => Some(UnitExpression::Add {
                    left: Box::new(left.clone()),
                    right: Box::new(right),
                }),
                (Some(left), None) => Some(left.clone()),
                (None, Some(right)) => Some(right),
                (None, None) => None,
            },
        }
    }

    fn __sub__(&self, rhs: Self) -> Self {
        Self {
            expression: match (&self.expression, rhs.expression) {
                (Some(left), Some(right)) => Some(UnitExpression::Subtract {
                    left: Box::new(left.clone()),
                    right: Box::new(right),
                }),
                (Some(left), None) => Some(left.clone()),
                (None, Some(right)) => Some(UnitExpression::Negate(Box::new(right))),
                (None, None) => None,
            },
        }
    }

    fn __mod__(&self, rhs: Self) -> Self {
        Self {
            expression: match (&self.expression, rhs.expression) {
                (Some(dividend), Some(divisor)) => Some(UnitExpression::Modulo {
                    dividend: Box::new(dividend.clone()),
                    divisor: Box::new(divisor),
                }),
                (Some(dividend), None) => Some(dividend.clone()),
                (None, Some(divisor)) => Some(UnitExpression::Modulo {
                    dividend: Box::new(UnitExpression::Integer(1)),
                    divisor: Box::new(divisor),
                }),
                (None, None) => None,
            },
        }
    }

    fn __floordiv__(&self, rhs: Self) -> Self {
        Self {
            expression: match (&self.expression, rhs.expression) {
                (Some(dividend), Some(divisor)) => {
                    Some(UnitExpression::Floor(Box::new(UnitExpression::Divide {
                        dividend: Box::new(dividend.clone()),
                        divisor: Box::new(divisor),
                    })))
                },
                (Some(dividend), None) => Some(dividend.clone()),
                (None, Some(divisor)) => {
                    Some(UnitExpression::Floor(Box::new(UnitExpression::Divide {
                        dividend: Box::new(UnitExpression::Integer(1)),
                        divisor: Box::new(divisor),
                    })))
                },
                (None, None) => None,
            },
        }
    }
}

#[derive(Debug, Clone)]
pub enum UnitExpression {
    Integer(i64),
    Float(f64),
    Unit(String),
    Negate(Box<Self>),
    Power {
        base: Box<Self>,
        exp: Box<Self>,
    },
    Multiply {
        left: Box<Self>,
        right: Box<Self>,
    },
    Divide {
        dividend: Box<Self>,
        divisor: Box<Self>,
    },
    Add {
        left: Box<Self>,
        right: Box<Self>,
    },
    Subtract {
        left: Box<Self>,
        right: Box<Self>,
    },
    Modulo {
        dividend: Box<Self>,
        divisor: Box<Self>,
    },
    Floor(Box<Self>),
}

impl UnitExpression {
    #[must_use]
    pub fn as_ascii(expression: Option<&Self>) -> impl fmt::Display + '_ {
        struct UnitExpressionAsciiFormatter<'a>(pub Option<&'a UnitExpression>);

        impl fmt::Display for UnitExpressionAsciiFormatter<'_> {
            fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
                if let Some(expression) = self.0 {
                    expression.format_as_ascii(fmt)
                } else {
                    fmt.write_str("dimensionless")
                }
            }
        }

        UnitExpressionAsciiFormatter(expression)
    }

    #[must_use]
    pub fn as_latex(expression: Option<&Self>) -> impl fmt::Display + '_ {
        struct UnitExpressionLatexFormatter<'a>(pub Option<&'a UnitExpression>);

        impl fmt::Display for UnitExpressionLatexFormatter<'_> {
            fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
                struct LatexFormatter<'a>(&'a UnitExpression);

                impl fmt::Display for LatexFormatter<'_> {
                    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
                        self.0.format_as_latex(fmt)
                    }
                }

                if let Some(expression) = self.0 {
                    fmt.write_fmt(format_args!("${}$", LatexFormatter(expression)))
                } else {
                    fmt.write_str("dimensionless")
                }
            }
        }

        UnitExpressionLatexFormatter(expression)
    }

    #[must_use]
    pub fn summary(expression: Option<&Self>) -> UnitExpressionSummary {
        UnitExpressionSummary {
            ascii: Cow::Owned(format!("{}", Self::as_ascii(expression))),
            latex: Cow::Owned(format!("{}", Self::as_latex(expression))),
        }
    }
}

impl UnitExpression {
    #[expect(clippy::too_many_lines)] // FIXME
    fn simplify(self) -> Self {
        match self {
            expr @ (Self::Integer(_) | Self::Float(_) | Self::Unit(_)) => expr,
            Self::Negate(expr) => match expr.simplify() {
                expr @ (Self::Integer(_)
                | Self::Float(_)
                | Self::Unit(_)
                | Self::Power { .. }
                | Self::Multiply { .. }
                | Self::Divide { .. }
                | Self::Add { .. }
                | Self::Modulo { .. }
                | Self::Floor { .. }) => Self::Negate(Box::new(expr)),
                Self::Negate(inner) => *inner,
                Self::Subtract { left, right } => Self::Subtract {
                    left: right,
                    right: left,
                },
            },
            Self::Power { base, exp } => match (base.simplify(), exp.simplify()) {
                (_, Self::Integer(0)) | (Self::Integer(1), _) => Self::Integer(1),
                (Self::Integer(0), _) => Self::Integer(0),
                (base, exp) => Self::Power {
                    base: Box::new(base),
                    exp: Box::new(exp),
                },
            },
            Self::Multiply { left, right } => match (left.simplify(), right.simplify()) {
                (Self::Integer(0), _) | (_, Self::Integer(0)) => Self::Integer(0),
                (Self::Integer(1), expr) | (expr, Self::Integer(1)) => expr,
                (Self::Negate(left), Self::Negate(right)) => Self::Multiply { left, right },
                (Self::Negate(left), right) => Self::Negate(Box::new(Self::Multiply {
                    left,
                    right: Box::new(right),
                })),
                (left, Self::Negate(right)) => Self::Negate(Box::new(Self::Multiply {
                    left: Box::new(left),
                    right,
                })),
                (left, right) => Self::Multiply {
                    left: Box::new(left),
                    right: Box::new(right),
                },
            },
            Self::Divide { dividend, divisor } => match (dividend.simplify(), divisor.simplify()) {
                (Self::Integer(0), _) => Self::Integer(0),
                (dividend, Self::Integer(1)) => dividend,
                (Self::Negate(dividend), Self::Negate(divisor)) => {
                    Self::Divide { dividend, divisor }
                },
                (Self::Negate(dividend), divisor) => Self::Negate(Box::new(Self::Divide {
                    dividend,
                    divisor: Box::new(divisor),
                })),
                (dividend, Self::Negate(divisor)) => Self::Negate(Box::new(Self::Divide {
                    dividend: Box::new(dividend),
                    divisor,
                })),
                (dividend, divisor) => Self::Divide {
                    dividend: Box::new(dividend),
                    divisor: Box::new(divisor),
                },
            },
            Self::Add { left, right } => match (left.simplify(), right.simplify()) {
                (Self::Integer(0), expr) | (expr, Self::Integer(0)) => expr,
                (Self::Negate(left), Self::Negate(right)) => {
                    Self::Negate(Box::new(Self::Add { left, right }))
                },
                (Self::Negate(left), right) => Self::Subtract {
                    left: Box::new(right),
                    right: left,
                },
                (left, Self::Negate(right)) => Self::Subtract {
                    left: Box::new(left),
                    right,
                },
                (left, right) => Self::Add {
                    left: Box::new(left),
                    right: Box::new(right),
                },
            },
            Self::Subtract { left, right } => match (left.simplify(), right.simplify()) {
                (Self::Integer(0), expr) => Self::Negate(Box::new(expr)),
                (expr, Self::Integer(0)) => expr,
                (Self::Negate(left), Self::Negate(right)) => Self::Subtract { right, left },
                (Self::Negate(left), right) => Self::Negate(Box::new(Self::Add {
                    left,
                    right: Box::new(right),
                })),
                (left, Self::Negate(right)) => Self::Add {
                    left: Box::new(left),
                    right,
                },
                (left, right) => Self::Subtract {
                    left: Box::new(left),
                    right: Box::new(right),
                },
            },
            Self::Modulo { dividend, divisor } => match (dividend.simplify(), divisor.simplify()) {
                (Self::Integer(0), _) => Self::Integer(0),
                (dividend, divisor) => Self::Modulo {
                    dividend: Box::new(dividend),
                    divisor: Box::new(divisor),
                },
            },
            Self::Floor(expr) => Self::Floor(Box::new(expr.simplify())),
        }
    }

    fn format_as_latex(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        struct LatexFormatter<'a>(&'a UnitExpression);

        impl fmt::Display for LatexFormatter<'_> {
            fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
                self.0.format_as_latex(fmt)
            }
        }

        struct ParenUnlessPrimitive<'a>(&'a UnitExpression);

        impl fmt::Display for ParenUnlessPrimitive<'_> {
            fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
                match &self.0 {
                    expr @ (UnitExpression::Integer(_)
                    | UnitExpression::Float(_)
                    | UnitExpression::Unit(_)) => expr.format_as_latex(fmt),
                    expr => fmt.write_fmt(format_args!("({})", LatexFormatter(expr))),
                }
            }
        }

        struct ParenUnlessMultiplyDividePrimitive<'a>(&'a UnitExpression);

        impl fmt::Display for ParenUnlessMultiplyDividePrimitive<'_> {
            fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
                match &self.0 {
                    expr @ (UnitExpression::Integer(_)
                    | UnitExpression::Float(_)
                    | UnitExpression::Unit(_)
                    | UnitExpression::Multiply { .. }
                    | UnitExpression::Divide { .. }) => expr.format_as_latex(fmt),
                    expr => fmt.write_fmt(format_args!("({})", LatexFormatter(expr))),
                }
            }
        }

        struct ParenUnlessAddSubtractPrimitive<'a>(&'a UnitExpression);

        impl fmt::Display for ParenUnlessAddSubtractPrimitive<'_> {
            fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
                match &self.0 {
                    expr @ (UnitExpression::Integer(_)
                    | UnitExpression::Float(_)
                    | UnitExpression::Unit(_)
                    | UnitExpression::Add { .. }
                    | UnitExpression::Subtract { .. }) => expr.format_as_latex(fmt),
                    expr => fmt.write_fmt(format_args!("({})", LatexFormatter(expr))),
                }
            }
        }

        match self {
            Self::Integer(int) => fmt.write_fmt(format_args!("{int}")),
            Self::Float(float) => fmt.write_fmt(format_args!("{float}")),
            Self::Unit(unit) => fmt.write_str(unit),
            Self::Negate(expr) => fmt.write_fmt(format_args!("-{}", ParenUnlessPrimitive(expr))),
            Self::Power { base, exp } => fmt.write_fmt(format_args!(
                "{{{}}}^{{{}}}",
                ParenUnlessPrimitive(base),
                LatexFormatter(exp)
            )),
            Self::Multiply { left, right } => fmt.write_fmt(format_args!(
                r"{} \cdot {}",
                ParenUnlessMultiplyDividePrimitive(left),
                ParenUnlessMultiplyDividePrimitive(right)
            )),
            Self::Divide { dividend, divisor } => fmt.write_fmt(format_args!(
                r"{} \div {}",
                ParenUnlessMultiplyDividePrimitive(dividend),
                ParenUnlessMultiplyDividePrimitive(divisor)
            )),
            Self::Add { left, right } => fmt.write_fmt(format_args!(
                "{} + {}",
                ParenUnlessAddSubtractPrimitive(left),
                ParenUnlessAddSubtractPrimitive(right)
            )),
            Self::Subtract { left, right } => fmt.write_fmt(format_args!(
                "{} - {}",
                ParenUnlessAddSubtractPrimitive(left),
                ParenUnlessAddSubtractPrimitive(right)
            )),
            Self::Modulo { dividend, divisor } => fmt.write_fmt(format_args!(
                "{}$ mod ${}",
                ParenUnlessPrimitive(dividend),
                ParenUnlessPrimitive(divisor)
            )),
            Self::Floor(expr) => {
                fmt.write_fmt(format_args!(r"\lfloor {} \rfloor", LatexFormatter(expr),))
            },
        }
    }

    fn format_as_ascii(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        struct AsciiFormatter<'a>(&'a UnitExpression);

        impl fmt::Display for AsciiFormatter<'_> {
            fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
                self.0.format_as_ascii(fmt)
            }
        }

        struct ParenUnlessPrimitive<'a>(&'a UnitExpression);

        impl fmt::Display for ParenUnlessPrimitive<'_> {
            fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
                match &self.0 {
                    expr @ (UnitExpression::Integer(_)
                    | UnitExpression::Float(_)
                    | UnitExpression::Unit(_)) => expr.format_as_ascii(fmt),
                    expr => fmt.write_fmt(format_args!("({})", AsciiFormatter(expr))),
                }
            }
        }

        struct ParenUnlessMultiplyDividePrimitive<'a>(&'a UnitExpression);

        impl fmt::Display for ParenUnlessMultiplyDividePrimitive<'_> {
            fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
                match &self.0 {
                    expr @ (UnitExpression::Integer(_)
                    | UnitExpression::Float(_)
                    | UnitExpression::Unit(_)
                    | UnitExpression::Multiply { .. }
                    | UnitExpression::Divide { .. }) => expr.format_as_ascii(fmt),
                    expr => fmt.write_fmt(format_args!("({})", AsciiFormatter(expr))),
                }
            }
        }

        struct ParenUnlessAddSubtractPrimitive<'a>(&'a UnitExpression);

        impl fmt::Display for ParenUnlessAddSubtractPrimitive<'_> {
            fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
                match &self.0 {
                    expr @ (UnitExpression::Integer(_)
                    | UnitExpression::Float(_)
                    | UnitExpression::Unit(_)
                    | UnitExpression::Add { .. }
                    | UnitExpression::Subtract { .. }) => expr.format_as_ascii(fmt),
                    expr => fmt.write_fmt(format_args!("({})", AsciiFormatter(expr))),
                }
            }
        }

        match self {
            Self::Integer(int) => fmt.write_fmt(format_args!("{int}")),
            Self::Float(float) => fmt.write_fmt(format_args!("{float}")),
            Self::Unit(unit) => fmt.write_str(unit),
            Self::Negate(expr) => fmt.write_fmt(format_args!("-{}", ParenUnlessPrimitive(expr))),
            Self::Power { base, exp } => fmt.write_fmt(format_args!(
                "{} ** {}",
                ParenUnlessPrimitive(base),
                ParenUnlessPrimitive(exp)
            )),
            Self::Multiply { left, right } => fmt.write_fmt(format_args!(
                "{} * {}",
                ParenUnlessMultiplyDividePrimitive(left),
                ParenUnlessMultiplyDividePrimitive(right)
            )),
            Self::Divide { dividend, divisor } => fmt.write_fmt(format_args!(
                "{} / {}",
                ParenUnlessMultiplyDividePrimitive(dividend),
                ParenUnlessMultiplyDividePrimitive(divisor)
            )),
            Self::Add { left, right } => fmt.write_fmt(format_args!(
                "{} + {}",
                ParenUnlessAddSubtractPrimitive(left),
                ParenUnlessAddSubtractPrimitive(right)
            )),
            Self::Subtract { left, right } => fmt.write_fmt(format_args!(
                "{} - {}",
                ParenUnlessAddSubtractPrimitive(left),
                ParenUnlessAddSubtractPrimitive(right)
            )),
            Self::Modulo { dividend, divisor } => fmt.write_fmt(format_args!(
                "{} mod {}",
                ParenUnlessPrimitive(dividend),
                ParenUnlessPrimitive(divisor)
            )),
            Self::Floor(expr) => fmt.write_fmt(format_args!(r"floor({})", AsciiFormatter(expr))),
        }
    }
}
