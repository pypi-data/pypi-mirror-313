use nonempty::NonEmpty;
use pyo3::{intern, prelude::*, sync::GILOnceCell};
use sorted_vec::SortedSet;

use core_dataset::variable::derivative::DataDerivative;
use core_goodness::{
    bit_information::DataArrayBitInformation, correlation::DataArrayCorrelationGoodness,
    error::DataArrayError, pca::DataArrayPreservedPCAGoodness, ps2nr::DataArrayPS2NR,
    uniformity::DataArrayUniformityGoodness, DataArrayHistogram,
};

use crate::{
    error::BenchmarkSingleCaseError, measuring::GoodnessMeasurements, settings::MetricsSettings,
};

struct DerivativeStackItem<'a, 'py> {
    head: Option<&'a DataDerivative>,
    tail: &'a [DataDerivative],
    py_data_array: Bound<'py, PyAny>,
    py_data_array_compressed: Bound<'py, PyAny>,
}

pub fn compute_derivatives_goodness_measurements<'py>(
    py: Python<'py>,
    derivatives: &SortedSet<NonEmpty<DataDerivative>>,
    py_data_array: Bound<'py, PyAny>,
    py_data_array_compressed: Bound<'py, PyAny>,
    measurements: &mut [GoodnessMeasurements],
    metrics_settings: &MetricsSettings,
    seed: u64,
) -> Result<(), BenchmarkSingleCaseError> {
    let mut derivative_stack = NonEmpty {
        head: DerivativeStackItem {
            head: None,
            tail: &[],
            py_data_array,
            py_data_array_compressed,
        },
        tail: Vec::with_capacity(derivatives.iter().map(NonEmpty::len).max().unwrap_or(0)),
    };

    for (derivatives, measurements) in derivatives.iter().zip(measurements.iter_mut()) {
        let DerivativeStackItem {
            py_data_array: py_data_array_derivative,
            py_data_array_compressed: py_data_array_compressed_derivative,
            ..
        } = loop {
            let prev = derivative_stack.last();

            if prev.head.is_none() || Some(&derivatives.head) == prev.head {
                if let Some(suffix) = derivatives.tail.strip_prefix(prev.tail) {
                    // Case 1: derivatives strictly extends prev

                    if let Some(next) = match prev.head {
                        None => Some(&derivatives.head),
                        Some(_) => suffix.first(),
                    } {
                        // Case 1a: we need to compute more for the derivative
                        let (method, variable) = match next {
                            DataDerivative::Differentiate { differentiate } => {
                                (intern!(py, "differentiate"), differentiate)
                            },
                            DataDerivative::Integrate { integrate } => {
                                (intern!(py, "integrate"), integrate)
                            },
                        };

                        let py_data_array = prev
                            .py_data_array
                            .call_method1(method, (variable,))?
                            .call_method0(intern!(py, "compute"))?;
                        let py_data_array_compressed = prev
                            .py_data_array_compressed
                            .call_method1(method, (variable,))?
                            .call_method0(intern!(py, "compute"))?;

                        derivative_stack.push(DerivativeStackItem {
                            head: Some(&derivatives.head),
                            tail: &derivatives.tail,
                            py_data_array,
                            py_data_array_compressed,
                        });

                        continue;
                    }

                    // Case 1b: we have already computed the derivative, done
                    break prev;
                }
            }

            // Case 2: we need to remove at least one stack level to re-establish a
            //         shared prefix with the top item on the stack
            // We don't drop inside the GIL here since the GIL will be aquired for
            //  the next stack push or to compute the goodness measurement below
            derivative_stack.pop();
        };

        compute_goodness_measurements(
            py,
            py_data_array_derivative.as_borrowed(),
            py_data_array_compressed_derivative.as_borrowed(),
            measurements,
            metrics_settings,
            seed,
        )?;
    }

    Ok(())
}

pub fn compute_goodness_measurements<'py>(
    py: Python<'py>,
    py_data_array: Borrowed<'_, 'py, PyAny>,
    py_data_array_compressed: Borrowed<'_, 'py, PyAny>,
    measurements: &mut GoodnessMeasurements,
    metrics_settings: &MetricsSettings,
    seed: u64,
) -> Result<(), BenchmarkSingleCaseError> {
    static XARRAY_APPLY_UFUNC: GILOnceCell<Py<PyAny>> = GILOnceCell::new();
    static NUMPY_MAXIMUM: GILOnceCell<Py<PyAny>> = GILOnceCell::new();

    let py_data_array_error =
        py_data_array.call_method1(intern!(py, "__sub__"), (py_data_array_compressed,))?;
    let py_data_array_error_abs = py_data_array_error.call_method0(intern!(py, "__abs__"))?;
    // relative error = (x - y) / max(abs(y), epsilon)
    let py_data_array_error_rel = py_data_array_error.call_method1(
        intern!(py, "__truediv__"),
        (XARRAY_APPLY_UFUNC
            .import(py, "xarray", "apply_ufunc")?
            .call1((
                NUMPY_MAXIMUM.import(py, "numpy", "maximum")?,
                py_data_array.call_method0(intern!(py, "__abs__"))?,
                f64::EPSILON,
            ))?,),
    )?;
    let py_data_array_error_rel_abs =
        py_data_array_error_rel.call_method0(intern!(py, "__abs__"))?;

    let py_data_array_error_histogram = DataArrayHistogram::compute(
        py,
        py_data_array_error.as_borrowed(),
        metrics_settings.error.bins,
    )?;
    let py_data_array_error_abs_histogram = DataArrayHistogram::compute(
        py,
        py_data_array_error_abs.as_borrowed(),
        metrics_settings.error.bins,
    )?;
    let py_data_array_error_rel_histogram = DataArrayHistogram::compute(
        py,
        py_data_array_error_rel.as_borrowed(),
        metrics_settings.error.bins,
    )?;
    let py_data_array_error_rel_abs_histogram = DataArrayHistogram::compute(
        py,
        py_data_array_error_rel_abs.as_borrowed(),
        metrics_settings.error.bins,
    )?;
    let py_data_array_error_rmse = DataArrayError::rmse(py, py_data_array_error.as_borrowed())?;

    measurements
        .uniformity
        .push(DataArrayUniformityGoodness::goodness(
            py,
            &py_data_array_error_histogram,
        )?);

    measurements
        .uniformity_rel
        .push(DataArrayUniformityGoodness::goodness(
            py,
            &py_data_array_error_rel_histogram,
        )?);

    measurements
        .correlation
        .push(DataArrayCorrelationGoodness::goodness(
            py,
            py_data_array,
            py_data_array_compressed,
        )?);

    measurements
        .preserved_pca
        .push(DataArrayPreservedPCAGoodness::goodness(
            py,
            py_data_array,
            py_data_array_compressed,
            metrics_settings.pca.max_modes,
            seed,
        )?);

    measurements
        .bit_information
        .push(DataArrayBitInformation::goodness(
            py,
            py_data_array,
            py_data_array_compressed,
            // TODO: allow configuring the set-zero when insignificant confidence threshold
            Some(0.99),
        )?);

    py_data_array_error_histogram
        .resample_into(&mut measurements.error, metrics_settings.error.resamples)?;
    py_data_array_error_abs_histogram.resample_into(
        &mut measurements.error_abs,
        metrics_settings.error.resamples,
    )?;
    py_data_array_error_rel_histogram.resample_into(
        &mut measurements.error_rel,
        metrics_settings.error.resamples,
    )?;
    py_data_array_error_rel_abs_histogram.resample_into(
        &mut measurements.error_rel_abs,
        metrics_settings.error.resamples,
    )?;

    measurements.error_rmse.push(py_data_array_error_rmse);

    measurements.ps2nr.push(DataArrayPS2NR::ps2nr(
        py,
        py_data_array,
        py_data_array_error_rmse,
    )?);

    Ok(())
}
