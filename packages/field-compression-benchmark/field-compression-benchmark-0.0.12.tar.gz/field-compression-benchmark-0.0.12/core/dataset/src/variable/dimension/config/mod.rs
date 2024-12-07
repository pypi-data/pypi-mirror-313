use std::fmt;

use pyo3::prelude::*;
use vecmap::{VecMap, VecSet};

use self::slice::PerVariableDataSlice;

use super::{DataDimension, DataSlice};

pub mod slice;

use slice::DataSliceSeed;

pub struct PerVariableDataDimension<'a, 'py> {
    da: Borrowed<'a, 'py, PyAny>,
    variable: &'a str,
    dimensions: &'a VecMap<String, DataDimension>,
    dimensions_seen: VecSet<String>,
}

impl<'a, 'py> PerVariableDataDimension<'a, 'py> {
    #[must_use]
    pub fn new(
        da: Borrowed<'a, 'py, PyAny>,
        variable: &'a str,
        dimensions: &'a VecMap<String, DataDimension>,
    ) -> Self {
        Self {
            da,
            variable,
            dimensions_seen: VecSet::with_capacity(dimensions.len()),
            dimensions,
        }
    }
}

pub struct DataDimensionsSeed<'a, 'py> {
    py: Python<'py>,
    per_variable: Vec<PerVariableDataDimension<'a, 'py>>,
}

impl<'a, 'py> DataDimensionsSeed<'a, 'py> {
    #[must_use]
    pub const fn new(
        py: Python<'py>,
        per_variable: Vec<PerVariableDataDimension<'a, 'py>>,
    ) -> Self {
        Self { py, per_variable }
    }
}

impl<'de> serde::de::DeserializeSeed<'de> for DataDimensionsSeed<'_, '_> {
    type Value = VecMap<String, DataSlice>;

    fn deserialize<D: serde::Deserializer<'de>>(
        self,
        deserializer: D,
    ) -> Result<Self::Value, D::Error> {
        serde::Deserializer::deserialize_map(deserializer, self)
    }
}

struct DataDimensionNameSeed<'b, 'a, 'py> {
    per_variable: &'b mut [PerVariableDataDimension<'a, 'py>],
}

impl<'de> serde::de::DeserializeSeed<'de> for DataDimensionNameSeed<'_, '_, '_> {
    type Value = String;

    fn deserialize<D: serde::Deserializer<'de>>(
        self,
        deserializer: D,
    ) -> Result<Self::Value, D::Error> {
        serde::de::Deserializer::deserialize_str(deserializer, self)
    }
}

impl serde::de::Visitor<'_> for DataDimensionNameSeed<'_, '_, '_> {
    type Value = String;

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("a data dimension name string")
    }

    fn visit_str<E: serde::de::Error>(self, v: &str) -> Result<Self::Value, E> {
        for PerVariableDataDimension {
            variable,
            dimensions,
            dimensions_seen,
            ..
        } in self.per_variable
        {
            if dimensions.get(v).is_none() {
                return Err(serde::de::Error::custom(format!(
                    "variable {variable:?} does not have a dimension called {v:?}"
                )));
            };

            if !dimensions_seen.insert(String::from(v)) {
                return Err(serde::de::Error::custom(format!(
                    "duplicate dimension {v:?} for variable {variable:?}"
                )));
            }
        }

        Ok(String::from(v))
    }
}

impl<'de> serde::de::Visitor<'de> for DataDimensionsSeed<'_, '_> {
    type Value = VecMap<String, DataSlice>;

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("a map of the variable's dimensions")
    }

    fn visit_map<A: serde::de::MapAccess<'de>>(
        mut self,
        mut map: A,
    ) -> Result<Self::Value, A::Error> {
        let per_variable_slice = self
            .per_variable
            .iter()
            .map(|variable| PerVariableDataSlice::new(variable.variable, variable.da))
            .collect::<Vec<_>>();

        let mut data_slices = VecMap::with_capacity(map.size_hint().unwrap_or(0));

        while let Some(dim_name) = map.next_key_seed(DataDimensionNameSeed {
            per_variable: &mut self.per_variable,
        })? {
            let slice =
                map.next_value_seed(DataSliceSeed::new(self.py, &dim_name, &per_variable_slice))?;

            data_slices.insert(dim_name, slice);
        }

        for PerVariableDataDimension {
            variable,
            dimensions,
            dimensions_seen,
            ..
        } in self.per_variable
        {
            for dim_name in dimensions.keys() {
                if !dimensions_seen.contains(dim_name) {
                    return Err(serde::de::Error::custom(format!(
                        "variable {variable:?} has a dimension {dim_name:?} but it is missing here"
                    )));
                }
            }
        }

        Ok(data_slices)
    }
}
