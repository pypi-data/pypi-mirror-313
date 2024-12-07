use std::{convert::Infallible, fmt};

use pyo3::{intern, prelude::*, sync::GILOnceCell};

use core_error::LocationError;
use core_measure::Measurement;

pub enum DataArrayCorrelationGoodness {}

impl DataArrayCorrelationGoodness {
    pub fn goodness(
        py: Python,
        da_a: Borrowed<PyAny>,
        da_b: Borrowed<PyAny>,
    ) -> Result<CompressionCorrelationGoodness, LocationError<PyErr>> {
        let pearson_correlation = Self::pearson_correlation(py, da_a, da_b)?;

        // correlation coefficient of 0 is the worst -> 0% goodness
        // correlation coefficient of 1 is the best -> 100% goodness
        // correlation coefficient of -1 is ... probably a sign-flip -> 100% goodness
        let abs_correlation = pearson_correlation.abs();

        Ok(CompressionCorrelationGoodness::new(abs_correlation))
    }

    pub fn pearson_correlation(
        py: Python,
        da_a: Borrowed<PyAny>,
        da_b: Borrowed<PyAny>,
    ) -> Result<f64, LocationError<PyErr>> {
        static XARRAY_COV: GILOnceCell<Py<PyAny>> = GILOnceCell::new();

        let squeeze = intern!(py, "squeeze");
        let mean = intern!(py, "mean");
        let std = intern!(py, "std");
        let __float__ = intern!(py, "__float__");

        let da_a = da_a.call_method0(squeeze)?;
        let da_b = da_b.call_method0(squeeze)?;

        let stdv_a: f64 = da_a.call_method0(std)?.call_method0(__float__)?.extract()?;
        let stdv_b: f64 = da_b.call_method0(std)?.call_method0(__float__)?.extract()?;

        match (stdv_a.abs() < f64::EPSILON, stdv_b.abs() < f64::EPSILON) {
            // both data arrays are constant, check if the means match
            (true, true) => {
                let mean_a: f64 = da_a
                    .call_method0(mean)?
                    .call_method0(__float__)?
                    .extract()?;
                let mean_b: f64 = da_b
                    .call_method0(mean)?
                    .call_method0(__float__)?
                    .extract()?;

                return if (mean_a - mean_b).abs() < f64::EPSILON {
                    Ok(1.0)
                } else {
                    Ok(0.0)
                };
            },
            // one data array is constant while the other is not -> zero correlation
            (true, false) | (false, true) => return Ok(0.0),
            // both data arrays have varying values -> correlation is well-defined
            (false, false) => (),
        }

        let covariance: f64 = XARRAY_COV
            .import(py, "xarray", "cov")?
            .call1((da_a, da_b))?
            .call_method0(intern!(py, "__float__"))?
            .extract()?;

        let correlation = covariance / (stdv_a * stdv_b);

        Ok(correlation)
    }
}

#[derive(Copy, Clone, Debug, PartialEq, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct CompressionCorrelationGoodness {
    abs_correlation: f64,
}

impl CompressionCorrelationGoodness {
    #[must_use]
    pub const fn new(abs_correlation: f64) -> Self {
        Self { abs_correlation }
    }
}

impl Measurement for CompressionCorrelationGoodness {
    type Error = Infallible;

    fn to_f64(&self) -> f64 {
        self.abs_correlation
    }

    fn try_from_f64(abs_correlation: f64) -> Result<Self, LocationError<Self::Error>> {
        Ok(Self { abs_correlation })
    }

    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        fmt.write_fmt(format_args!("{:.2}%", self.abs_correlation * 100.0))
    }
}
