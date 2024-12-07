use std::{convert::Infallible, fmt};

use nonempty::NonEmpty;
use sorted_vec::SortedSet;
use vecmap::VecSet;

use super::DataDerivative;

pub struct DataDerivativeFormulaSetSeed<'a> {
    variable: &'a str,
    dimensions: VecSet<&'a str>,
}

impl<'a> DataDerivativeFormulaSetSeed<'a> {
    pub const fn new(variable: &'a str, dimensions: VecSet<&'a str>) -> Self {
        Self {
            variable,
            dimensions,
        }
    }
}

impl<'de> serde::de::DeserializeSeed<'de> for DataDerivativeFormulaSetSeed<'_> {
    type Value = SortedSet<NonEmpty<DataDerivative>>;

    fn deserialize<D: serde::Deserializer<'de>>(
        self,
        deserializer: D,
    ) -> Result<Self::Value, D::Error> {
        serde::Deserializer::deserialize_seq(deserializer, self)
    }
}

impl<'de> serde::de::Visitor<'de> for DataDerivativeFormulaSetSeed<'_> {
    type Value = SortedSet<NonEmpty<DataDerivative>>;

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("a set of data variable derivatives")
    }

    fn visit_seq<A: serde::de::SeqAccess<'de>>(self, mut seq: A) -> Result<Self::Value, A::Error> {
        let mut formulas = Vec::new();

        while let Some(formula) = seq.next_element_seed(DataDerivativeFormulaSeed {
            variable: self.variable,
            dimensions: &self.dimensions,
            integrated_dimensions: VecSet::with_capacity(self.dimensions.len()),
        })? {
            formulas.push(formula);
        }

        Ok(SortedSet::from_unsorted(formulas))
    }
}

struct DataDerivativeFormulaSeed<'a> {
    variable: &'a str,
    dimensions: &'a VecSet<&'a str>,
    integrated_dimensions: VecSet<String>,
}

impl<'de> serde::de::DeserializeSeed<'de> for DataDerivativeFormulaSeed<'_> {
    type Value = NonEmpty<DataDerivative>;

    fn deserialize<D: serde::Deserializer<'de>>(
        self,
        deserializer: D,
    ) -> Result<Self::Value, D::Error> {
        serde::Deserializer::deserialize_seq(deserializer, self)
    }
}

impl<'de> serde::de::Visitor<'de> for DataDerivativeFormulaSeed<'_> {
    type Value = NonEmpty<DataDerivative>;

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("a non-empty sequence of data variable derivatives")
    }

    fn visit_seq<A: serde::de::SeqAccess<'de>>(
        mut self,
        mut seq: A,
    ) -> Result<Self::Value, A::Error> {
        let Some(head) = seq.next_element_seed(DataDerivativeSeed {
            variable: self.variable,
            dimensions: self.dimensions,
            integrated_dimensions: &mut self.integrated_dimensions,
        })?
        else {
            return Err(serde::de::Error::custom(
                "expected at least one data variable derivative",
            ));
        };

        let mut tail = Vec::new();

        while let Some(elem) = seq.next_element_seed(DataDerivativeSeed {
            variable: self.variable,
            dimensions: self.dimensions,
            integrated_dimensions: &mut self.integrated_dimensions,
        })? {
            tail.push(elem);
        }

        Ok(NonEmpty { head, tail })
    }
}

struct DataDerivativeSeed<'a> {
    variable: &'a str,
    dimensions: &'a VecSet<&'a str>,
    integrated_dimensions: &'a mut VecSet<String>,
}

impl<'de> serde::de::DeserializeSeed<'de> for DataDerivativeSeed<'_> {
    type Value = DataDerivative;

    fn deserialize<D: serde::Deserializer<'de>>(
        self,
        deserializer: D,
    ) -> Result<Self::Value, D::Error> {
        serde::Deserializer::deserialize_struct(deserializer, "DataDerivative", METHODS, self)
    }
}

const METHODS: &[&str] = &["differentiate", "integrate"];

#[derive(Clone, Copy)]
enum Method {
    Differentiate,
    Integrate,
}

impl fmt::Display for Method {
    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Self::Differentiate => fmt.write_str("differentiate"),
            Self::Integrate => fmt.write_str("integrate"),
        }
    }
}

impl<'de> serde::de::Deserialize<'de> for Method {
    fn deserialize<D: serde::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        serde::Deserializer::deserialize_identifier(deserializer, MethodVisitor)
    }
}

struct MethodVisitor;

impl serde::de::Visitor<'_> for MethodVisitor {
    type Value = Method;

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("a data variable derivative method identifier")
    }

    fn visit_str<E: serde::de::Error>(self, value: &str) -> Result<Self::Value, E> {
        match value {
            "differentiate" => Ok(Method::Differentiate),
            "integrate" => Ok(Method::Integrate),
            _ => Err(serde::de::Error::unknown_field(value, METHODS)),
        }
    }

    fn visit_bytes<E: serde::de::Error>(self, value: &[u8]) -> Result<Self::Value, E> {
        match value {
            b"differentiate" => Ok(Method::Differentiate),
            b"integrate" => Ok(Method::Integrate),
            _ => {
                let value = String::from_utf8_lossy(value);
                Err(serde::de::Error::unknown_field(&value, METHODS))
            },
        }
    }
}

struct ExcessiveField;

impl<'de> serde::de::DeserializeSeed<'de> for ExcessiveField {
    type Value = Infallible;

    fn deserialize<D: serde::Deserializer<'de>>(
        self,
        deserializer: D,
    ) -> Result<Self::Value, D::Error> {
        serde::Deserializer::deserialize_identifier(deserializer, self)
    }
}

impl serde::de::Visitor<'_> for ExcessiveField {
    type Value = Infallible;

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("no more variable derivative fields")
    }

    fn visit_str<E: serde::de::Error>(self, value: &str) -> Result<Self::Value, E> {
        Err(serde::de::Error::unknown_field(value, &[]))
    }

    fn visit_bytes<E: serde::de::Error>(self, value: &[u8]) -> Result<Self::Value, E> {
        let value = String::from_utf8_lossy(value);
        Err(serde::de::Error::unknown_field(&value, &[]))
    }
}

struct DataDerivativeValueSeed<'a> {
    variable: &'a str,
    dimensions: &'a VecSet<&'a str>,
    integrated_dimensions: &'a mut VecSet<String>,
    method: Method,
}

impl<'de> serde::de::DeserializeSeed<'de> for DataDerivativeValueSeed<'_> {
    type Value = String;

    fn deserialize<D: serde::Deserializer<'de>>(
        self,
        deserializer: D,
    ) -> Result<Self::Value, D::Error> {
        deserializer.deserialize_str(self)
    }
}

impl serde::de::Visitor<'_> for DataDerivativeValueSeed<'_> {
    type Value = String;

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("a data dimension name string")
    }

    fn visit_str<E: serde::de::Error>(self, v: &str) -> Result<Self::Value, E> {
        if !self.dimensions.contains(v) {
            return Err(serde::de::Error::custom(format!(
                "variable {:?} does not have a dimension called {v:?} to {} over",
                self.variable, self.method
            )));
        }

        if self.integrated_dimensions.contains(v) {
            return Err(serde::de::Error::custom(format!(
                "{v:?} has already been integrated over for variable {:?}",
                self.variable
            )));
        }

        if matches!(self.method, Method::Integrate) {
            self.integrated_dimensions.insert(String::from(v));
        }

        Ok(String::from(v))
    }
}

impl<'de> serde::de::Visitor<'de> for DataDerivativeSeed<'_> {
    type Value = DataDerivative;

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("a data variable derivative")
    }

    fn visit_map<A: serde::de::MapAccess<'de>>(self, mut map: A) -> Result<Self::Value, A::Error> {
        let Some(method) = map.next_key()? else {
            return Err(serde::de::Error::custom(
                "a data variable derivative must have either a `differentiate` or an `integrate` \
                 field",
            ));
        };

        let value = map.next_value_seed(DataDerivativeValueSeed {
            variable: self.variable,
            dimensions: self.dimensions,
            integrated_dimensions: self.integrated_dimensions,
            method,
        })?;

        map.next_key_seed(ExcessiveField)?;

        match method {
            Method::Differentiate => Ok(DataDerivative::Differentiate {
                differentiate: value,
            }),
            Method::Integrate => Ok(DataDerivative::Integrate { integrate: value }),
        }
    }
}
