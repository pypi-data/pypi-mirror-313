use std::{borrow::Cow, collections::HashSet, path::PathBuf};

use pyo3::{
    exceptions::{PyKeyError, PyTypeError},
    prelude::*,
    sync::GILOnceCell,
    types::PyDict,
};

use crate::{
    compressor::ConcreteCompressor,
    dataclass::{Dataclass, DataclassOut, DataclassRegistry},
    dataset::Dataset,
};

pub fn create_module(py: Python) -> Result<Bound<PyModule>, PyErr> {
    let module = PyModule::new(py, "benchmark")?;

    module.add_class::<BenchmarkCase>()?;
    module.add_class::<BenchmarkCaseId>()?;
    module.add_class::<BenchmarkCaseFilter>()?;
    module.add_function(wrap_pyfunction!(report, &module)?)?;
    module.add_function(wrap_pyfunction!(settings, &module)?)?;

    let types = PyModule::new(py, "types")?;
    dataclass_registry().export(py, types.as_borrowed())?;
    module.add_submodule(&types)?;

    Ok(module)
}

fn dataclass_registry() -> DataclassRegistry {
    let mut registry = DataclassRegistry::new();

    registry.insert::<core_benchmark::settings::BenchmarkSettings>();
    registry.insert::<core_benchmark::error::BenchmarkCaseError>();
    registry.insert::<core_benchmark::report::BenchmarkCaseReport>();
    registry.insert_with_sample(&core_benchmark::case::BenchmarkCaseId::from_uuid(
        uuid::Uuid::nil(),
    ));
    registry.insert::<core_benchmark::report::BenchmarkReport>();

    // FIXME: remove once supported in serde-reflection:
    // https://github.com/zefchain/serde-reflection/pull/41
    registry.insert::<Result<
        core_benchmark::report::BenchmarkCaseOutput,
        core_benchmark::error::BenchmarkCaseError,
    >>();
    registry.insert::<core_compressor::codec::CodecKind>();
    registry.insert::<core_compressor::parameter::ConcreteParameterSummary>();
    registry.insert::<core_dataset::dataset::DatasetFormat>();
    registry.insert::<core_dataset::variable::DataDType>();
    registry.insert::<core_dataset::variable::derivative::DataDerivativeSummary>();
    registry.insert::<core_dataset::variable::dimension::DataSliceSummary>();

    registry
}

#[pyclass(module = "fcbench.benchmark", frozen)]
pub struct BenchmarkCase {
    dataset: Py<crate::dataset::Dataset>,
    variable: Py<crate::dataset::DataVariable>,
    compressor: Py<crate::compressor::ConcreteCompressor>,
}

#[pymethods]
impl BenchmarkCase {
    #[new]
    pub fn new(
        py: Python,
        dataset: PyRef<Dataset>,
        variable: &str,
        compressor: PyRef<ConcreteCompressor>,
    ) -> Result<Self, PyErr> {
        let Some(variable) = dataset.dataset.get_variable(variable) else {
            return Err(PyKeyError::new_err(String::from(variable)));
        };

        let variable = crate::dataset::DataVariable {
            variable: variable.clone(),
        };

        Ok(Self {
            dataset: dataset.into(),
            variable: Py::new(py, variable)?,
            compressor: compressor.into(),
        })
    }

    #[getter]
    /// [SIGNATURE]: # "(self) -> BenchmarkCaseId"
    pub fn id(&self, py: Python) -> Result<BenchmarkCaseId, PyErr> {
        self.with_case(py, |case| Ok(BenchmarkCaseId { id: case.get_id() }))
    }

    #[getter]
    /// [SIGNATURE]: # "(self) -> UUID"
    pub fn uuid<'py>(&self, py: Python<'py>) -> Result<Bound<'py, PyAny>, PyErr> {
        self.with_case(py, |case| {
            let uuid = case.get_uuid();

            uuid_class(py)?.call1((format!("{uuid}"),))
        })
    }

    #[expect(clippy::needless_pass_by_value)]
    /// [SIGNATURE]: # "(settings: types.BenchmarkSettings) -> types.BenchmarkCaseReport"
    pub fn benchmark(
        &self,
        py: Python,
        settings: Dataclass<core_benchmark::settings::BenchmarkSettings>,
    ) -> Result<DataclassOut<core_benchmark::report::BenchmarkCaseReport>, PyErr> {
        let dataset: &core_dataset::dataset::Dataset = &self.dataset.try_borrow(py)?.dataset;
        let variable: &core_dataset::variable::DataVariable =
            &self.variable.try_borrow(py)?.variable;
        let compressor: &core_compressor::compressor::ConcreteCompressor =
            &self.compressor.try_borrow(py)?.concrete;

        match core_benchmark::run_benchmark_case(py, dataset, variable, compressor, &settings) {
            Ok(result) => DataclassOut::new(
                &core_benchmark::report::BenchmarkCaseReport {
                    dataset: Cow::Borrowed(dataset.path()),
                    format: dataset.format(),
                    variable: variable.summary(),
                    compressor: compressor.summary(),
                    result: Ok(result),
                },
                py,
            ),
            Err(err) => Err(core_error::pyerr_from_location_err(py, err)),
        }
    }
}

impl BenchmarkCase {
    fn with_case<Q>(
        &self,
        py: Python,
        inner: impl FnOnce(core_benchmark::case::BenchmarkCase) -> Result<Q, PyErr>,
    ) -> Result<Q, PyErr> {
        inner(core_benchmark::case::BenchmarkCase {
            dataset: &self.dataset.try_borrow(py)?.dataset,
            variable: &self.variable.try_borrow(py)?.variable,
            compressor: Cow::Borrowed(&self.compressor.try_borrow(py)?.concrete),
        })
    }
}

#[pyclass(module = "fcbench.benchmark", frozen)]
#[derive(PartialEq, Eq, Hash)]
pub struct BenchmarkCaseId {
    id: core_benchmark::case::BenchmarkCaseId,
}

#[pymethods]
impl BenchmarkCaseId {
    #[staticmethod]
    /// [SIGNATURE]: # "(self, uuid: UUID) -> BenchmarkCaseId"
    pub fn from_uuid<'py>(py: Python<'py>, uuid: &Bound<'py, PyAny>) -> Result<Self, PyErr> {
        if !uuid.is_instance(uuid_class(py)?)? {
            return Err(PyErr::new::<PyTypeError, _>(
                "uuid is not an instance of uuid.UUID",
            ));
        }

        let uuid: String = uuid.str()?.extract()?;
        let uuid = uuid
            .parse()
            .map_err(|err| core_error::pyerr_from_location_err(py, err))?;

        Ok(Self {
            id: core_benchmark::case::BenchmarkCaseId::from_uuid(uuid),
        })
    }

    #[getter]
    /// [SIGNATURE]: # "(self) -> UUID"
    pub fn uuid<'py>(&self, py: Python<'py>) -> Result<Bound<'py, PyAny>, PyErr> {
        let uuid = self.id.into_uuid();

        uuid_class(py)?.call1((format!("{uuid}"),))
    }
}

fn uuid_class(py: Python) -> Result<&Bound<PyAny>, PyErr> {
    static UUID: GILOnceCell<Py<PyAny>> = GILOnceCell::new();
    UUID.import(py, "uuid", "UUID")
}

impl<'py> FromPyObject<'py> for BenchmarkCaseId {
    fn extract_bound(object: &Bound<'py, PyAny>) -> Result<Self, PyErr> {
        if let Ok(id) = object.downcast::<Self>() {
            let id: PyRef<Self> = id.try_borrow()?;
            let id: &Self = &id;
            return Ok(Self { id: id.id });
        }

        Self::from_uuid(object.py(), object)
    }
}

#[pyclass(module = "fcbench.benchmark", frozen)]
pub struct BenchmarkCaseFilter {
    filter: core_benchmark::case::BenchmarkCaseFilter,
}

#[pymethods]
impl BenchmarkCaseFilter {
    #[new]
    /// [SIGNATURE]: # "(ids: Set[Union[BenchmarkCaseId, UUID]]) -> BenchmarkCaseFilter"
    pub fn new(py: Python, ids: HashSet<BenchmarkCaseId>) -> Result<Self, PyErr> {
        Ok(Self {
            filter: core_benchmark::case::BenchmarkCaseFilter::new(
                ids.into_iter().map(|id| id.id).collect(),
            )
            .map_err(|err| core_error::pyerr_from_location_err(py, err))?,
        })
    }

    #[must_use]
    pub fn __len__(&self) -> usize {
        self.filter.len()
    }

    #[must_use]
    pub fn __iter__(this: PyRef<Self>) -> BenchmarkCaseFilterIterator {
        let iter = this.filter.iter();
        let iter: Box<
            dyn ExactSizeIterator<Item = core_benchmark::case::BenchmarkCaseId> + Send + Sync,
        > = Box::new(iter);
        // Safety:
        // - we borrow the filter that's inside PyRef<Self> and Py<Self>
        // - the iterator carries around clones of Py<Self>
        // - the iterator items contain no lifetimes
        // - so the dataset lives long enough
        // - Self is a frozen class, so no mutation can occur
        #[expect(unsafe_code)]
        let iter: Box<
            dyn ExactSizeIterator<Item = core_benchmark::case::BenchmarkCaseId>
                + Send
                + Sync
                + 'static,
        > = unsafe { std::mem::transmute(iter) };

        let py_filter: Py<Self> = Py::from(this);

        BenchmarkCaseFilterIterator {
            filter: py_filter,
            iter,
        }
    }

    #[must_use]
    #[expect(clippy::needless_pass_by_value)]
    pub fn __contains__(&self, id: BenchmarkCaseId) -> bool {
        self.filter.contains_case_id(&id.id)
    }

    #[must_use]
    #[expect(clippy::needless_pass_by_value)]
    /// [SIGNATURE]: # "(self, dataset: Union[str, bytes, PathLike]) -> bool"
    pub fn contains_dataset(&self, dataset: PathBuf) -> bool {
        self.filter.contains_dataset(&dataset)
    }

    #[must_use]
    /// [SIGNATURE]: # "(self, variable: str) -> bool"
    pub fn contains_variable(&self, variable: &str) -> bool {
        self.filter.contains_variable(variable)
    }

    #[must_use]
    #[expect(clippy::needless_pass_by_value)]
    /// [SIGNATURE]: # "(self, compressor: Union[str, bytes, PathLike]) -> bool"
    pub fn contains_compressor(&self, compressor: PathBuf) -> bool {
        self.filter.contains_compressor(&compressor)
    }

    #[must_use]
    pub fn contains_codec_params(
        &self,
        codec_params: &crate::compressor::ConcreteCompressor,
    ) -> bool {
        self.filter.contains_codec_params(&codec_params.concrete)
    }

    /// [SIGNATURE]: # "(self, case: BenchmarkCase) -> bool"
    pub fn contains_case(&self, py: Python, case: &BenchmarkCase) -> Result<bool, PyErr> {
        case.with_case(py, |case| Ok(self.filter.contains_case(&case)))
    }
}

#[pyclass(module = "fcbench.benchmark")]
// not frozen as the iterator is mutated on iteration
pub struct BenchmarkCaseFilterIterator {
    filter: Py<BenchmarkCaseFilter>,
    // FIXME: remove boxing once impl Trait inside an associated type is stable
    iter: Box<
        dyn ExactSizeIterator<Item = core_benchmark::case::BenchmarkCaseId> + Send + Sync + 'static,
    >,
}

#[pymethods]
impl BenchmarkCaseFilterIterator {
    pub const fn __iter__(this: PyRef<Self>) -> PyRef<Self> {
        this
    }

    pub fn __next__(&mut self) -> Option<BenchmarkCaseId> {
        self.iter.next().map(|id| BenchmarkCaseId { id })
    }

    #[must_use]
    pub fn __len__(&self) -> usize {
        self.iter.len()
    }

    #[expect(clippy::needless_pass_by_value)]
    pub fn __contains__(&self, py: Python, id: BenchmarkCaseId) -> Result<bool, PyErr> {
        let filter: PyRef<BenchmarkCaseFilter> = self.filter.try_borrow(py)?;
        let filter: &BenchmarkCaseFilter = &filter;

        Ok(filter.filter.contains_case_id(&id.id))
    }
}

#[pyfunction]
#[pyo3(signature = (**kwargs))]
/// [SIGNATURE]: # "(**kwargs) -> types.BenchmarkSettings"
fn settings<'py>(
    py: Python<'py>,
    kwargs: Option<Bound<'py, PyDict>>,
) -> Result<DataclassOut<core_benchmark::settings::BenchmarkSettings>, PyErr> {
    DataclassOut::new(
        &*kwargs
            .unwrap_or_else(|| PyDict::new(py))
            .extract::<Dataclass<_>>()?,
        py,
    )
}

#[pyfunction]
#[pyo3(signature = (**kwargs))]
/// [SIGNATURE]: # "(**kwargs) -> types.BenchmarkReport"
fn report<'py>(
    py: Python<'py>,
    kwargs: Option<Bound<'py, PyDict>>,
) -> Result<DataclassOut<core_benchmark::report::BenchmarkReport<'py>>, PyErr> {
    DataclassOut::new(
        &*kwargs
            .unwrap_or_else(|| PyDict::new(py))
            .extract::<Dataclass<_>>()?,
        py,
    )
}

#[cfg(test)]
mod tests {
    #[test]
    fn dataclass_registry() {
        let _ = super::dataclass_registry();
    }
}
