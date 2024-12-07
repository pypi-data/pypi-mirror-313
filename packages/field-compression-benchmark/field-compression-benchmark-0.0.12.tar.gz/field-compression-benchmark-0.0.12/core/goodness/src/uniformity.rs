use std::{convert::Infallible, fmt};

use numpy::PyUntypedArrayMethods;
use pyo3::{
    intern,
    prelude::*,
    types::{IntoPyDict, PyString},
};

use core_error::LocationError;
use core_measure::Measurement;

use super::DataArrayHistogram;

pub enum DataArrayUniformityGoodness {}

impl DataArrayUniformityGoodness {
    pub fn goodness<'py>(
        py: Python<'py>,
        histogram: &DataArrayHistogram<'py>,
    ) -> Result<CompressionUniformityGoodness, LocationError<PyErr>> {
        #[expect(clippy::cast_precision_loss)]
        let u01_entropy = (PyUntypedArrayMethods::len(&histogram.bins) as f64).log2();
        let da_entropy = histogram.entropy()?;

        let entropy_goodness = da_entropy / u01_entropy;

        let morans_i = Self::morans_i(py, histogram.da.as_borrowed())?;
        let morans_i_goodness = 1.0 - morans_i.abs();

        Ok(CompressionUniformityGoodness::new(
            entropy_goodness * morans_i_goodness,
        ))
    }

    pub fn morans_i(py: Python, da: Borrowed<PyAny>) -> Result<f64, LocationError<PyErr>> {
        // da_mean = da.mean()
        let da_mean: f64 = da.call_method0(intern!(py, "mean"))?.extract()?;
        // da_mid = da - da_mean
        let da_mid = da.call_method1(intern!(py, "__sub__"), (da_mean,))?;

        // denominator = (da_mid**2).sum()
        let denominator: f64 = da_mid
            .call_method1(intern!(py, "__mul__"), (da_mid.as_borrowed(),))?
            .call_method0(intern!(py, "sum"))?
            .extract()?;

        if denominator.abs() < f64::EPSILON {
            return Ok(0.0);
        }

        let mut num_neighbours = 0_u32;

        let shift = intern!(py, "shift");
        let add = intern!(py, "__add__");

        // neighbours_sum = (
        //    sum(da.shift({dim: -1}) for dim in da.dims) +
        //    sum(da.shift({dim: +1}) for dim in da.dims)
        let Some(neighbours_sum) = da.getattr(intern!(py, "dims"))?.try_iter()?.try_fold(
            None,
            |acc, dim| -> Result<Option<Bound<PyAny>>, LocationError<PyErr>> {
                let dim: Bound<PyString> = dim?.extract()?;

                let left_neighbour =
                    da.call_method1(shift, ([(dim.as_borrowed(), -1)].into_py_dict(py)?,))?;
                let right_neighbour =
                    da.call_method1(shift, ([(dim.as_borrowed(), 1)].into_py_dict(py)?,))?;

                let acc = match acc {
                    None => left_neighbour,
                    Some(acc) => acc.call_method1(add, (left_neighbour,))?,
                };

                num_neighbours += 2;

                acc.call_method1(add, (right_neighbour,))
                    .map(Some)
                    .map_err(LocationError::new)
            },
        )?
        else {
            return Ok(0.0);
        };

        // neighbours_difference = neighbours_sum - da_mean * len(da.dims) * 2
        let neighbours_difference = neighbours_sum.call_method1(
            intern!(py, "__sub__"),
            (da_mean * f64::from(num_neighbours),),
        )?;

        // numerator = (neighbours_difference * da_mid).sum()
        let numerator: f64 = neighbours_difference
            .call_method1(intern!(py, "__mul__"), (da_mid,))?
            .call_method0(intern!(py, "sum"))?
            .extract()?;

        // Moran's I = numerator / (denominator * len(da.dims) * 2)
        Ok(numerator / (denominator * f64::from(num_neighbours)))
    }
}

#[derive(Copy, Clone, Debug, PartialEq, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct CompressionUniformityGoodness {
    uniformity: f64,
}

impl CompressionUniformityGoodness {
    #[must_use]
    pub const fn new(uniformity: f64) -> Self {
        Self { uniformity }
    }
}

impl Measurement for CompressionUniformityGoodness {
    type Error = Infallible;

    fn to_f64(&self) -> f64 {
        self.uniformity
    }

    fn try_from_f64(uniformity: f64) -> Result<Self, LocationError<Self::Error>> {
        Ok(Self { uniformity })
    }

    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        fmt.write_fmt(format_args!("{:.2}%", self.uniformity * 100.0))
    }
}
