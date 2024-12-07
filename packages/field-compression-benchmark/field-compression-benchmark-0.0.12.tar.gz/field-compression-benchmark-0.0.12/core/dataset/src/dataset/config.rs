use std::{
    fmt,
    path::{Path, PathBuf},
};

use core_error::pyerr_chain_from_location_err;
use pyo3::prelude::*;
use vecmap::{VecMap, VecSet};

use crate::{
    dataset::{open_xarray_dataset, Dataset, DatasetSettings},
    units::UnitRegistry,
    variable::{DataVariable, DataVariableSeed},
};

pub struct DatasetSeed<'a, 'py> {
    py: Python<'py>,
    config_path: Option<&'a Path>,
    unit_registry: Borrowed<'a, 'py, UnitRegistry>,
    settings: &'a DatasetSettings,
}

impl<'a, 'py> DatasetSeed<'a, 'py> {
    pub const fn new(
        py: Python<'py>,
        config_path: Option<&'a Path>,
        unit_registry: Borrowed<'a, 'py, UnitRegistry>,
        settings: &'a DatasetSettings,
    ) -> Self {
        Self {
            py,
            config_path,
            unit_registry,
            settings,
        }
    }
}

impl<'de> serde::de::DeserializeSeed<'de> for DatasetSeed<'_, '_> {
    type Value = Dataset;

    fn deserialize<D: serde::Deserializer<'de>>(
        self,
        deserializer: D,
    ) -> Result<Self::Value, D::Error> {
        serde::Deserializer::deserialize_struct(deserializer, "Dataset", FIELDS, self)
    }
}

const FIELDS: &[&str] = &["path", "format", "variable", "variables"];

#[derive(Copy, Clone)]
enum Field {
    Path,
    Format,
    Variables,
    Excessive,
}

impl<'de> serde::de::DeserializeSeed<'de> for Field {
    type Value = ();

    fn deserialize<D: serde::Deserializer<'de>>(
        self,
        deserializer: D,
    ) -> Result<Self::Value, D::Error> {
        serde::Deserializer::deserialize_identifier(deserializer, self)
    }
}

impl serde::de::Visitor<'_> for Field {
    type Value = ();

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("a dataset config field identifier")
    }

    fn visit_str<E: serde::de::Error>(self, value: &str) -> Result<Self::Value, E> {
        match (self, value) {
            (Self::Path, "path")
            | (Self::Format, "format")
            | (Self::Variables, "variable" | "variables") => Ok(()),
            _ => Err(serde::de::Error::unknown_field(
                value,
                match self {
                    Self::Path => &["path"],
                    Self::Format => &["format"],
                    Self::Variables => &["variable", "variables"],
                    Self::Excessive => &[],
                },
            )),
        }
    }

    fn visit_bytes<E: serde::de::Error>(self, value: &[u8]) -> Result<Self::Value, E> {
        match (self, value) {
            (Self::Path, b"path")
            | (Self::Format, b"format")
            | (Self::Variables, b"variable" | b"variables") => Ok(()),
            _ => {
                let value = String::from_utf8_lossy(value);
                Err(serde::de::Error::unknown_field(
                    &value,
                    match self {
                        Self::Path => &["path"],
                        Self::Format => &["format"],
                        Self::Variables => &["variable", "variables"],
                        Self::Excessive => &[],
                    },
                ))
            },
        }
    }
}

struct DatasetVariablesSeed<'a, 'py> {
    py: Python<'py>,
    ds: Borrowed<'a, 'py, PyAny>,
    variables: VecMap<String, DataVariable>,
    ignored_variables: VecSet<String>,
    variables_seen: VecSet<String>,
}

impl<'de> serde::de::DeserializeSeed<'de> for DatasetVariablesSeed<'_, '_> {
    type Value = (VecMap<String, DataVariable>, VecSet<String>);

    fn deserialize<D: serde::Deserializer<'de>>(
        self,
        deserializer: D,
    ) -> Result<Self::Value, D::Error> {
        deserializer.deserialize_seq(self)
    }
}

impl<'de> serde::de::Visitor<'de> for DatasetVariablesSeed<'_, '_> {
    type Value = (VecMap<String, DataVariable>, VecSet<String>);

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("a sequence of variables")
    }

    fn visit_seq<A: serde::de::SeqAccess<'de>>(
        mut self,
        mut seq: A,
    ) -> Result<Self::Value, A::Error> {
        #[expect(clippy::equatable_if_let)]
        while let Some(()) = seq.next_element_seed(DataVariableSeed::new(
            self.py,
            self.ds,
            &mut self.variables,
            &mut self.variables_seen,
        ))? {
            // no-op
        }

        let mut index = 0;
        while let Some((variable, _)) = self.variables.get_index(index) {
            if self.variables_seen.contains(variable) {
                index += 1;
            } else {
                let (variable, _) = self.variables.swap_remove_index(index);
                self.ignored_variables.insert(variable);
            }
        }

        Ok((self.variables, self.ignored_variables))
    }
}

impl<'de> serde::de::Visitor<'de> for DatasetSeed<'_, '_> {
    type Value = Dataset;

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("a dataset config")
    }

    fn visit_map<A: serde::de::MapAccess<'de>>(self, mut map: A) -> Result<Self::Value, A::Error> {
        let Some(()) = map.next_key_seed(Field::Path)? else {
            return Err(serde::de::Error::missing_field("path"));
        };
        let path: PathBuf = map.next_value()?;

        let Some(()) = map.next_key_seed(Field::Format)? else {
            return Err(serde::de::Error::missing_field("format"));
        };
        let format = map.next_value()?;

        let path = match self.config_path.and_then(Path::parent) {
            None => path,
            Some(parent) => parent.join(path),
        };

        let ds = open_xarray_dataset(self.py, &path, format, self.settings.auto_chunk_size)
            .map_err(|err| {
                let err = anyhow::Error::new(pyerr_chain_from_location_err(self.py, err))
                    .context("failed to load the dataset");
                // we use anyhow here to format the full error chain
                serde::de::Error::custom(format!("{err:#}"))
            })?;
        let variables: VecMap<String, DataVariable> =
            DataVariable::extract_from_dataset(self.py, ds.as_borrowed(), self.unit_registry)
                .map_err(|err| {
                    let err = anyhow::Error::new(pyerr_chain_from_location_err(self.py, err))
                        .context("failed to extract the dataset variables");
                    // we use anyhow here to format the full error chain
                    serde::de::Error::custom(format!("{err:#}"))
                })?;

        let Some(()) = map.next_key_seed(Field::Variables)? else {
            return Err(serde::de::Error::missing_field("variables"));
        };
        let (variables, ignored_variables) = map.next_value_seed(DatasetVariablesSeed {
            py: self.py,
            ds: ds.as_borrowed(),
            variables_seen: VecSet::with_capacity(variables.len()),
            variables,
            ignored_variables: VecSet::new(),
        })?;

        map.next_key_seed(Field::Excessive)?;

        Ok(Dataset {
            config_path: self.config_path.map(Path::to_path_buf),
            path,
            format,
            variables,
            ignored_variables,
            settings: self.settings.clone(),
        })
    }
}
