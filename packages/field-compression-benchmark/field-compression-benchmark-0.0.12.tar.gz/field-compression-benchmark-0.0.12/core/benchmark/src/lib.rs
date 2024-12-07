#![allow(clippy::missing_errors_doc)] // FIXME

use nonempty::NonEmpty;
use pyo3::{intern, prelude::*};
use rand::SeedableRng;
use sorted_vec::SortedSet;

use core_compressor::compressor::ConcreteCompressor;
use core_dataset::{
    dataset::Dataset,
    variable::{derivative::DataDerivative, DataVariable},
};

pub mod case;
pub mod error;
mod goodness;
pub mod measuring;
mod performance;
pub mod report;
pub mod reporter;
pub mod settings;

use crate::{
    case::BenchmarkCase,
    error::BenchmarkSingleCaseError,
    goodness::{compute_derivatives_goodness_measurements, compute_goodness_measurements},
    measuring::Measurements,
    performance::compress_and_perform_performance_measurements,
    report::BenchmarkCaseOutput,
    settings::{BenchmarkSettings, MetricsSettings},
};

pub fn run_benchmark_case<'a>(
    py: Python,
    dataset: &'a Dataset,
    variable: &'a DataVariable,
    compressor: &ConcreteCompressor<'a>,
    settings: &BenchmarkSettings,
) -> Result<BenchmarkCaseOutput, BenchmarkSingleCaseError> {
    let mut rng = rand_chacha::ChaChaRng::seed_from_u64(settings.measurements.bootstrap.seed);

    let py_data_array = dataset.open_xarray_sliced_variable(py, variable)?;

    let num_measurements = settings.measurements.num_repeats.get() * variable.num_reductions();

    let mut measurements = Measurements::new(
        num_measurements,
        settings.measurements.metrics.error.resamples.get(),
        variable.derivatives().len(),
        compressor.codecs().len(),
    );

    for it in 0..settings.measurements.num_repeats.get() {
        let mut reductions = variable.iter_reductions();

        loop {
            let Some(sliced_py_data_array) = reductions
                .next(py)?
                .map(|reduction| py_data_array.get_item(reduction))
                .transpose()?
            else {
                break;
            };

            run_benchmark_iteration_and_perform_measurements(
                py,
                compressor,
                variable.derivatives(),
                sliced_py_data_array.as_borrowed(),
                &mut measurements,
                &settings.measurements.metrics,
                it == 0,
                settings.measurements.bootstrap.seed,
            )?;
        }
    }

    Ok(BenchmarkCaseOutput {
        stats: measurements.analyse(&mut rng, settings.measurements.bootstrap.samples)?,
    })
}

#[expect(clippy::too_many_arguments)] // FIXME
fn run_benchmark_iteration_and_perform_measurements<'py>(
    py: Python<'py>,
    compressor: &ConcreteCompressor,
    derivatives: &SortedSet<NonEmpty<DataDerivative>>,
    py_data_array: Borrowed<'_, 'py, PyAny>,
    measurements: &mut Measurements,
    metrics_settings: &MetricsSettings,
    compute_goodness: bool,
    seed: u64,
) -> Result<(), BenchmarkSingleCaseError> {
    let py_data_array_compressed =
        compress_and_perform_performance_measurements(py, compressor, py_data_array, measurements)?;

    if !compute_goodness {
        return Ok(());
    }

    // Eagerly pre-load the uncompressed dataset to speed up analysis
    let py_data_array_computed = py_data_array.call_method0(intern!(py, "compute"))?;

    compute_goodness_measurements(
        py,
        py_data_array_computed.as_borrowed(),
        py_data_array_compressed.as_borrowed(),
        &mut measurements.goodness.head,
        metrics_settings,
        seed,
    )?;

    compute_derivatives_goodness_measurements(
        py,
        derivatives,
        py_data_array_computed,
        py_data_array_compressed,
        &mut measurements.goodness.tail,
        metrics_settings,
        seed,
    )?;

    Ok(())
}
