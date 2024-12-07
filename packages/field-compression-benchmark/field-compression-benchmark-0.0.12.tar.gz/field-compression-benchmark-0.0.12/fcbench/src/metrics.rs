use std::num::NonZeroUsize;

use numpy::PyArray1;
use pyo3::prelude::*;

pub fn create_module(py: Python) -> Result<Bound<PyModule>, PyErr> {
    let module = PyModule::new(py, "metrics")?;

    module.add_class::<BitInformation>()?;
    module.add_class::<PreservedPCA>()?;
    module.add_class::<Uniformity>()?;

    Ok(module)
}

#[pyclass(module = "fcbench.metrics", frozen)]
pub struct BitInformation {
    _inner: (),
}

#[pymethods]
impl BitInformation {
    #[staticmethod]
    /// [SIGNATURE]: # "(a: Union[numpy.array, xarray.DataArray], /, *, set_zero_insignificant_confidence: Optional[float] = 0.99) -> numpy.array"
    #[pyo3(signature = (a, /, *, set_zero_insignificant_confidence=Some(0.99)))]
    pub fn bit_information<'py>(
        py: Python<'py>,
        a: &Bound<'py, PyAny>,
        set_zero_insignificant_confidence: Option<f64>,
    ) -> Result<Bound<'py, PyArray1<f64>>, PyErr> {
        #[expect(clippy::option_if_let_else)]
        let bit_information = if let Ok(a) = a.downcast() {
            core_goodness::bit_information::DataArrayBitInformation::bit_information_array(
                py,
                a.into(),
                set_zero_insignificant_confidence,
            )
        } else {
            core_goodness::bit_information::DataArrayBitInformation::bit_information(
                py,
                a.into(),
                set_zero_insignificant_confidence,
            )
        }
        .map_err(core_error::LocationError::into_error)?;

        Ok(bit_information)
    }

    #[staticmethod]
    /// [SIGNATURE]: # "(a: Union[numpy.array, xarray.DataArray], /, *, set_zero_insignificant_confidence: Optional[float] = 0.99) -> float"
    #[pyo3(signature = (a, /, *, set_zero_insignificant_confidence=Some(0.99)))]
    pub fn information_content(
        py: Python,
        a: &Bound<PyAny>,
        set_zero_insignificant_confidence: Option<f64>,
    ) -> Result<f64, PyErr> {
        #[expect(clippy::option_if_let_else)]
        let information_content = if let Ok(a) = a.downcast() {
            core_goodness::bit_information::DataArrayBitInformation::information_content_array(
                py,
                a.into(),
                set_zero_insignificant_confidence,
            )
        } else {
            core_goodness::bit_information::DataArrayBitInformation::information_content(
                py,
                a.into(),
                set_zero_insignificant_confidence,
            )
        }
        .map_err(core_error::LocationError::into_error)?;

        Ok(information_content)
    }

    #[staticmethod]
    /// [SIGNATURE]: # "(a: Union[numpy.array, xarray.DataArray], /, information_ratio: float, *, set_zero_insignificant_confidence: Optional[float] = 0.99) -> int"
    #[pyo3(signature = (a, /, information_ratio, *, set_zero_insignificant_confidence=Some(0.99)))]
    pub fn required_bits(
        py: Python,
        a: &Bound<PyAny>,
        information_ratio: f64,
        set_zero_insignificant_confidence: Option<f64>,
    ) -> Result<usize, PyErr> {
        #[expect(clippy::option_if_let_else)]
        let required_bits = if let Ok(a) = a.downcast() {
            core_goodness::bit_information::DataArrayBitInformation::required_bits_array(
                py,
                a.into(),
                information_ratio,
                set_zero_insignificant_confidence,
            )
        } else {
            core_goodness::bit_information::DataArrayBitInformation::required_bits(
                py,
                a.into(),
                information_ratio,
                set_zero_insignificant_confidence,
            )
        }
        .map_err(core_error::LocationError::into_error)?;

        Ok(required_bits)
    }
}

#[pyclass(module = "fcbench.metrics", frozen)]
pub struct PreservedPCA {
    _inner: (),
}

#[pymethods]
impl PreservedPCA {
    #[staticmethod]
    /// [SIGNATURE]: # "(a: xarray.DataArray, b: xarray.DataArray, /, *, max_modes: int = 10, seed: int = 42) -> float"
    #[pyo3(signature = (a, b, /, *, max_modes=NonZeroUsize::MIN.saturating_add(9), seed = 42))]
    pub fn goodness(
        py: Python,
        a: &Bound<PyAny>,
        b: &Bound<PyAny>,
        max_modes: NonZeroUsize,
        seed: u64,
    ) -> Result<f64, PyErr> {
        let preserved_pca = core_goodness::pca::DataArrayPreservedPCAGoodness::goodness(
            py,
            a.as_borrowed(),
            b.as_borrowed(),
            max_modes,
            seed,
        )
        .map_err(core_error::LocationError::into_error)?;

        Ok(core_measure::Measurement::to_f64(&preserved_pca))
    }
}

#[pyclass(module = "fcbench.metrics", frozen)]
pub struct Uniformity {
    _inner: (),
}

#[pymethods]
impl Uniformity {
    #[staticmethod]
    /// [SIGNATURE]: # "(a: xarray.DataArray, /, *, bins: int = 100) -> float"
    #[pyo3(signature = (a, /, *, bins=NonZeroUsize::MIN.saturating_add(99)))]
    pub fn goodness(py: Python, a: &Bound<PyAny>, bins: NonZeroUsize) -> Result<f64, PyErr> {
        let histogram = core_goodness::DataArrayHistogram::compute(py, a.as_borrowed(), bins)
            .map_err(core_error::LocationError::into_error)?;

        let uniformity =
            core_goodness::uniformity::DataArrayUniformityGoodness::goodness(py, &histogram)
                .map_err(core_error::LocationError::into_error)?;

        Ok(core_measure::Measurement::to_f64(&uniformity))
    }
}
