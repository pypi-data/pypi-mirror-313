use std::{iter::FusedIterator, path::PathBuf};

use pyo3::{intern, prelude::*};
use pyo3_error::PyErrChain;
use thiserror::Error;
use vecmap::{VecMap, VecSet};

use core_benchmark::case::BenchmarkCaseFilter;
use core_compressor::{
    compressor::{Compressor, ParseCompressorError},
    parameter::ParameterEvalError,
};
use core_dataset::{
    dataset::{Dataset, DatasetSettings, ParseDatasetError},
    units::{UnitExpression, UnitRegistry, UnitRegistryMethods},
    variable::{derivative::DataDerivative, dimension::DataSlice},
};
use core_error::{pyerr_chain_from_location_err, LocationError};

use crate::args::Minimal;

pub struct Benchmark {
    compressors: VecMap<String, Compressor>,
    datasets: VecMap<PathBuf, Dataset>,
}

impl Benchmark {
    #[expect(clippy::too_many_lines)] // FIXME
    pub fn prepare(
        py: Python,
        mut compressors: VecSet<PathBuf>,
        mut datasets: VecSet<PathBuf>,
        minimal: &Minimal,
        case_filter: Option<&BenchmarkCaseFilter>,
        dataset_settings: &DatasetSettings,
    ) -> Result<Self, LocationError<BenchmarkPrepareError>> {
        println!("- Loading the SI unit registry");

        let unit_registry = Bound::<UnitRegistry>::try_new(py)
            .map_err(|err| err.map(|err| pyerr_chain_from_location_err(py, err)))
            .map_err(BenchmarkPrepareError::UnitRegistry)?;

        println!("- Parsing the compressor configuration files");

        if let Some(case_filter) = case_filter {
            datasets.retain(|dataset| case_filter.contains_dataset(dataset));
            compressors.retain(|compressor| case_filter.contains_compressor(compressor));
        }

        let mut compressors = Compressor::from_config_files(py, &compressors)
            .map_err(BenchmarkPrepareError::Compressor)?;

        if minimal.codec_parameters {
            compressors.values_mut().for_each(Compressor::minimise);
        }

        for compressor in compressors.values() {
            compressor
                .ensure_py_imports(py)
                .map_err(|err| err.map(|err| pyerr_chain_from_location_err(py, err)))
                .map_err(BenchmarkPrepareError::CodecImport)?;

            println!("  - {compressor}");
        }

        println!("- Parsing the dataset configuration files");

        let mut datasets = Dataset::from_config_files(
            py,
            &datasets,
            unit_registry.as_borrowed(),
            dataset_settings,
        )
        .map_err(BenchmarkPrepareError::Dataset)?;

        datasets.values_mut().for_each(|dataset: &mut Dataset| {
            dataset.minimise(
                minimal.dataset_variables,
                minimal.variable_dimensions,
                minimal.variable_derivatives,
            );

            if let Some(case_filter) = case_filter {
                dataset.filter(|variable| case_filter.contains_variable(variable));
            }
        });

        for dataset in datasets.values() {
            let dataset: &Dataset = dataset;

            println!("  - {:?}", dataset.path());
            println!("    - format: {:?}", dataset.format());

            if dataset.variables().len() > 0 {
                println!("    - variables:");

                for variable in dataset.variables() {
                    println!("      - {}:", variable.name());

                    if let Some(long_name) = variable.long_name() {
                        println!("        - long name: {long_name}");
                    }
                    if let Some(units) = variable.units() {
                        println!(
                            "        - units: {}  =  {}",
                            UnitExpression::as_ascii(units.verbose().expression()),
                            UnitExpression::as_ascii(units.base().expression())
                        );
                    }
                    println!("        - dtype: {}", variable.dtype());

                    println!("        - dimensions:");
                    for (name, dimension) in variable.dimensions() {
                        print!("          - {name}");
                        match dimension.slice() {
                            DataSlice::IntValue { value } => {
                                println!(" = {value} (of {} values)", dimension.size());
                            },
                            DataSlice::FloatValue { value } => {
                                println!(" = {value} (of {} values)", dimension.size());
                            },
                            DataSlice::Index { index } => {
                                println!(" = {name}[{index}] (of {} values)", dimension.size());
                            },
                            DataSlice::All { reduce: false } => {
                                println!(": all {} values", dimension.size());
                            },
                            DataSlice::All { reduce: true } => {
                                println!(": reduce over {} values", dimension.size());
                            },
                        };
                    }

                    println!("        - derivatives:");
                    println!("          - {}", variable.name());
                    for derivatives in variable.derivatives().iter() {
                        print!("          - {}", variable.name());
                        for derivative in derivatives {
                            match derivative {
                                DataDerivative::Differentiate { differentiate } => {
                                    print!(" ∂ {differentiate}");
                                },
                                DataDerivative::Integrate { integrate } => print!(" ∫ {integrate}"),
                            }
                        }
                        println!();
                    }
                }
            }

            if dataset.ignored_variables().len() > 0 {
                println!("    - ignored variables:");

                for variable in dataset.ignored_variables() {
                    println!("      - {variable}");
                }
            }
        }

        println!();

        Ok(Self {
            compressors,
            datasets,
        })
    }

    pub fn prepare_python(py: Python) -> Result<(), LocationError<PyErr>> {
        let py_version: String = py.import("sys")?.getattr("version")?.extract()?;

        println!("Initialising the benchmark for Python {py_version}");

        let __version__ = intern!(py, "__version__");

        println!("- Pre-loading Python packages:");

        for module_name in [
            "cfgrib",
            "dask",
            "netCDF4",
            "numpy",
            "numcodecs",
            "pint",
            "xarray",
            "xeofs",
            "xhistogram",
            "zarr",
        ] {
            let module = py.import(module_name)?;
            let module_version: String = module.getattr(__version__)?.extract()?;

            println!("  - {module_name}: {module_version}");
        }

        Ok(())
    }

    pub fn compressors(&self) -> impl FusedIterator<Item = &Compressor> {
        self.compressors.values()
    }

    pub fn datasets(&self) -> impl FusedIterator<Item = &Dataset> {
        self.datasets.values()
    }

    pub fn pre_check_concrete_compressors(
        &self,
        py: Python,
        case_filter: Option<&BenchmarkCaseFilter>,
    ) -> Result<usize, BenchmarkPrepareError> {
        let mut num_compressors = 0;

        for compressor in self.compressors() {
            for concrete in compressor
                .iter_concrete()
                .map_err(LocationError::from)
                .map_err(BenchmarkPrepareError::PrecheckCompressorParameter)?
            {
                let concrete = concrete
                    .map_err(LocationError::from)
                    .map_err(BenchmarkPrepareError::PrecheckCompressorParameter)?;

                if case_filter.as_ref().map_or(true, |case_filter| {
                    case_filter.contains_codec_params(&concrete)
                }) {
                    concrete
                        .build_py(py)
                        .map_err(|err| err.map(|err| pyerr_chain_from_location_err(py, err)))
                        .map_err(BenchmarkPrepareError::PrecheckCompressorPython)?;
                    num_compressors += 1;
                }
            }
        }

        Ok(num_compressors)
    }
}

#[derive(Debug, Error)]
pub enum BenchmarkPrepareError {
    #[error("failed to load a dataset")]
    Dataset(#[source] LocationError<ParseDatasetError>),
    #[error("failed to load a compressor")]
    Compressor(#[source] LocationError<ParseCompressorError>),
    #[error("failed to import a codec")]
    CodecImport(#[source] LocationError<PyErrChain>),
    #[error("failed to load the unit registry")]
    UnitRegistry(#[source] LocationError<PyErrChain>),
    #[error("failed to precheck a compressor")]
    PrecheckCompressorPython(#[source] LocationError<PyErrChain>),
    #[error("failed to precheck a compressor")]
    PrecheckCompressorParameter(#[source] LocationError<ParameterEvalError>),
}
