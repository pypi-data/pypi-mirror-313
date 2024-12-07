use std::{
    collections::{HashMap, HashSet},
    path::{Path, PathBuf},
};

use numpy::PyUntypedArray;
use pyo3::{prelude::*, types::PyDict};
use vecmap::VecSet;

use crate::dataclass::{Dataclass, DataclassOutFrozen, DataclassRegistry};

/// Create a [`PyModule`] with name "compressor" that exports the
/// [`Compressor`] and the [`compute_numpy_array_compress_decompress()`] and
/// [`compute_dataarray_compress_decompress()`] functions.
///
/// The created module is expected to be a submodule of `fcbench` since the
/// all exports expect to have the `fcbench.compressor` module path.
pub fn create_module(py: Python) -> Result<Bound<PyModule>, PyErr> {
    let module = PyModule::new(py, "compressor")?;

    module.add_class::<Compressor>()?;
    module.add_class::<Codec>()?;
    module.add_class::<ConcreteCompressor>()?;
    module.add_class::<ConcreteCodec>()?;
    module.add_function(wrap_pyfunction!(
        compute_numpy_array_compress_decompress,
        &module
    )?)?;
    module.add_function(wrap_pyfunction!(
        compute_dataarray_compress_decompress,
        &module
    )?)?;

    let types = PyModule::new(py, "types")?;
    dataclass_registry().export(py, types.as_borrowed())?;
    module.add_submodule(&types)?;

    Ok(module)
}

fn dataclass_registry() -> DataclassRegistry {
    let mut registry = DataclassRegistry::new();

    registry.insert::<core_compressor::compress::CodecPerformanceMeasurement>();

    registry
}

#[pyclass(module = "fcbench.compressor", frozen)]
pub struct Compressor {
    compressor: core_compressor::compressor::Compressor,
}

#[pymethods]
impl Compressor {
    #[staticmethod]
    #[pyo3(signature = (**kwargs))]
    /// [SIGNATURE]: # "(**kwargs) -> Compressor"
    pub fn from_config_kwargs<'py>(
        py: Python<'py>,
        kwargs: Option<Bound<'py, PyDict>>,
    ) -> Result<Self, PyErr> {
        let kwargs = kwargs.unwrap_or_else(|| PyDict::new(py));

        let mut depythonizer = pythonize::Depythonizer::from_object(kwargs.as_any());

        match core_compressor::compressor::Compressor::from_deserialised_config(
            py,
            &mut depythonizer,
        ) {
            Ok(compressor) => Ok(Self { compressor }),
            Err(err) => Err(PyErr::from(err)),
        }
    }

    #[staticmethod]
    /// [SIGNATURE]: # "(config: str) -> Compressor"
    pub fn from_config_str(py: Python, config: &str) -> Result<Self, PyErr> {
        match core_compressor::compressor::Compressor::from_config_str(py, config) {
            Ok(compressor) => Ok(Self { compressor }),
            Err(err) => Err(core_error::pyerr_from_location_err(py, err)),
        }
    }

    #[expect(clippy::needless_pass_by_value)]
    #[staticmethod]
    /// [SIGNATURE]: # "(config_file: Union[str, Path, PathLike]) -> Compressor"
    pub fn from_config_file(py: Python, config_file: PathBuf) -> Result<Self, PyErr> {
        match core_compressor::compressor::Compressor::from_config_file(py, &config_file) {
            Ok(compressor) => Ok(Self { compressor }),
            Err(err) => Err(core_error::pyerr_from_location_err(py, err)),
        }
    }

    #[staticmethod]
    /// [SIGNATURE]: # "(config_files: Set[Union[str, Path, PathLike]]) -> Mapping[str, Compressor]"
    pub fn from_config_files(
        py: Python,
        config_files: HashSet<PathBuf>,
    ) -> Result<HashMap<String, Self>, PyErr> {
        match core_compressor::compressor::Compressor::from_config_files(
            py,
            &VecSet::from_iter(config_files),
        ) {
            Ok(compressors) => Ok(compressors
                .into_iter()
                .map(|(name, compressor)| (name, Self { compressor }))
                .collect()),
            Err(err) => Err(core_error::pyerr_from_location_err(py, err)),
        }
    }

    #[expect(clippy::needless_pass_by_value)]
    #[staticmethod]
    /// [SIGNATURE]: # "(config_directory: Union[str, Path, PathLike]) -> Mapping[str, Compressor]"
    pub fn from_config_directory(
        py: Python,
        config_directory: PathBuf,
    ) -> Result<HashMap<String, Self>, PyErr> {
        match core_compressor::compressor::Compressor::from_config_directory(py, &config_directory)
        {
            Ok(compressors) => Ok(compressors
                .into_iter()
                .map(|(name, compressor)| (name, Self { compressor }))
                .collect()),
            Err(err) => Err(core_error::pyerr_from_location_err(py, err)),
        }
    }

    #[must_use]
    #[getter]
    /// [SIGNATURE]: # "(self) -> str"
    pub fn name(&self) -> &str {
        self.compressor.name()
    }

    #[must_use]
    #[getter]
    /// [SIGNATURE]: # "(self) -> Optional[Union[str, bytes, PathLike]]"
    pub fn config_path(&self) -> Option<&Path> {
        self.compressor.config_path()
    }

    #[must_use]
    #[getter]
    /// [SIGNATURE]: # "(self) -> Iterator[Codec]"
    pub fn codecs(this: PyRef<Self>) -> CodecIterator {
        let iter = this.compressor.codecs();
        let iter: Box<dyn ExactSizeIterator<Item = &core_compressor::codec::Codec> + Send + Sync> =
            Box::new(iter);
        // Safety:
        // - we borrow the compressor that's inside PyRef<Self> and Py<Self>
        // - the iterator and its items all carry around clones of Py<Self>
        // - so the compressor lives long enough
        // - Self is a frozen class, so no mutation can occur
        #[expect(unsafe_code)]
        let iter: Box<
            dyn ExactSizeIterator<Item = &'static core_compressor::codec::Codec>
                + Send
                + Sync
                + 'static,
        > = unsafe { std::mem::transmute(iter) };

        let py_compressor: Py<Self> = Py::from(this);

        CodecIterator {
            _compressor: py_compressor,
            iter,
        }
    }

    #[must_use]
    /// [SIGNATURE]: # "(self)"
    pub fn minimise(&self) -> Self {
        // copy on write since Self is a frozen PyO3 class
        let mut this = Self {
            compressor: self.compressor.clone(),
        };
        this.compressor.minimise();
        this
    }

    #[must_use]
    pub fn __str__(&self) -> String {
        format!("{}", self.compressor)
    }

    /// [SIGNATURE]: # "(self)"
    pub fn ensure_imports(&self, py: Python) -> Result<(), PyErr> {
        self.compressor
            .ensure_py_imports(py)
            .map_err(core_error::LocationError::into_error)
    }

    #[getter]
    /// [SIGNATURE]: # "(self) -> Iterator[ConcreteCompressor]"
    pub fn concrete(this: PyRef<Self>, py: Python) -> Result<ConcreteCompressorIterator, PyErr> {
        let iter: core_compressor::compressor::ConcreteCompressorIterator<'_> = this
            .compressor
            .iter_concrete()
            .map_err(|err| core_error::pyerr_from_location_err(py, err))?;

        // Safety:
        // - we borrow the compressor that's inside PyRef<Self> and Py<Self>
        // - the iterator and its items all carry around clones of Py<Self>
        // - so the compressor lives long enough
        // - Self is a frozen class, so no mutation can occur
        #[expect(unsafe_code)]
        let iter: core_compressor::compressor::ConcreteCompressorIterator<'static> =
            unsafe { std::mem::transmute(iter) };

        let py_compressor: Py<Self> = Py::from(this);

        Ok(ConcreteCompressorIterator {
            compressor: py_compressor,
            iter,
        })
    }
}

#[pyclass(module = "fcbench.compressor", frozen)]
pub struct Codec {
    codec: core_compressor::codec::Codec,
}

#[pymethods]
impl Codec {
    #[getter]
    /// [SIGNATURE]: # "(self) -> type[numcodecs.abc.Codec]"
    pub fn r#type<'py>(
        &self,
        py: Python<'py>,
    ) -> Result<Bound<'py, numcodecs_python::PyCodecClass>, PyErr> {
        self.codec
            .import_py(py)
            .map_err(core_error::LocationError::into_error)
    }

    #[must_use]
    #[getter]
    /// [SIGNATURE]: # "(self) -> str"
    pub fn name(&self) -> &str {
        self.codec.name()
    }

    #[must_use]
    #[getter]
    /// [SIGNATURE]: # "(self) -> str"
    pub const fn import_path(&self) -> &str {
        self.codec.import_path().as_str()
    }

    #[must_use]
    #[getter]
    /// [SIGNATURE]: # "(self) -> str"
    pub fn kind(&self) -> String {
        format!("{}", self.codec.kind())
    }

    #[must_use]
    pub fn __str__(&self) -> String {
        format!("{}", self.codec)
    }
}

#[pyclass(module = "fcbench.compressor")]
// not frozen as the iterator is mutated on iteration
pub struct CodecIterator {
    _compressor: Py<Compressor>,
    // FIXME: remove boxing once impl Trait inside an associated type is stable
    iter: Box<
        dyn ExactSizeIterator<Item = &'static core_compressor::codec::Codec>
            + Send
            + Sync
            + 'static,
    >,
}

#[pymethods]
impl CodecIterator {
    #[must_use]
    pub const fn __iter__(this: PyRef<Self>) -> PyRef<Self> {
        this
    }

    pub fn __next__(&mut self) -> Option<Codec> {
        self.iter.next().map(|codec| Codec {
            codec: codec.clone(),
        })
    }

    #[must_use]
    pub fn __len__(&self) -> usize {
        self.iter.len()
    }
}

#[pyclass(module = "fcbench.compressor", frozen)]
pub struct ConcreteCompressor {
    _compressor: Py<Compressor>,
    pub(crate) concrete: core_compressor::compressor::ConcreteCompressor<'static>,
}

#[pymethods]
impl ConcreteCompressor {
    #[must_use]
    /// [SIGNATURE]: # "(self) -> str"
    pub fn name(&self) -> &str {
        self.concrete.name()
    }

    #[must_use]
    /// [SIGNATURE]: # "(self) -> Optional[Union[str, bytes, PathLike]]"
    pub fn config_path(&self) -> Option<&Path> {
        self.concrete.config_path()
    }

    #[must_use]
    pub fn __str__(&self) -> String {
        format!("{}", self.concrete)
    }

    /// [SIGNATURE]: # "(self) -> Sequence[numcodecs.abc.Codec]"
    pub fn build<'py>(
        &self,
        py: Python<'py>,
    ) -> Result<Vec<Bound<'py, numcodecs_python::PyCodec>>, PyErr> {
        self.concrete
            .build_py(py)
            .map_err(core_error::LocationError::into_error)
    }

    #[must_use]
    #[getter]
    /// [SIGNATURE]: # "(self) -> Iterator[ConcreteCodec]"
    pub fn codecs(this: PyRef<Self>) -> ConcreteCodecIterator {
        let iter = this.concrete.codecs();
        let iter: Box<
            dyn ExactSizeIterator<Item = &core_compressor::codec::ConcreteCodec> + Send + Sync,
        > = Box::new(iter);
        // Safety:
        // - we borrow the compressor that's inside PyRef<Self> and Py<Self>
        // - the iterator and its items all carry around clones of Py<Self>
        // - so the compressor lives long enough
        // - Self is a frozen class, so no mutation can occur
        #[expect(unsafe_code)]
        let iter: Box<
            dyn ExactSizeIterator<Item = &'static core_compressor::codec::ConcreteCodec<'static>>
                + Send
                + Sync
                + 'static,
        > = unsafe { std::mem::transmute(iter) };

        let py_compressor: Py<Self> = Py::from(this);

        ConcreteCodecIterator {
            compressor: py_compressor,
            iter,
        }
    }
}

#[pyclass(module = "fcbench.compressor")]
// not frozen as the iterator is mutated on iteration
pub struct ConcreteCompressorIterator {
    compressor: Py<Compressor>,
    iter: core_compressor::compressor::ConcreteCompressorIterator<'static>,
}

#[pymethods]
impl ConcreteCompressorIterator {
    #[must_use]
    pub const fn __iter__(this: PyRef<Self>) -> PyRef<Self> {
        this
    }

    pub fn __next__(&mut self, py: Python) -> Result<Option<ConcreteCompressor>, PyErr> {
        self.iter
            .next()
            .map(|concrete| match concrete {
                Ok(concrete) => Ok(ConcreteCompressor {
                    _compressor: self.compressor.clone_ref(py),
                    concrete,
                }),
                Err(err) => Err(core_error::pyerr_from_location_err(py, err)),
            })
            .transpose()
    }
}

#[pyclass(module = "fcbench.compressor", frozen)]
pub struct ConcreteCodec {
    _compressor: Py<ConcreteCompressor>,
    concrete: core_compressor::codec::ConcreteCodec<'static>,
}

#[pymethods]
impl ConcreteCodec {
    /// [SIGNATURE]: # "(self) -> numcodecs.abc.Codec"
    pub fn build<'py>(
        &self,
        py: Python<'py>,
    ) -> Result<Bound<'py, numcodecs_python::PyCodec>, PyErr> {
        match self.concrete.build_py(py) {
            Ok(concrete) => Ok(concrete),
            Err(err) => Err(err.into_error()),
        }
    }

    #[must_use]
    #[getter]
    /// [SIGNATURE]: # "(self) -> str"
    pub const fn import_path(&self) -> &str {
        self.concrete.import_path().as_str()
    }

    #[must_use]
    #[getter]
    /// [SIGNATURE]: # "(self) -> str"
    pub fn kind(&self) -> String {
        format!("{}", self.concrete.kind())
    }

    #[must_use]
    pub fn __str__(&self) -> String {
        format!("{}", self.concrete)
    }
}

#[pyclass(module = "fcbench.compressor")]
// not frozen as the iterator is mutated on iteration
pub struct ConcreteCodecIterator {
    compressor: Py<ConcreteCompressor>,
    // FIXME: remove boxing once impl Trait inside an associated type is stable
    iter: Box<
        dyn ExactSizeIterator<Item = &'static core_compressor::codec::ConcreteCodec<'static>>
            + Send
            + Sync
            + 'static,
    >,
}

#[pymethods]
impl ConcreteCodecIterator {
    #[must_use]
    pub const fn __iter__(this: PyRef<Self>) -> PyRef<Self> {
        this
    }

    pub fn __next__(&mut self, py: Python) -> Option<ConcreteCodec> {
        self.iter.next().map(|concrete| ConcreteCodec {
            _compressor: self.compressor.clone_ref(py),
            concrete: concrete.clone(),
        })
    }

    #[must_use]
    pub fn __len__(&self) -> usize {
        self.iter.len()
    }
}

#[pyfunction]
#[expect(clippy::needless_pass_by_value)]
/// Perform compression and decompression on the provided [`xarray.DataArray`]
/// `da` using the `compressor`, and return the decompressed
/// [`xarray.DataArray`] alongside per-codec performance measurements.
///
/// The compression is performed in-memory on a chunk-by-chunk basis.
///
/// Note that compression is applied from left to right, so `compressor[0]`
/// will be applied to encode the data first. Decompression is applied in
/// reverse, from right to left, so `compressor[0]` will be applied to decode
/// the data last.
///
/// [`xarray.DataArray`]: https://docs.xarray.dev/en/v2023.11.0/generated/xarray.DataArray.html
///
/// [SIGNATURE]: # "(da: xarray.DataArray, compressor: Sequence[numcodecs.abc.Codec]) -> Tuple[xarray.DataArray, Sequence[types.CodecPerformanceMeasurement]]"
pub fn compute_dataarray_compress_decompress<'py>(
    py: Python<'py>,
    da: &Bound<'py, PyAny>,
    compressor: Vec<Bound<'py, numcodecs_python::PyCodec>>,
) -> Result<
    (
        Bound<'py, PyAny>,
        Vec<DataclassOutFrozen<core_compressor::compress::CodecPerformanceMeasurement>>,
    ),
    PyErr,
> {
    match core_compressor::compress::DataArrayCompressor::compute_compress_decompress(
        py,
        da.into(),
        &compressor,
    ) {
        Ok((da, measurements)) => Ok((
            da,
            measurements
                .into_iter()
                .map(|measurement| Dataclass::new(measurement).output_frozen(py))
                .collect::<Result<_, _>>()?,
        )),
        Err(err) => Err(err.into_error()),
    }
}

#[pyfunction]
/// Perform compression and decompression on the provided [`numpy.array`]
/// `array` using the `compressor`, and return the decompressed
/// [`numpy.array`] alongside per-codec performance measurements.
///
/// The compression is performed in-memory on the entire array.
///
/// Note that compression is applied from left to right, so `compressor[0]`
/// will be applied to encode the data first. Decompression is applied in
/// reverse, from right to left, so `compressor[0]` will be applied to decode
/// the data last.
///
/// [`numpy.array`]: https://numpy.org/doc/1.26/reference/generated/numpy.array.html
///
/// [SIGNATURE]: # "(array: numpy.array, compressor: Sequence[numcodecs.abc.Codec]) -> Tuple[numpy.array, Sequence[types.CodecPerformanceMeasurement]]"
pub fn compute_numpy_array_compress_decompress<'py>(
    py: Python<'py>,
    array: Bound<'py, PyUntypedArray>,
    compressor: Vec<Bound<'py, numcodecs_python::PyCodec>>,
) -> Result<
    (
        Bound<'py, PyUntypedArray>,
        Vec<DataclassOutFrozen<core_compressor::compress::CodecPerformanceMeasurement>>,
    ),
    PyErr,
> {
    match core_compressor::compress::NumpyArrayCompressor::compress_decompress(
        py, array, compressor,
    ) {
        Ok((array, measurements)) => Ok((
            array,
            measurements
                .into_iter()
                .map(|measurement| Dataclass::new(measurement).output_frozen(py))
                .collect::<Result<_, _>>()?,
        )),
        Err(err) => Err(err.into_error()),
    }
}

#[cfg(test)]
mod tests {
    #[test]
    fn dataclass_registry() {
        let _ = super::dataclass_registry();
    }
}
