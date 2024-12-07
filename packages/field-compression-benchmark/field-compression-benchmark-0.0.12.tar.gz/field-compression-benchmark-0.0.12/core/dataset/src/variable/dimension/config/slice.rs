use std::{convert::Infallible, fmt, marker::PhantomData};

use core_error::pyerr_chain_from_location_err;
use pyo3::{intern, prelude::*, types::IntoPyDict, BoundObject};

use super::super::DataSlice;

pub struct PerVariableDataSlice<'a, 'py> {
    variable: &'a str,
    da: Borrowed<'a, 'py, PyAny>,
}

impl<'a, 'py> PerVariableDataSlice<'a, 'py> {
    #[must_use]
    pub const fn new(variable: &'a str, da: Borrowed<'a, 'py, PyAny>) -> Self {
        Self { variable, da }
    }
}

pub struct DataSliceSeed<'b, 'a, 'py> {
    py: Python<'py>,
    dimension: &'a str,
    per_variable: &'b [PerVariableDataSlice<'a, 'py>],
}

impl<'b, 'a, 'py> DataSliceSeed<'b, 'a, 'py> {
    #[must_use]
    pub const fn new(
        py: Python<'py>,
        dimension: &'a str,
        per_variable: &'b [PerVariableDataSlice<'a, 'py>],
    ) -> Self {
        Self {
            py,
            dimension,
            per_variable,
        }
    }
}

impl<'de> serde::de::DeserializeSeed<'de> for DataSliceSeed<'_, '_, '_> {
    type Value = DataSlice;

    fn deserialize<D: serde::Deserializer<'de>>(
        self,
        deserializer: D,
    ) -> Result<Self::Value, D::Error> {
        serde::Deserializer::deserialize_struct(deserializer, "DataDimension", FIELDS, self)
    }
}

const FIELDS: &[&str] = &["type", "value", "index", "valueset", "reduce"];

#[derive(Clone, Copy)]
enum Field {
    Type,
    Index,
    ValueSet,
}

impl<'de> serde::de::Deserialize<'de> for Field {
    fn deserialize<D: serde::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        serde::Deserializer::deserialize_identifier(deserializer, FieldVisitor)
    }
}

struct FieldVisitor;

impl serde::de::Visitor<'_> for FieldVisitor {
    type Value = Field;

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("a data dimension field identifier")
    }

    fn visit_str<E: serde::de::Error>(self, value: &str) -> Result<Self::Value, E> {
        match value {
            "type" => Ok(Field::Type),
            "index" => Ok(Field::Index),
            "valueset" => Ok(Field::ValueSet),
            _ => Err(serde::de::Error::custom(format!(
                "unexpected field `{value}`, a data dimension must start with either a `type`, \
                 `index`, or `valueset` field"
            ))),
        }
    }

    fn visit_bytes<E: serde::de::Error>(self, value: &[u8]) -> Result<Self::Value, E> {
        match value {
            b"type" => Ok(Field::Type),
            b"index" => Ok(Field::Index),
            b"valueset" => Ok(Field::ValueSet),
            _ => {
                let value = String::from_utf8_lossy(value);
                Err(serde::de::Error::custom(format!(
                    "unexpected field `{value}`, a data dimension must start with either a \
                     `type`, `index`, or `valueset` field"
                )))
            },
        }
    }
}

#[derive(Clone, Copy)]
enum ExtraField {
    Value,
    Reduce,
    Excessive,
}

impl<'de> serde::de::DeserializeSeed<'de> for ExtraField {
    type Value = ();

    fn deserialize<D: serde::Deserializer<'de>>(
        self,
        deserializer: D,
    ) -> Result<<Self as serde::de::DeserializeSeed<'de>>::Value, D::Error> {
        serde::Deserializer::deserialize_identifier(deserializer, self)
    }
}

impl<'de> serde::de::Visitor<'de> for ExtraField {
    type Value = ();

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("a data dimension field identifier")
    }

    fn visit_str<E: serde::de::Error>(
        self,
        value: &str,
    ) -> Result<<Self as serde::de::Visitor<'de>>::Value, E> {
        match (self, value) {
            (Self::Value, "value") | (Self::Reduce, "reduce") => Ok(()),
            _ => Err(serde::de::Error::unknown_field(
                value,
                match self {
                    Self::Value => &["value"],
                    Self::Reduce => &["reduce"],
                    Self::Excessive => &[],
                },
            )),
        }
    }

    fn visit_bytes<E: serde::de::Error>(
        self,
        value: &[u8],
    ) -> Result<<Self as serde::de::Visitor<'de>>::Value, E> {
        match (self, value) {
            (Self::Value, b"value") | (Self::Reduce, b"reduce") => Ok(()),
            _ => {
                let value = String::from_utf8_lossy(value);
                Err(serde::de::Error::unknown_field(
                    &value,
                    match self {
                        Self::Value => &["value"],
                        Self::Reduce => &["reduce"],
                        Self::Excessive => &[],
                    },
                ))
            },
        }
    }
}

#[derive(serde::Serialize, serde::Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum Type {
    Int,
    Float,
}

#[derive(Debug, serde::Serialize, serde::Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum ValueSet {
    All,
}

struct DataSliceValueSeed<
    'b,
    'a,
    'py,
    T: Copy + serde::de::DeserializeOwned + IntoPyObject<'py, Error = Infallible>,
> {
    py: Python<'py>,
    dimension: &'a str,
    ty: PhantomData<T>,
    is_index: bool,
    per_variable: &'b [PerVariableDataSlice<'a, 'py>],
}

impl<'py, 'de, T: Copy + serde::de::DeserializeOwned + IntoPyObject<'py, Error = Infallible>>
    serde::de::DeserializeSeed<'de> for DataSliceValueSeed<'_, '_, 'py, T>
{
    type Value = T;

    fn deserialize<D: serde::Deserializer<'de>>(
        self,
        deserializer: D,
    ) -> Result<Self::Value, D::Error> {
        let value = T::deserialize(deserializer)?;

        let selector: Bound<PyAny> = match value.into_pyobject(self.py) {
            Ok(selector) => selector.into_any().into_bound(),
            Err(err) => match err {},
        };

        for PerVariableDataSlice { variable, da } in self.per_variable {
            let selector = [(self.dimension, &selector)].into_py_dict(self.py);
            selector
                .and_then(|selector| {
                    da.call_method1(
                        if self.is_index {
                            intern!(self.py, "isel")
                        } else {
                            intern!(self.py, "sel")
                        },
                        (selector,),
                    )
                })
                .map_err(|err| {
                    let err = anyhow::Error::new(pyerr_chain_from_location_err(self.py, err))
                        .context(format!(
                            "failed to slice the variable {variable:?} along the dimension {:?}",
                            self.dimension,
                        ));
                    // we use anyhow here to format the full error chain
                    serde::de::Error::custom(format!("{err:#}"))
                })?;
        }

        Ok(value)
    }
}

impl<'de> serde::de::Visitor<'de> for DataSliceSeed<'_, '_, '_> {
    type Value = DataSlice;

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("a data dimension")
    }

    fn visit_map<A: serde::de::MapAccess<'de>>(self, mut map: A) -> Result<Self::Value, A::Error> {
        let Some(identifier) = map.next_key()? else {
            return Err(serde::de::Error::custom(
                "missing field, a data dimension must start with either a `type`, `index`, or \
                 `valueset` field",
            ));
        };

        let slice = match identifier {
            Field::Type => {
                let r#type = map.next_value()?;

                let Some(()) = map.next_key_seed(ExtraField::Value)? else {
                    return Err(serde::de::Error::missing_field("value"));
                };

                match r#type {
                    Type::Int => DataSlice::IntValue {
                        value: map.next_value_seed(DataSliceValueSeed {
                            py: self.py,
                            dimension: self.dimension,
                            ty: PhantomData::<i64>,
                            is_index: false,
                            per_variable: self.per_variable,
                        })?,
                    },
                    Type::Float => DataSlice::FloatValue {
                        value: map.next_value_seed(DataSliceValueSeed {
                            py: self.py,
                            dimension: self.dimension,
                            ty: PhantomData::<f64>,
                            is_index: false,
                            per_variable: self.per_variable,
                        })?,
                    },
                }
            },
            Field::Index => DataSlice::Index {
                index: map.next_value_seed(DataSliceValueSeed {
                    py: self.py,
                    dimension: self.dimension,
                    ty: PhantomData::<isize>,
                    is_index: true,
                    per_variable: self.per_variable,
                })?,
            },
            Field::ValueSet => {
                let ValueSet::All = map.next_value()?;

                let reduce = match map.next_key_seed(ExtraField::Reduce)? {
                    Some(()) => map.next_value()?,
                    None => false,
                };

                DataSlice::All { reduce }
            },
        };

        map.next_key_seed(ExtraField::Excessive)?;

        Ok(slice)
    }
}
