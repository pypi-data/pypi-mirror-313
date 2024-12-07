use std::{convert::Infallible, fmt, num::NonZeroUsize};

use pyo3::{
    intern,
    prelude::*,
    sync::GILOnceCell,
    types::{IntoPyDict, PyBool, PyString},
    IntoPyObjectExt,
};

use core_error::LocationError;
use core_measure::Measurement;

use super::correlation::DataArrayCorrelationGoodness;

pub enum DataArrayPreservedPCAGoodness {}

impl DataArrayPreservedPCAGoodness {
    pub fn goodness(
        py: Python,
        da_a: Borrowed<PyAny>,
        da_b: Borrowed<PyAny>,
        max_modes: NonZeroUsize,
        seed: u64,
    ) -> Result<PreservedPCAGoodness, LocationError<PyErr>> {
        static DASK_CONFIG_SET: GILOnceCell<Py<PyAny>> = GILOnceCell::new();

        let Some((max_dim, max_dim_rank)) = da_a
            .getattr(intern!(py, "sizes"))?
            .call_method0(intern!(py, "items"))?
            .try_iter()?
            .map(
                |dimension| -> Result<(Bound<PyString>, usize), LocationError<PyErr>> {
                    dimension?.extract().map_err(LocationError::new)
                },
            )
            .reduce(|acc, elem| {
                let (acc, elem) = (acc?, elem?);
                if acc.1 > elem.1 || (acc.1 == elem.1 && acc.0.gt(&elem.0)?) {
                    Ok(acc)
                } else {
                    Ok(elem)
                }
            })
            .transpose()?
        else {
            let val_a: f64 = da_a.call_method0(intern!(py, "__float__"))?.extract()?;
            let val_b: f64 = da_b.call_method0(intern!(py, "__float__"))?.extract()?;

            return if (val_a - val_b).abs() < f64::EPSILON {
                Ok(PreservedPCAGoodness::new(1.0))
            } else {
                Ok(PreservedPCAGoodness::new(0.0))
            };
        };
        let n_modes = max_modes.get().min(max_dim_rank);

        if da_a.getattr(intern!(py, "sizes"))?.len()? <= 1 {
            let correlation = DataArrayCorrelationGoodness::pearson_correlation(py, da_a, da_b)?;
            return Ok(PreservedPCAGoodness::new(correlation.abs()));
        }

        // Disable multi-threading for the computation of the principal components
        let context = DASK_CONFIG_SET.import(py, "dask.config", "set")?.call(
            (),
            Some(&[(intern!(py, "scheduler"), intern!(py, "synchronous"))].into_py_dict(py)?),
        )?;
        context.call_method0(intern!(py, "__enter__"))?;

        let abs_correlation_sum = (|| -> Result<f64, LocationError<PyErr>> {
            let model_a = Self::fit_pca_model(py, da_a, max_dim.as_borrowed(), n_modes, seed)?;
            let model_b = Self::fit_pca_model(py, da_b, max_dim.as_borrowed(), n_modes, seed)?;

            let scores_a = model_a.call_method(
                intern!(py, "scores"),
                (),
                Some(&[(intern!(py, "normalized"), false)].into_py_dict(py)?),
            )?;
            let scores_b = model_b.call_method(
                intern!(py, "scores"),
                (),
                Some(&[(intern!(py, "normalized"), false)].into_py_dict(py)?),
            )?;

            let mut abs_correlation_sum = 0.0_f64;

            for n in 1..=n_modes {
                let scores_a = scores_a.call_method(
                    intern!(py, "sel"),
                    (),
                    Some(&[(intern!(py, "mode"), n)].into_py_dict(py)?),
                )?;
                let scores_b = scores_b.call_method(
                    intern!(py, "sel"),
                    (),
                    Some(&[(intern!(py, "mode"), n)].into_py_dict(py)?),
                )?;

                let correlation = DataArrayCorrelationGoodness::pearson_correlation(
                    py,
                    model_a
                        .call_method(
                            intern!(py, "inverse_transform"),
                            (scores_a,),
                            Some(&[(intern!(py, "normalized"), false)].into_py_dict(py)?),
                        )?
                        .as_borrowed(),
                    model_b
                        .call_method(
                            intern!(py, "inverse_transform"),
                            (scores_b,),
                            Some(&[(intern!(py, "normalized"), false)].into_py_dict(py)?),
                        )?
                        .as_borrowed(),
                )?;

                abs_correlation_sum += correlation.abs();
            }

            Ok(abs_correlation_sum)
        })();

        context.call_method1(
            intern!(py, "__exit__"),
            (Option::<()>::None, Option::<()>::None, Option::<()>::None),
        )?;

        #[expect(clippy::cast_precision_loss)]
        let abs_correlation_sum_fraction = abs_correlation_sum? / (n_modes as f64);

        Ok(PreservedPCAGoodness::new(abs_correlation_sum_fraction))
    }

    fn fit_pca_model<'py>(
        py: Python<'py>,
        da: Borrowed<'_, 'py, PyAny>,
        dim: Borrowed<'_, 'py, PyString>,
        n_modes: usize,
        seed: u64,
    ) -> Result<Bound<'py, PyAny>, LocationError<PyErr>> {
        static XEOFS_EOF: GILOnceCell<Py<PyAny>> = GILOnceCell::new();

        #[expect(clippy::cast_possible_truncation)]
        // xeofs only takes u32 seeds
        let seed = ((seed & u64::from(u32::MAX)) ^ ((seed >> 32) & u64::from(u32::MAX))) as u32;

        let eof = XEOFS_EOF.import(py, "xeofs.single", "EOF")?;

        let model = eof.call(
            (),
            Some(
                &[
                    (intern!(py, "n_modes"), &n_modes.into_bound_py_any(py)?),
                    (intern!(py, "compute"), PyBool::new(py, true).as_any()),
                    // we generally work on high-dimensional data, so
                    //  always use the randomized solver and seed it
                    (intern!(py, "solver"), intern!(py, "randomized")),
                    (intern!(py, "random_state"), &seed.into_bound_py_any(py)?),
                    (intern!(py, "standardize"), PyBool::new(py, false).as_any()),
                ]
                .into_py_dict(py)?,
            ),
        )?;

        model.call_method(
            intern!(py, "fit"),
            (),
            Some(
                &[
                    (intern!(py, "X"), da),
                    (intern!(py, "dim"), dim.as_any().as_borrowed()),
                ]
                .into_py_dict(py)?,
            ),
        )?;

        Ok(model)
    }
}

#[derive(Copy, Clone, Debug, PartialEq, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct PreservedPCAGoodness {
    abs_correlation_sum_fraction: f64,
}

impl PreservedPCAGoodness {
    #[must_use]
    pub const fn new(abs_correlation_sum_fraction: f64) -> Self {
        Self {
            abs_correlation_sum_fraction,
        }
    }
}

impl Measurement for PreservedPCAGoodness {
    type Error = Infallible;

    fn to_f64(&self) -> f64 {
        self.abs_correlation_sum_fraction
    }

    fn try_from_f64(abs_correlation_sum_fraction: f64) -> Result<Self, LocationError<Self::Error>> {
        Ok(Self {
            abs_correlation_sum_fraction,
        })
    }

    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        fmt.write_fmt(format_args!(
            "{:.2}%",
            self.abs_correlation_sum_fraction * 100.0
        ))
    }
}
