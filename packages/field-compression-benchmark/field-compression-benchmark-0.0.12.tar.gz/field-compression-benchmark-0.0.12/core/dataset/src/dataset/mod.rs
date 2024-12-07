use std::{
    fmt, fs,
    path::{Path, PathBuf},
};

use byte_unit::Byte;
use pyo3::{
    intern,
    prelude::*,
    sync::GILOnceCell,
    types::{IntoPyDict, PyDict},
};
use thiserror::Error;
use vecmap::{VecMap, VecSet};

use core_error::LocationError;

mod config;

use self::config::DatasetSeed;
use crate::{units::UnitRegistry, variable::DataVariable};

#[derive(Debug, Clone)]
pub struct Dataset {
    config_path: Option<PathBuf>,
    path: PathBuf,
    format: DatasetFormat,
    variables: VecMap<String, DataVariable>,
    ignored_variables: VecSet<String>,
    settings: DatasetSettings,
}

impl Dataset {
    pub fn from_deserialised_config<'a, 'py, 'de, D: serde::Deserializer<'de>>(
        py: Python<'py>,
        deserializer: D,
        unit_registry: Borrowed<'_, 'py, UnitRegistry>,
        settings: &DatasetSettings,
    ) -> Result<Self, D::Error> {
        serde::de::DeserializeSeed::deserialize(
            DatasetSeed::new(py, None, unit_registry, settings),
            deserializer,
        )
    }

    pub fn from_config_str<'py>(
        py: Python<'py>,
        config: &str,
        unit_registry: Borrowed<'_, 'py, UnitRegistry>,
        settings: &DatasetSettings,
    ) -> Result<Self, LocationError<ParseDatasetError>> {
        Self::from_deserialised_config(py, toml::Deserializer::new(config), unit_registry, settings)
            .map_err(|err| ParseDatasetError::ParseConfig { source: err })
            .map_err(LocationError::new)
    }

    pub fn from_config_file<'py>(
        py: Python<'py>,
        config_file: &Path,
        unit_registry: Borrowed<'_, 'py, UnitRegistry>,
        settings: &DatasetSettings,
    ) -> Result<Self, LocationError<ParseDatasetError>> {
        let config =
            fs::read_to_string(config_file).map_err(|err| ParseDatasetError::ReadFile {
                source: err,
                file: config_file.to_path_buf(),
            })?;

        serde::de::DeserializeSeed::deserialize(
            DatasetSeed::new(py, Some(config_file), unit_registry, settings),
            toml::Deserializer::new(&config),
        )
        .map_err(|err| ParseDatasetError::ParseConfigFile {
            source: err,
            file: config_file.to_path_buf(),
        })
        .map_err(LocationError::new)
    }

    pub fn from_config_files<'py>(
        py: Python<'py>,
        config_files: &VecSet<PathBuf>,
        unit_registry: Borrowed<'_, 'py, UnitRegistry>,
        settings: &DatasetSettings,
    ) -> Result<VecMap<PathBuf, Self>, LocationError<ParseDatasetError>> {
        let mut datasets = VecMap::with_capacity(config_files.len());

        for path in config_files {
            let dataset = Self::from_config_file(py, path, unit_registry, settings)?;

            datasets.insert(path.clone(), dataset);
        }

        Ok(datasets)
    }

    pub fn from_config_directory<'py>(
        py: Python<'py>,
        config_directory: &Path,
        unit_registry: Borrowed<'_, 'py, UnitRegistry>,
        settings: &DatasetSettings,
    ) -> Result<VecMap<PathBuf, Self>, LocationError<ParseDatasetError>> {
        let mut config_files = VecSet::new();

        for path in
            fs::read_dir(config_directory).map_err(|err| ParseDatasetError::ReadDirectory {
                source: err,
                directory: config_directory.to_path_buf(),
            })?
        {
            let path = path
                .map_err(|err| ParseDatasetError::QueryFile {
                    source: err,
                    directory: config_directory.to_path_buf(),
                })?
                .path();

            if !matches!(path.extension(), Some(ext) if ext == "toml") {
                // Skip all non-config files in the directory
                continue;
            }

            config_files.insert(path);
        }

        Self::from_config_files(py, &config_files, unit_registry, settings)
    }

    #[must_use]
    pub fn config_path(&self) -> Option<&Path> {
        self.config_path.as_deref()
    }

    #[must_use]
    pub fn path(&self) -> &Path {
        &self.path
    }

    #[must_use]
    pub const fn format(&self) -> DatasetFormat {
        self.format
    }

    #[must_use]
    pub fn variables(&self) -> impl ExactSizeIterator<Item = &DataVariable> {
        self.variables.values()
    }

    #[must_use]
    pub fn get_variable(&self, name: &str) -> Option<&DataVariable> {
        self.variables.get(name)
    }

    #[must_use]
    pub fn ignored_variables(&self) -> impl ExactSizeIterator<Item = &str> {
        self.ignored_variables.iter().map(|variable| &**variable)
    }

    pub fn open_xarray<'py>(
        &self,
        py: Python<'py>,
    ) -> Result<Bound<'py, PyAny>, LocationError<PyErr>> {
        open_xarray_dataset(py, &self.path, self.format, self.settings.auto_chunk_size)
    }

    pub fn open_xarray_sliced_variable<'py>(
        &self,
        py: Python<'py>,
        variable: &DataVariable,
    ) -> Result<Bound<'py, PyAny>, LocationError<PyErr>> {
        let dataset = self.open_xarray(py)?;
        let mut data_array = dataset.get_item(variable.name())?;

        for (dim_name, dimension) in variable.dimensions() {
            data_array = dimension
                .slice()
                .sel(py, data_array.as_borrowed(), dim_name)?;
        }

        Ok(data_array)
    }

    pub fn minimise(&mut self, variables: bool, dimensions: bool, derivatives: bool) {
        if variables && self.variables.len() > 1 {
            self.ignored_variables
                .extend(self.variables.drain(1..).map(|(k, _v)| k));
        }

        self.variables
            .values_mut()
            .for_each(|variable| variable.minimise(dimensions, derivatives));
    }

    pub fn filter(&mut self, mut keep_variable: impl FnMut(&str) -> bool) {
        self.variables.retain(|name, _| {
            let keep = keep_variable(name);
            if !keep {
                self.ignored_variables.insert(String::from(name));
            }
            keep
        });
    }
}

#[derive(Copy, Clone, Debug, PartialEq, Eq, Hash, serde::Serialize, serde::Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum DatasetFormat {
    #[serde(alias = "GRIB")]
    GRIB,
    #[serde(alias = "NetCDF4", alias = "NetCDF", alias = "netcdf")]
    NetCDF4,
    #[serde(alias = "Zarr")]
    Zarr,
}

impl fmt::Display for DatasetFormat {
    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Self::GRIB => fmt.write_str("GRIB"),
            Self::NetCDF4 => fmt.write_str("NetCDF4"),
            Self::Zarr => fmt.write_str("Zarr"),
        }
    }
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
#[serde(default)]
pub struct DatasetSettings {
    pub auto_chunk_size: Byte,
}

impl Default for DatasetSettings {
    fn default() -> Self {
        Self {
            auto_chunk_size: Byte::from(Byte::MEBIBYTE.as_u64() * 32),
        }
    }
}

#[derive(Debug, Error)]
pub enum ParseDatasetError {
    #[error("failed to read the dataset directory {directory:?}")]
    ReadDirectory {
        source: std::io::Error,
        directory: PathBuf,
    },
    #[error("failed to query a dataset config file in {directory:?}")]
    QueryFile {
        source: std::io::Error,
        directory: PathBuf,
    },
    #[error("failed to read the dataset config file {file:?}")]
    ReadFile {
        source: std::io::Error,
        file: PathBuf,
    },
    #[error("failed to parse the dataset config")]
    ParseConfig { source: toml::de::Error },
    #[error("failed to parse the dataset config file {file:?}")]
    ParseConfigFile {
        source: toml::de::Error,
        file: PathBuf,
    },
}

fn open_xarray_dataset<'py>(
    py: Python<'py>,
    path: &Path,
    format: DatasetFormat,
    auto_chunk_size: Byte,
) -> Result<Bound<'py, PyAny>, LocationError<PyErr>> {
    static XARRAY_OPEN_DATASET: GILOnceCell<Py<PyAny>> = GILOnceCell::new();
    static DASK_CONFIG_SET: GILOnceCell<Py<PyAny>> = GILOnceCell::new();

    let kwargs = PyDict::new(py);
    let engine = intern!(py, "engine");

    match format {
        DatasetFormat::GRIB => {
            kwargs.set_item(engine, intern!(py, "cfgrib"))?;
            kwargs.set_item(
                intern!(py, "backend_kwargs"),
                [(intern!(py, "indexpath"), intern!(py, ""))].into_py_dict(py)?,
            )?;
        },
        DatasetFormat::NetCDF4 => {
            kwargs.set_item(engine, intern!(py, "netcdf4"))?;
        },
        DatasetFormat::Zarr => {
            kwargs.set_item(engine, intern!(py, "zarr"))?;
        },
    };

    kwargs.set_item(intern!(py, "chunks"), intern!(py, "auto"))?;
    kwargs.set_item(intern!(py, "cache"), false)?;

    let context = DASK_CONFIG_SET.import(py, "dask.config", "set")?.call(
        (),
        Some(&[(intern!(py, "array.chunk-size"), auto_chunk_size.as_u128())].into_py_dict(py)?),
    )?;

    // Load the dataset using the auto chunking with the given chunk size
    context.call_method0(intern!(py, "__enter__"))?;
    let dataset = XARRAY_OPEN_DATASET
        .import(py, "xarray", "open_dataset")?
        .call((path,), Some(&kwargs))?
        .call_method0(intern!(py, "unify_chunks"))
        .map_err(LocationError::new);
    context.call_method1(
        intern!(py, "__exit__"),
        (Option::<()>::None, Option::<()>::None, Option::<()>::None),
    )?;

    dataset
}
