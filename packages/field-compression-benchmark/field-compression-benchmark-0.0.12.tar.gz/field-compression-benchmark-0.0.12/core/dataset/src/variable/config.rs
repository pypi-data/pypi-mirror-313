use std::fmt;

use core_error::pyerr_chain_from_location_err;
use nonempty::NonEmpty;
use pyo3::prelude::*;
use vecmap::{VecMap, VecSet};

use super::{
    derivative::DataDerivativeFormulaSetSeed,
    dimension::{DataDimensionsSeed, PerVariableDataDimension},
    DataVariable,
};

pub struct DataVariableSeed<'a, 'py> {
    py: Python<'py>,
    ds: Borrowed<'a, 'py, PyAny>,
    variables: &'a mut VecMap<String, DataVariable>,
    variables_seen: &'a mut VecSet<String>,
}

impl<'a, 'py> DataVariableSeed<'a, 'py> {
    #[must_use]
    pub fn new(
        py: Python<'py>,
        ds: Borrowed<'a, 'py, PyAny>,
        variables: &'a mut VecMap<String, DataVariable>,
        variables_seen: &'a mut VecSet<String>,
    ) -> Self {
        Self {
            py,
            ds,
            variables,
            variables_seen,
        }
    }
}

impl<'de> serde::de::DeserializeSeed<'de> for DataVariableSeed<'_, '_> {
    type Value = ();

    fn deserialize<D: serde::Deserializer<'de>>(
        self,
        deserializer: D,
    ) -> Result<Self::Value, D::Error> {
        serde::Deserializer::deserialize_struct(deserializer, "DataVariable", FIELDS, self)
    }
}

const FIELDS: &[&str] = &["name", "names", "dimensions", "derivatives"];

#[derive(Clone, Copy)]
enum NameField {
    Name,
    Names,
}

impl<'de> serde::de::Deserialize<'de> for NameField {
    fn deserialize<D: serde::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        serde::Deserializer::deserialize_identifier(deserializer, NameFieldVisitor)
    }
}

struct NameFieldVisitor;

impl serde::de::Visitor<'_> for NameFieldVisitor {
    type Value = NameField;

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("a data variable field identifier")
    }

    fn visit_str<E: serde::de::Error>(self, value: &str) -> Result<Self::Value, E> {
        match value {
            "name" => Ok(NameField::Name),
            "names" => Ok(NameField::Names),
            _ => Err(serde::de::Error::custom(format!(
                "unexpected field `{value}`, a data variable must start with either a `name` or \
                 `names` field"
            ))),
        }
    }

    fn visit_bytes<E: serde::de::Error>(self, value: &[u8]) -> Result<Self::Value, E> {
        match value {
            b"name" => Ok(NameField::Name),
            b"names" => Ok(NameField::Names),
            _ => {
                let value = String::from_utf8_lossy(value);
                Err(serde::de::Error::custom(format!(
                    "unexpected field `{value}`, a data variable must start with either a `name` \
                     or `names` field"
                )))
            },
        }
    }
}

#[derive(Clone, Copy)]
enum ExtraField {
    Dimensions,
    Derivatives,
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
        formatter.write_str("a data variable field identifier")
    }

    fn visit_str<E: serde::de::Error>(
        self,
        value: &str,
    ) -> Result<<Self as serde::de::Visitor<'de>>::Value, E> {
        match (self, value) {
            (Self::Dimensions, "dimensions") | (Self::Derivatives, "derivatives") => Ok(()),
            _ => Err(serde::de::Error::unknown_field(
                value,
                match self {
                    Self::Dimensions => &["dimensions"],
                    Self::Derivatives => &["derivatives"],
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
            (Self::Dimensions, b"dimensions") | (Self::Derivatives, b"derivatives") => Ok(()),
            _ => {
                let value = String::from_utf8_lossy(value);
                Err(serde::de::Error::unknown_field(
                    &value,
                    match self {
                        Self::Dimensions => &["dimensions"],
                        Self::Derivatives => &["derivatives"],
                        Self::Excessive => &[],
                    },
                ))
            },
        }
    }
}

struct DataVariableNameSeed<'a, 'py> {
    ds: Borrowed<'a, 'py, PyAny>,
    variables: &'a VecMap<String, DataVariable>,
    variables_seen: &'a mut VecSet<String>,
}

impl<'py, 'de> serde::de::DeserializeSeed<'de> for DataVariableNameSeed<'_, 'py> {
    type Value = (String, Bound<'py, PyAny>);

    fn deserialize<D: serde::Deserializer<'de>>(
        self,
        deserializer: D,
    ) -> Result<Self::Value, D::Error> {
        serde::Deserializer::deserialize_str(deserializer, self)
    }
}

impl<'py> serde::de::Visitor<'_> for DataVariableNameSeed<'_, 'py> {
    type Value = (String, Bound<'py, PyAny>);

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("a data variable name string")
    }

    fn visit_str<E: serde::de::Error>(self, v: &str) -> Result<Self::Value, E> {
        if self.variables.get(v).is_none() {
            return Err(serde::de::Error::custom(format!(
                "dataset does not contain a variable called {v:?}"
            )));
        };

        if !self.variables_seen.insert(String::from(v)) {
            return Err(serde::de::Error::custom(format!(
                "duplicate variable name {v:?}"
            )));
        }

        let da = self.ds.get_item(v).map_err(|err| {
            let err = anyhow::Error::new(pyerr_chain_from_location_err(self.ds.py(), err))
                .context(format!("failed to load the variable {v:?}"));
            // we use anyhow here to format the full error chain
            serde::de::Error::custom(format!("{err:#}"))
        })?;

        Ok((String::from(v), da))
    }
}

struct DataVariableNameListSeed<'a, 'py> {
    ds: Borrowed<'a, 'py, PyAny>,
    variables: &'a VecMap<String, DataVariable>,
    variables_seen: &'a mut VecSet<String>,
}

impl<'py, 'de> serde::de::DeserializeSeed<'de> for DataVariableNameListSeed<'_, 'py> {
    type Value = NonEmpty<(String, Bound<'py, PyAny>)>;

    fn deserialize<D: serde::Deserializer<'de>>(
        self,
        deserializer: D,
    ) -> Result<Self::Value, D::Error> {
        serde::Deserializer::deserialize_seq(deserializer, self)
    }
}

impl<'py, 'de> serde::de::Visitor<'de> for DataVariableNameListSeed<'_, 'py> {
    type Value = NonEmpty<(String, Bound<'py, PyAny>)>;

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("a list of data variable name strings")
    }

    fn visit_seq<A: serde::de::SeqAccess<'de>>(self, mut seq: A) -> Result<Self::Value, A::Error> {
        let Some(head) = seq.next_element_seed(DataVariableNameSeed {
            ds: self.ds,
            variables: self.variables,
            variables_seen: self.variables_seen,
        })?
        else {
            return Err(serde::de::Error::custom(
                "expected at least one data variable name",
            ));
        };

        let mut tail = Vec::new();

        while let Some(elem) = seq.next_element_seed(DataVariableNameSeed {
            ds: self.ds,
            variables: self.variables,
            variables_seen: self.variables_seen,
        })? {
            tail.push(elem);
        }

        Ok(NonEmpty { head, tail })
    }
}

impl<'de> serde::de::Visitor<'de> for DataVariableSeed<'_, '_> {
    type Value = ();

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("a data variable")
    }

    fn visit_map<A: serde::de::MapAccess<'de>>(self, mut map: A) -> Result<Self::Value, A::Error> {
        let Some(name) = map.next_key()? else {
            return Err(serde::de::Error::custom(
                "missing field, a data variable must start with either a `name` or `names` field",
            ));
        };

        let variables = match name {
            NameField::Name => NonEmpty {
                head: map.next_value_seed(DataVariableNameSeed {
                    ds: self.ds,
                    variables: self.variables,
                    variables_seen: self.variables_seen,
                })?,
                tail: Vec::new(),
            },
            NameField::Names => map.next_value_seed(DataVariableNameListSeed {
                ds: self.ds,
                variables: self.variables,
                variables_seen: self.variables_seen,
            })?,
        };

        let Some(()) = map.next_key_seed(ExtraField::Derivatives)? else {
            return Err(serde::de::Error::missing_field("derivatives"));
        };

        // Since the data derivatives are common for all variables we're parsing
        // right now, we only need to check them for one of them
        let Some((name, variable)) = self.variables.get_key_value(&variables.head.0) else {
            return Err(serde::de::Error::custom(
                "BUG: dataset does not contain pre-checked variable (b)",
            ));
        };

        let data_derivatives = map.next_value_seed(DataDerivativeFormulaSetSeed::new(
            name,
            variable
                .dimensions
                .keys()
                .map(|dim_name| &**dim_name)
                .collect(),
        ))?;

        let Some(()) = map.next_key_seed(ExtraField::Dimensions)? else {
            return Err(serde::de::Error::missing_field("dimensions"));
        };

        // Since each variable could have the same dimensions name- and slicing-wise
        // but have a different size, we only deserialize the common slices but check
        // them against all variables
        let data_slices = map.next_value_seed(DataDimensionsSeed::new(
            self.py,
            variables
                .iter()
                .map(|(name, da)| {
                    self.variables
                        .get(name)
                        .map(|variable| {
                            PerVariableDataDimension::new(
                                da.as_borrowed(),
                                name,
                                &variable.dimensions,
                            )
                        })
                        .ok_or_else(|| {
                            serde::de::Error::custom(
                                "BUG: dataset does not contain pre-checked variable (a)",
                            )
                        })
                })
                .collect::<Result<_, _>>()?,
        ))?;

        map.next_key_seed(ExtraField::Excessive)?;

        // Now the per-variable data dimensions can be updated with the common slices
        for (name, _) in &variables {
            let Some(variable) = self.variables.get_mut(name) else {
                return Err(serde::de::Error::custom(
                    "BUG: dataset does not contain pre-checked variable (c)",
                ));
            };

            for (dim_name, dimension) in &mut variable.dimensions {
                let Some(slice) = data_slices.get(dim_name) else {
                    return Err(serde::de::Error::custom(
                        "BUG: variable does not contain pre-checked dimension",
                    ));
                };

                dimension.slice = slice.clone();
            }

            variable.derivatives = data_derivatives.clone();
        }

        Ok(())
    }
}
