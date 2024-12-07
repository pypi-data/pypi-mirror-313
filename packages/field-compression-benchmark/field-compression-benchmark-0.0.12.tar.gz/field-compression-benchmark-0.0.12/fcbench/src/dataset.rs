use std::{
    collections::{HashMap, HashSet},
    path::{Path, PathBuf},
};

use pyo3::{
    exceptions::PyKeyError,
    prelude::*,
    types::{PyDict, PyList},
};
use vecmap::VecSet;

use crate::dataclass::{Dataclass, DataclassOut, DataclassOutFrozen, DataclassRegistry};

pub fn create_module(py: Python) -> Result<Bound<PyModule>, PyErr> {
    let module = PyModule::new(py, "dataset")?;

    module.add_class::<Dataset>()?;
    module.add_class::<DataVariable>()?;
    module.add_function(wrap_pyfunction!(settings, &module)?)?;

    let types = PyModule::new(py, "types")?;
    dataclass_registry().export(py, types.as_borrowed())?;
    module.add_submodule(&types)?;

    Ok(module)
}

fn dataclass_registry() -> DataclassRegistry {
    let mut registry = DataclassRegistry::new();

    registry.insert::<core_dataset::dataset::DatasetSettings>();
    registry.insert::<core_dataset::units::DataUnitSummary>();

    registry
}

#[pyclass(module = "fcbench.dataset", frozen)]
pub struct Dataset {
    pub(crate) dataset: core_dataset::dataset::Dataset,
}

#[pymethods]
impl Dataset {
    #[expect(clippy::needless_pass_by_value)]
    #[staticmethod]
    #[pyo3(signature = (unit_registry, settings, **kwargs))]
    /// [SIGNATURE]: # "(unit_registry: pint.UnitRegistry, settings: types.DatasetSettings, **kwargs) -> Dataset"
    pub fn from_config_kwargs<'py>(
        py: Python<'py>,
        unit_registry: &Bound<'py, core_dataset::units::UnitRegistry>,
        settings: Dataclass<core_dataset::dataset::DatasetSettings>,
        kwargs: Option<Bound<'py, PyDict>>,
    ) -> Result<Self, PyErr> {
        let kwargs = kwargs.unwrap_or_else(|| PyDict::new(py));

        let mut depythonizer = pythonize::Depythonizer::from_object(kwargs.as_any());

        match core_dataset::dataset::Dataset::from_deserialised_config(
            py,
            &mut depythonizer,
            unit_registry.as_borrowed(),
            &settings,
        ) {
            Ok(dataset) => Ok(Self { dataset }),
            Err(err) => Err(PyErr::from(err)),
        }
    }

    #[expect(clippy::needless_pass_by_value)]
    #[staticmethod]
    /// [SIGNATURE]: # "(config: str, unit_registry: pint.UnitRegistry, settings: types.DatasetSettings) -> Dataset"
    pub fn from_config_str<'py>(
        py: Python<'py>,
        config: &str,
        unit_registry: &Bound<'py, core_dataset::units::UnitRegistry>,
        settings: Dataclass<core_dataset::dataset::DatasetSettings>,
    ) -> Result<Self, PyErr> {
        match core_dataset::dataset::Dataset::from_config_str(
            py,
            config,
            unit_registry.as_borrowed(),
            &settings,
        ) {
            Ok(dataset) => Ok(Self { dataset }),
            Err(err) => Err(core_error::pyerr_from_location_err(py, err)),
        }
    }

    #[expect(clippy::needless_pass_by_value)]
    #[staticmethod]
    /// [SIGNATURE]: # "(config_file: Union[str, bytes, PathLike], unit_registry: pint.UnitRegistry, settings: types.DatasetSettings) -> Dataset"
    pub fn from_config_file<'py>(
        py: Python<'py>,
        config_file: PathBuf,
        unit_registry: &Bound<'py, core_dataset::units::UnitRegistry>,
        settings: Dataclass<core_dataset::dataset::DatasetSettings>,
    ) -> Result<Self, PyErr> {
        match core_dataset::dataset::Dataset::from_config_file(
            py,
            &config_file,
            unit_registry.as_borrowed(),
            &settings,
        ) {
            Ok(dataset) => Ok(Self { dataset }),
            Err(err) => Err(core_error::pyerr_from_location_err(py, err)),
        }
    }

    #[expect(clippy::needless_pass_by_value)]
    #[staticmethod]
    /// [SIGNATURE]: # "(config_files: Set[Union[str, Path, PathLike]], unit_registry: pint.UnitRegistry, settings: types.DatasetSettings) -> Mapping[str, Dataset]"
    pub fn from_config_files<'py>(
        py: Python<'py>,
        config_files: HashSet<PathBuf>,
        unit_registry: &Bound<'py, core_dataset::units::UnitRegistry>,
        settings: Dataclass<core_dataset::dataset::DatasetSettings>,
    ) -> Result<HashMap<PathBuf, Self>, PyErr> {
        match core_dataset::dataset::Dataset::from_config_files(
            py,
            &VecSet::from_iter(config_files),
            unit_registry.as_borrowed(),
            &settings,
        ) {
            Ok(datasets) => Ok(datasets
                .into_iter()
                .map(|(path, dataset)| (path, Self { dataset }))
                .collect()),
            Err(err) => Err(core_error::pyerr_from_location_err(py, err)),
        }
    }

    #[expect(clippy::needless_pass_by_value)]
    #[staticmethod]
    /// [SIGNATURE]: # "(config_directory: Union[str, Path, PathLike], unit_registry: pint.UnitRegistry, settings: types.DatasetSettings) -> Mapping[str, Dataset]"
    pub fn from_config_directory<'py>(
        py: Python<'py>,
        config_directory: PathBuf,
        unit_registry: &Bound<'py, core_dataset::units::UnitRegistry>,
        settings: Dataclass<core_dataset::dataset::DatasetSettings>,
    ) -> Result<HashMap<PathBuf, Self>, PyErr> {
        match core_dataset::dataset::Dataset::from_config_directory(
            py,
            &config_directory,
            unit_registry.as_borrowed(),
            &settings,
        ) {
            Ok(datasets) => Ok(datasets
                .into_iter()
                .map(|(path, dataset)| (path, Self { dataset }))
                .collect()),
            Err(err) => Err(core_error::pyerr_from_location_err(py, err)),
        }
    }

    #[must_use]
    #[getter]
    /// [SIGNATURE]: # "(self) -> Optional[str]"
    pub fn config_path(&self) -> Option<&Path> {
        self.dataset.config_path()
    }

    #[must_use]
    #[getter]
    /// [SIGNATURE]: # "(self) -> str"
    pub fn path(&self) -> &Path {
        self.dataset.path()
    }

    #[must_use]
    #[getter]
    /// [SIGNATURE]: # "(self) -> str"
    pub fn format(&self) -> String {
        format!("{}", self.dataset.format())
    }

    /// [SIGNATURE]: # "(self, variables: bool, dimensions: bool, derivatives: bool) -> Dataset"
    pub fn minimise(&self, variables: bool, dimensions: bool, derivatives: bool) -> Self {
        // copy on write since Self is a frozen PyO3 class
        let mut this = Self {
            dataset: self.dataset.clone(),
        };
        this.dataset.minimise(variables, dimensions, derivatives);
        this
    }

    /// [SIGNATURE]: # "(self, keep_variable: Callable[[str], bool]) -> Dataset"
    pub fn filter(&self, keep_variable: &Bound<PyAny>) -> Result<Self, PyErr> {
        // copy on write since Self is a frozen PyO3 class
        let mut this = Self {
            dataset: self.dataset.clone(),
        };

        let mut result = Ok(());

        let keep_variable = |variable: &str| {
            // if an error occurs, we don't filter out any more items to
            //  keep the dataset the same, as if we had returned early
            if result.is_err() {
                return true;
            }

            match keep_variable.call1((variable,)).and_then(|k| k.extract()) {
                Ok(keep) => keep,
                Err(err) => {
                    result = Err(err);
                    true
                },
            }
        };

        this.dataset.filter(keep_variable);

        result.map(|()| this)
    }

    /// [SIGNATURE]: # "(self) -> xarray.Dataset"
    pub fn open_xarray<'py>(&self, py: Python<'py>) -> Result<Bound<'py, PyAny>, PyErr> {
        self.dataset
            .open_xarray(py)
            .map_err(core_error::LocationError::into_error)
    }

    /// [SIGNATURE]: # "(self, variable: str) -> xarray.DataArray"
    pub fn open_xarray_sliced_variable<'py>(
        &self,
        py: Python<'py>,
        variable: &DataVariable,
    ) -> Result<Bound<'py, PyAny>, PyErr> {
        self.dataset
            .open_xarray_sliced_variable(py, &variable.variable)
            .map_err(core_error::LocationError::into_error)
    }

    #[must_use]
    #[getter]
    /// [SIGNATURE]: # "(self) -> Mapping[str, DataVariable]"
    pub fn variables(this: PyRef<Self>) -> DataVariableIterator {
        let iter = this.dataset.variables();
        let iter: Box<
            dyn ExactSizeIterator<Item = &core_dataset::variable::DataVariable> + Send + Sync,
        > = Box::new(iter);
        // Safety:
        // - we borrow the dataset that's inside PyRef<Self> and Py<Self>
        // - the iterator and its items all carry around clones of Py<Self>
        // - so the dataset lives long enough
        // - Self is a frozen class, so no mutation can occur
        #[expect(unsafe_code)]
        let iter: Box<
            dyn ExactSizeIterator<Item = &'static core_dataset::variable::DataVariable>
                + Send
                + Sync
                + 'static,
        > = unsafe { std::mem::transmute(iter) };

        let py_dataset: Py<Self> = Py::from(this);

        DataVariableIterator {
            dataset: py_dataset,
            iter,
        }
    }

    #[getter]
    /// [SIGNATURE]: # "(self) -> Sequence[str]"
    pub fn ignored_variables<'py>(&self, py: Python<'py>) -> Result<Bound<'py, PyList>, PyErr> {
        PyList::new(py, self.dataset.ignored_variables())
    }
}

#[pyfunction]
/// [SIGNATURE]: # "(**kwargs) -> types.DatasetSettings"
#[pyo3(signature = (**kwargs))]
fn settings<'py>(
    py: Python<'py>,
    kwargs: Option<Bound<'py, PyDict>>,
) -> Result<DataclassOut<core_dataset::dataset::DatasetSettings>, PyErr> {
    DataclassOut::new(
        &*kwargs
            .unwrap_or_else(|| PyDict::new(py))
            .extract::<Dataclass<_>>()?,
        py,
    )
}

#[pyclass(module = "fcbench.dataset", frozen)]
pub struct DataVariable {
    pub(crate) variable: core_dataset::variable::DataVariable,
}

#[pymethods]
impl DataVariable {
    #[must_use]
    #[getter]
    /// [SIGNATURE]: # "(self) -> str"
    pub fn name(&self) -> &str {
        self.variable.name()
    }

    #[must_use]
    #[getter]
    /// [SIGNATURE]: # "(self) -> Optional[str]"
    pub fn long_name(&self) -> Option<&str> {
        self.variable.long_name()
    }

    #[getter]
    /// [SIGNATURE]: # "(self) -> Optional[types.DataUnit]"
    pub fn units(
        &self,
        py: Python,
    ) -> Result<Option<DataclassOutFrozen<core_dataset::units::DataUnitSummary>>, PyErr> {
        self.variable
            .units()
            .map(|unit| DataclassOutFrozen::new(&unit.summary(), py))
            .transpose()
    }

    #[must_use]
    #[getter]
    /// [SIGNATURE]: # "(self) -> str"
    pub fn dtype(&self) -> String {
        format!("{}", self.variable.dtype())
    }
}

#[pyclass(module = "fcbench.compressor", mapping)]
// not frozen as the iterator is mutated on iteration
pub struct DataVariableIterator {
    dataset: Py<Dataset>,
    // FIXME: remove boxing once impl Trait inside an associated type is stable
    iter: Box<
        dyn ExactSizeIterator<Item = &'static core_dataset::variable::DataVariable>
            + Send
            + Sync
            + 'static,
    >,
}

#[pymethods]
impl DataVariableIterator {
    pub const fn __iter__(this: PyRef<Self>) -> PyRef<Self> {
        this
    }

    pub fn __next__(&mut self) -> Option<DataVariable> {
        self.iter.next().map(|variable| DataVariable {
            variable: variable.clone(),
        })
    }

    #[must_use]
    pub fn __len__(&self) -> usize {
        self.iter.len()
    }

    pub fn __contains__(&self, py: Python, name: &str) -> Result<bool, PyErr> {
        let dataset: PyRef<Dataset> = self.dataset.try_borrow(py)?;
        let dataset: &Dataset = &dataset;

        Ok(dataset.dataset.get_variable(name).is_some())
    }

    pub fn __getitem__(&self, py: Python, name: &str) -> Result<DataVariable, PyErr> {
        let dataset: PyRef<Dataset> = self.dataset.try_borrow(py)?;
        let dataset: &Dataset = &dataset;

        dataset.dataset.get_variable(name).map_or_else(
            || Err(PyKeyError::new_err(String::from(name))),
            |variable| {
                Ok(DataVariable {
                    variable: variable.clone(),
                })
            },
        )
    }
}

#[cfg(test)]
mod tests {
    #[test]
    fn dataclass_registry() {
        let _ = super::dataclass_registry();
    }
}
