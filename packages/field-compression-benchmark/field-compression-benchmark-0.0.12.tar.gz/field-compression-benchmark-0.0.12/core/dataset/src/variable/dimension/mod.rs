use std::{num::NonZeroUsize, ops::ControlFlow};

use pyo3::{
    intern,
    prelude::*,
    types::{IntoPyDict, PySlice},
    IntoPyObjectExt,
};

use core_error::LocationError;

mod config;

pub(super) use config::{DataDimensionsSeed, PerVariableDataDimension};

#[derive(Debug, Clone)]
pub struct DataDimension {
    size: NonZeroUsize,
    pub(super) slice: DataSlice,
}

impl DataDimension {
    #[must_use]
    pub const fn new(size: NonZeroUsize, slice: DataSlice) -> Self {
        Self { size, slice }
    }

    #[must_use]
    pub const fn with_size(size: NonZeroUsize) -> Self {
        Self {
            size,
            slice: DataSlice::All { reduce: false },
        }
    }

    #[must_use]
    pub const fn size(&self) -> NonZeroUsize {
        self.size
    }

    #[must_use]
    pub const fn slice(&self) -> &DataSlice {
        &self.slice
    }

    #[must_use]
    pub const fn num_reductions(&self) -> usize {
        match self.slice {
            DataSlice::IntValue { .. }
            | DataSlice::FloatValue { .. }
            | DataSlice::Index { .. }
            | DataSlice::All { reduce: false } => 1,
            DataSlice::All { reduce: true } => self.size.get(),
        }
    }

    #[must_use]
    pub const fn iter_reductions(&self) -> Option<DataDimensionReductionIterator> {
        match self.slice {
            // single-value dimensions are dropped in the slicing
            DataSlice::IntValue { .. } | DataSlice::FloatValue { .. } | DataSlice::Index { .. } => {
                None
            },
            DataSlice::All { reduce: false } => Some(DataDimensionReductionIterator::All),
            DataSlice::All { reduce: true } => Some(DataDimensionReductionIterator::Reduction {
                size: self.size,
                value: 0,
            }),
        }
    }

    pub fn minimise(&mut self) {
        match self.slice {
            DataSlice::IntValue { .. }
            | DataSlice::FloatValue { .. }
            | DataSlice::Index { .. }
            | DataSlice::All { reduce: false } => (),
            DataSlice::All { reduce: true } => self.slice = DataSlice::Index { index: 0 },
        }
    }

    #[must_use]
    pub const fn summary(&self) -> DataDimensionSummary {
        DataDimensionSummary {
            size: self.size,
            slice: self.slice.summary(),
        }
    }
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
#[serde(rename = "DataDimension")]
#[serde(deny_unknown_fields)]
pub struct DataDimensionSummary {
    size: NonZeroUsize,
    slice: DataSliceSummary,
}

#[derive(Debug, Clone)]
pub enum DataSlice {
    IntValue { value: i64 },
    FloatValue { value: f64 },
    Index { index: isize },
    All { reduce: bool },
}

impl DataSlice {
    pub fn sel<'py>(
        &self,
        py: Python<'py>,
        da: Borrowed<'_, 'py, PyAny>,
        dim_name: &str,
    ) -> Result<Bound<'py, PyAny>, LocationError<PyErr>> {
        let (selector, is_index) = match self {
            Self::IntValue { value } => (value.into_bound_py_any(py)?, false),
            Self::FloatValue { value } => (value.into_bound_py_any(py)?, false),
            Self::Index { index } => (index.into_bound_py_any(py)?, true),
            Self::All { .. } => return Ok(da.to_owned()),
        };

        da.call_method(
            if is_index {
                intern!(py, "isel")
            } else {
                intern!(py, "sel")
            },
            ([(dim_name, selector)].into_py_dict(py)?,),
            // https://github.com/pydata/xarray/issues/4073#issuecomment-1163292454
            Some(&[(intern!(py, "drop"), true)].into_py_dict(py)?),
        )
        .map_err(LocationError::new)
    }

    #[must_use]
    pub const fn summary(&self) -> DataSliceSummary {
        let inner = match self {
            Self::IntValue { value } => DataSliceSummaryInner::IntValue {
                r#type: IntType::Int,
                value: *value,
            },
            Self::FloatValue { value } => DataSliceSummaryInner::FloatValue {
                r#type: FloatType::Float,
                value: *value,
            },
            Self::Index { index } => DataSliceSummaryInner::Index { index: *index },
            Self::All { reduce } => DataSliceSummaryInner::All {
                valueset: AllValues::All,
                reduce: *reduce,
            },
        };

        DataSliceSummary { inner }
    }
}

pub enum DataDimensionReductionIterator {
    All,
    Reduction { size: NonZeroUsize, value: usize },
}

impl DataDimensionReductionIterator {
    pub fn next<'py>(
        &mut self,
        py: Python<'py>,
    ) -> ControlFlow<Bound<'py, PyAny>, Bound<'py, PyAny>> {
        match self {
            Self::All => ControlFlow::Break(PySlice::full(py).into_any()),
            Self::Reduction { ref size, value } => {
                let old_value = *value;
                if (old_value + 1) < size.get() {
                    *value += 1;
                    ControlFlow::Continue(match old_value.into_pyobject(py) {
                        Ok(old_value) => old_value.into_any(),
                        Err(err) => match err {},
                    })
                } else {
                    *value = 0;
                    ControlFlow::Break(match old_value.into_pyobject(py) {
                        Ok(old_value) => old_value.into_any(),
                        Err(err) => match err {},
                    })
                }
            },
        }
    }

    #[must_use]
    pub fn get<'py>(&self, py: Python<'py>) -> Bound<'py, PyAny> {
        match self {
            Self::All => PySlice::full(py).into_any(),
            Self::Reduction { value, .. } => match value.into_pyobject(py) {
                Ok(value) => value.into_any(),
                Err(err) => match err {},
            },
        }
    }
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
#[serde(rename = "DataSlice")]
#[serde(transparent)]
pub struct DataSliceSummary {
    inner: DataSliceSummaryInner,
}

#[derive(Debug, Clone, Copy)]
enum DataSliceSummaryInner {
    IntValue { r#type: IntType, value: i64 },
    FloatValue { r#type: FloatType, value: f64 },
    Index { index: isize },
    All { valueset: AllValues, reduce: bool },
}

impl serde::Serialize for DataSliceSummaryInner {
    fn serialize<S: serde::Serializer>(&self, serializer: S) -> Result<S::Ok, S::Error> {
        if serializer.is_human_readable() {
            match *self {
                Self::IntValue { r#type, value } => {
                    DataSliceSummaryInnerHumanReadable::IntValue { r#type, value }
                },
                Self::FloatValue { r#type, value } => {
                    DataSliceSummaryInnerHumanReadable::FloatValue { r#type, value }
                },
                Self::Index { index } => DataSliceSummaryInnerHumanReadable::Index { index },
                Self::All { valueset, reduce } => {
                    DataSliceSummaryInnerHumanReadable::All { valueset, reduce }
                },
            }
            .serialize(serializer)
        } else {
            match *self {
                Self::IntValue { r#type, value } => {
                    DataSliceSummaryInnerBinary::IntValue { r#type, value }
                },
                Self::FloatValue { r#type, value } => {
                    DataSliceSummaryInnerBinary::FloatValue { r#type, value }
                },
                Self::Index { index } => DataSliceSummaryInnerBinary::Index { index },
                Self::All { valueset, reduce } => {
                    DataSliceSummaryInnerBinary::All { valueset, reduce }
                },
            }
            .serialize(serializer)
        }
    }
}

impl<'de> serde::Deserialize<'de> for DataSliceSummaryInner {
    fn deserialize<D: serde::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        if deserializer.is_human_readable() {
            match DataSliceSummaryInnerHumanReadable::deserialize(deserializer)? {
                DataSliceSummaryInnerHumanReadable::IntValue { r#type, value } => {
                    Ok(Self::IntValue { r#type, value })
                },
                DataSliceSummaryInnerHumanReadable::FloatValue { r#type, value } => {
                    Ok(Self::FloatValue { r#type, value })
                },
                DataSliceSummaryInnerHumanReadable::Index { index } => Ok(Self::Index { index }),
                DataSliceSummaryInnerHumanReadable::All { valueset, reduce } => {
                    Ok(Self::All { valueset, reduce })
                },
            }
        } else {
            match DataSliceSummaryInnerBinary::deserialize(deserializer)? {
                DataSliceSummaryInnerBinary::IntValue { r#type, value } => {
                    Ok(Self::IntValue { r#type, value })
                },
                DataSliceSummaryInnerBinary::FloatValue { r#type, value } => {
                    Ok(Self::FloatValue { r#type, value })
                },
                DataSliceSummaryInnerBinary::Index { index } => Ok(Self::Index { index }),
                DataSliceSummaryInnerBinary::All { valueset, reduce } => {
                    Ok(Self::All { valueset, reduce })
                },
            }
        }
    }
}

#[derive(serde::Serialize, serde::Deserialize)]
#[serde(rename = "DataSlice")]
#[serde(untagged)]
enum DataSliceSummaryInnerHumanReadable {
    IntValue {
        r#type: IntType,
        value: i64,
    },
    FloatValue {
        r#type: FloatType,
        value: f64,
    },
    Index {
        index: isize,
    },
    All {
        valueset: AllValues,
        #[serde(default)]
        reduce: bool,
    },
}

#[derive(serde::Serialize, serde::Deserialize)]
#[serde(rename = "DataSlice")]
enum DataSliceSummaryInnerBinary {
    IntValue {
        r#type: IntType,
        value: i64,
    },
    FloatValue {
        r#type: FloatType,
        value: f64,
    },
    Index {
        index: isize,
    },
    All {
        valueset: AllValues,
        #[serde(default)]
        reduce: bool,
    },
}

#[derive(Debug, Clone, Copy, serde::Serialize, serde::Deserialize)]
#[serde(rename = "Type")]
#[serde(rename_all = "lowercase")]
enum IntType {
    Int,
}

#[derive(Debug, Clone, Copy, serde::Serialize, serde::Deserialize)]
#[serde(rename = "Type")]
#[serde(rename_all = "lowercase")]
enum FloatType {
    Float,
}

#[derive(Debug, Clone, Copy, serde::Serialize, serde::Deserialize)]
#[serde(rename_all = "lowercase")]
enum AllValues {
    All,
}
