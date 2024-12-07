use std::{borrow::Cow, fmt, ops::ControlFlow};

use nonempty::NonEmpty;
use pyo3::{exceptions::PyValueError, intern, prelude::*, types::PyTuple};
use sorted_vec::SortedSet;
use vecmap::VecMap;

use core_error::LocationError;

use crate::units::{DataUnit, DataUnitSummary, UnitRegistry, UnitRegistryMethods};

mod config;
pub mod derivative;
pub mod dimension;

pub(super) use config::DataVariableSeed;
use derivative::DataDerivative;
use dimension::{DataDimension, DataDimensionReductionIterator};

use self::{derivative::DataDerivativeSummary, dimension::DataDimensionSummary};

#[derive(Debug, Clone)]
pub struct DataVariable {
    name: String,
    long_name: Option<String>,
    units: Option<DataUnit>,
    dtype: DataDType,
    dimensions: VecMap<String, DataDimension>,
    derivatives: SortedSet<NonEmpty<DataDerivative>>,
}

impl DataVariable {
    pub fn extract_from_dataset<'py>(
        py: Python<'py>,
        dataset: Borrowed<'_, 'py, PyAny>,
        unit_registry: Borrowed<'_, 'py, UnitRegistry>,
    ) -> Result<VecMap<String, Self>, LocationError<PyErr>> {
        let mut variables = VecMap::new();

        for name in dataset.try_iter()? {
            let name: String = name?.extract()?;
            let variable = dataset.get_item(&name)?;

            let long_name = match variable.getattr(intern!(py, "long_name")) {
                Ok(long_name) => Some(long_name.extract()?),
                Err(_) => None,
            };
            let units = match variable.getattr(intern!(py, "units")) {
                Ok(units) => Some(unit_registry.resolve(&units.extract::<String>()?)?),
                Err(_) => None,
            };
            let dtype = match variable
                .getattr(intern!(py, "dtype"))?
                .str()?
                .extract::<String>()?
                .as_str()
            {
                "float32" => DataDType::Float32,
                "float64" => DataDType::Float64,
                format => {
                    return Err(PyErr::new::<PyValueError, _>(format!(
                        "unknown variable dtype {format:?}"
                    ))
                    .into())
                },
            };

            let mut dimensions = VecMap::new();
            for dimension in variable
                .getattr(intern!(py, "sizes"))?
                .call_method0(intern!(py, "items"))?
                .try_iter()?
            {
                let (name, size) = dimension?.extract()?;
                dimensions.insert(name, DataDimension::with_size(size));
            }

            variables.insert(
                name.clone(),
                Self {
                    name,
                    long_name,
                    units,
                    dtype,
                    dimensions,
                    derivatives: SortedSet::new(),
                },
            );
        }

        Ok(variables)
    }

    #[must_use]
    pub fn name(&self) -> &str {
        &self.name
    }

    #[must_use]
    pub fn long_name(&self) -> Option<&str> {
        self.long_name.as_deref()
    }

    #[must_use]
    pub const fn units(&self) -> Option<&DataUnit> {
        self.units.as_ref()
    }

    #[must_use]
    pub const fn dtype(&self) -> DataDType {
        self.dtype
    }

    pub fn dimensions(&self) -> impl Iterator<Item = (&str, &DataDimension)> {
        self.dimensions
            .iter()
            .map(|(name, dimension)| (name.as_str(), dimension))
    }

    #[must_use]
    pub fn num_reductions(&self) -> usize {
        self.dimensions
            .values()
            .map(DataDimension::num_reductions)
            .product()
    }

    #[must_use]
    pub fn iter_reductions(&self) -> DataVariableReductionIterator {
        DataVariableReductionIterator {
            _variable: self,
            dimensions: self
                .dimensions
                .values()
                .filter_map(DataDimension::iter_reductions)
                .collect(),
            all_done: false,
        }
    }

    #[must_use]
    pub const fn derivatives(&self) -> &SortedSet<NonEmpty<DataDerivative>> {
        &self.derivatives
    }

    pub fn minimise(&mut self, dimensions: bool, derivatives: bool) {
        if dimensions {
            self.dimensions
                .values_mut()
                .for_each(DataDimension::minimise);
        }

        if derivatives {
            self.derivatives = SortedSet::new();
        }
    }

    #[must_use]
    pub fn summary(&self) -> DataVariableSummary {
        DataVariableSummary {
            name: Cow::Borrowed(self.name.as_str()),
            long_name: self
                .long_name
                .as_ref()
                .map(|long_name| Cow::Borrowed(long_name.as_str())),
            units: self.units.as_ref().map(DataUnit::summary),
            dtype: self.dtype,
            dimensions: self
                .dimensions
                .iter()
                .map(|(name, dimension)| (Cow::Borrowed(name.as_str()), dimension.summary()))
                .collect(),
            derivatives: SortedSet::from_unsorted(
                self.derivatives
                    .iter()
                    .map(|derivatives| NonEmpty {
                        head: derivatives.head.summary(),
                        tail: derivatives
                            .tail
                            .iter()
                            .map(DataDerivative::summary)
                            .collect(),
                    })
                    .collect(),
            ),
        }
    }
}

pub struct DataVariableReductionIterator<'a> {
    _variable: &'a DataVariable,
    dimensions: Vec<DataDimensionReductionIterator>,
    all_done: bool,
}

impl DataVariableReductionIterator<'_> {
    pub fn next<'py>(&mut self, py: Python<'py>) -> Result<Option<Bound<'py, PyTuple>>, PyErr> {
        if self.all_done {
            return Ok(None);
        }

        self.all_done = true;

        let reduction = PyTuple::new(
            py,
            self.dimensions.iter_mut().map(|dimension| {
                if self.all_done {
                    match dimension.next(py) {
                        ControlFlow::Break(dimension) => dimension,
                        ControlFlow::Continue(dimension) => {
                            self.all_done = false;
                            dimension
                        },
                    }
                } else {
                    dimension.get(py)
                }
            }),
        )?;

        Ok(Some(reduction))
    }
}

#[derive(Copy, Clone, Debug, PartialEq, Eq, Hash, serde::Serialize, serde::Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum DataDType {
    Float32,
    Float64,
}

impl fmt::Display for DataDType {
    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Self::Float32 => fmt.write_str("float32"),
            Self::Float64 => fmt.write_str("float64"),
        }
    }
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
#[serde(rename = "DataVariable")]
#[serde(deny_unknown_fields)]
pub struct DataVariableSummary<'a> {
    #[serde(borrow)]
    name: Cow<'a, str>,
    #[serde(borrow)]
    long_name: Option<Cow<'a, str>>,
    #[serde(borrow)]
    units: Option<DataUnitSummary<'a>>,
    dtype: DataDType,
    #[serde(borrow)]
    dimensions: VecMap<Cow<'a, str>, DataDimensionSummary>,
    #[serde(serialize_with = "derivative::serialize")]
    #[serde(deserialize_with = "derivative::deserialize")]
    derivatives: SortedSet<NonEmpty<DataDerivativeSummary<'a>>>,
}
