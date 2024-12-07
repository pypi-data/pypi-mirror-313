#![allow(clippy::missing_errors_doc)] // FIXME

#[macro_use]
extern crate crunchy;

use std::{convert::Infallible, num::NonZeroUsize};

use numpy::{PyArray1, PyArrayMethods, PyUntypedArrayMethods};
use pyo3::{
    intern,
    prelude::*,
    sync::GILOnceCell,
    types::{IntoPyDict, PyTuple},
    PyTypeInfo,
};

use core_error::LocationError;
use core_measure::{stats::ConfidenceInterval, Measurement};

pub mod bit_information;
pub mod correlation;
pub mod error;
pub mod pca;
pub mod ps2nr;
pub mod uniformity;

pub struct DataArrayHistogram<'py> {
    da: Bound<'py, PyAny>,
    _da_min: f64,
    _da_max: f64,
    edges: Bound<'py, PyArray1<f64>>,
    bins: Bound<'py, PyArray1<usize>>,
}

impl<'py> DataArrayHistogram<'py> {
    pub fn compute(
        py: Python<'py>,
        da: Borrowed<'_, 'py, PyAny>,
        bins: NonZeroUsize,
    ) -> Result<Self, LocationError<PyErr>> {
        static NUMPY_LINSPACE: GILOnceCell<Py<PyAny>> = GILOnceCell::new();
        static XHISTOGRAM_HISTOGRAM: GILOnceCell<Py<PyAny>> = GILOnceCell::new();

        let skipna = [(intern!(py, "skipna"), true)].into_py_dict(py)?;

        let da_min = da.call_method(intern!(py, "min"), PyTuple::empty(py), Some(&skipna))?;
        let da_max = da.call_method(intern!(py, "max"), PyTuple::empty(py), Some(&skipna))?;

        let da_min = da_min.extract::<f64>()?;
        let da_max = da_max.extract::<f64>()?;

        let edges: Bound<PyArray1<f64>> = NUMPY_LINSPACE
            .import(py, "numpy", "linspace")?
            .call1((da_min, da_max, bins.get() + 1))?
            .extract()?;
        let bins: Bound<PyArray1<usize>> = XHISTOGRAM_HISTOGRAM
            .import(py, "xhistogram.core", "histogram")?
            .call(
                (da,),
                Some(&[(intern!(py, "bins"), edges.as_borrowed())].into_py_dict(py)?),
            )?
            .get_item(0)?
            .call_method1(intern!(py, "astype"), (intern!(py, "uintp"),))?
            .extract()?;

        Ok(DataArrayHistogram {
            da: da.to_owned(),
            _da_min: da_min,
            _da_max: da_max,
            edges,
            bins,
        })
    }

    pub fn approximate_quantiles_tuple(
        &self,
        py: Python<'py>,
        percentiles: &[f64],
    ) -> Result<Bound<'py, PyTuple>, LocationError<PyErr>> {
        static NUMPY_INSERT: GILOnceCell<Py<PyAny>> = GILOnceCell::new();
        static NUMPY_CUMSUM: GILOnceCell<Py<PyAny>> = GILOnceCell::new();
        static NUMPY_INTERP: GILOnceCell<Py<PyAny>> = GILOnceCell::new();

        let zero_bins: Bound<PyArray1<usize>> = NUMPY_INSERT
            .import(py, "numpy", "insert")?
            .call1((self.bins.as_borrowed(), 0, 0_usize))?
            .extract()?;
        let cumulative_bins: Bound<PyArray1<usize>> = NUMPY_CUMSUM
            .import(py, "numpy", "cumsum")?
            .call1((zero_bins,))?
            .extract()?;
        let cdf: Bound<PyArray1<f64>> = cumulative_bins
            .call_method1(
                intern!(py, "__truediv__"),
                (cumulative_bins.get_item(PyUntypedArrayMethods::len(&cumulative_bins) - 1)?,),
            )?
            .extract()?;

        let quantiles = PyTuple::type_object(py)
            .call1((NUMPY_INTERP.import(py, "numpy", "interp")?.call1((
                PyTuple::new(py, percentiles)?,
                cdf,
                self.edges.as_borrowed(),
            ))?,))?
            .extract()?;

        Ok(quantiles)
    }

    pub fn approximate_quantiles_variable(
        &self,
        percentiles: &[f64],
    ) -> Result<Vec<f64>, LocationError<PyErr>> {
        self.approximate_quantiles_tuple(self.da.py(), percentiles)?
            .extract()
            .map_err(LocationError::new)
    }

    pub fn approximate_quantiles<const N: usize>(
        &self,
        percentiles: [f64; N],
    ) -> Result<[f64; N], LocationError<PyErr>> {
        self.approximate_quantiles_tuple(self.da.py(), &percentiles)?
            .extract()
            .map_err(LocationError::new)
    }

    pub fn summarise(&self) -> Result<ConfidenceInterval<f64>, LocationError<PyErr>> {
        let [p2_5, p15_9, p50, p84_1, p97_5] =
            self.approximate_quantiles([0.025, 0.159, 0.5, 0.841, 0.975])?;

        Ok(ConfidenceInterval {
            p2_5,
            p15_9,
            p50,
            p84_1,
            p97_5,
        })
    }

    pub fn resample_into<T: Measurement<Error = Infallible>>(
        &self,
        samples: &mut Vec<T>,
        num_resamples: NonZeroUsize,
    ) -> Result<(), LocationError<PyErr>> {
        let mut i: usize = 0;
        let percentiles = (0..num_resamples.get())
            .map(|_| {
                #[expect(clippy::cast_precision_loss)]
                let percentile = ((i + 1) as f64) / ((num_resamples.get() + 1) as f64);
                i += 1;
                percentile
            })
            .collect::<Vec<_>>();

        for quantile in self.approximate_quantiles_variable(&percentiles)? {
            samples.push(match T::try_from_f64(quantile) {
                Ok(measurement) => measurement,
                Err(err) => err.infallible(),
            });
        }

        Ok(())
    }

    pub fn entropy(&self) -> Result<f64, LocationError<PyErr>> {
        let readonly_bins = self.bins.try_readonly().map_err(PyErr::from)?;
        let bins = readonly_bins.as_slice().map_err(PyErr::from)?;

        #[expect(clippy::cast_precision_loss)]
        let total = bins.iter().sum::<usize>() as f64;

        let non_zero_probabilities = bins.iter().filter_map(|bin| {
            if *bin == 0 {
                None
            } else {
                #[expect(clippy::cast_precision_loss)]
                Some((*bin as f64) / total)
            }
        });
        let neg_entropy = non_zero_probabilities.map(|p| p * p.log2()).sum::<f64>();

        // entropy = -sum(p * np.log2(p) for p in (bins / bins.sum()) if p != 0.0)
        Ok((-neg_entropy).max(0.0_f64))
    }
}
