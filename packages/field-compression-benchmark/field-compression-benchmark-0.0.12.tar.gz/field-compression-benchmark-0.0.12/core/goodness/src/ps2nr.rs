use std::{convert::Infallible, fmt};

use pyo3::{intern, prelude::*, types::IntoPyDict};

use core_error::LocationError;
use core_measure::Measurement;

use crate::error::CompressionError;

pub enum DataArrayPS2NR {}

impl DataArrayPS2NR {
    pub fn ps2nr(
        py: Python,
        da: Borrowed<PyAny>,
        rmse: CompressionError,
    ) -> Result<PeakSignalToNoiseRatio, LocationError<PyErr>> {
        let __float__ = intern!(py, "__float__");

        let skipna = [(intern!(py, "skipna"), true)].into_py_dict(py)?;

        let da_min: f64 = da
            .call_method(intern!(py, "min"), (), Some(&skipna))?
            .call_method0(__float__)?
            .extract()?;
        let da_max: f64 = da
            .call_method(intern!(py, "max"), (), Some(&skipna))?
            .call_method0(__float__)?
            .extract()?;

        let mse = rmse.to_f64() * rmse.to_f64();

        let ps2nr = 20.0_f64.mul_add((da_max - da_min).log10(), -10.0 * mse.log10());

        Ok(PeakSignalToNoiseRatio { ps2nr })
    }
}

#[derive(Copy, Clone, Debug, PartialEq, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct PeakSignalToNoiseRatio {
    ps2nr: f64,
}

impl PeakSignalToNoiseRatio {
    #[must_use]
    pub const fn new(ps2nr: f64) -> Self {
        Self { ps2nr }
    }
}

impl Measurement for PeakSignalToNoiseRatio {
    type Error = Infallible;

    fn to_f64(&self) -> f64 {
        self.ps2nr
    }

    fn try_from_f64(ps2nr: f64) -> Result<Self, LocationError<Self::Error>> {
        Ok(Self { ps2nr })
    }

    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        fmt.write_fmt(format_args!("{:.2}", self.ps2nr))
    }
}
