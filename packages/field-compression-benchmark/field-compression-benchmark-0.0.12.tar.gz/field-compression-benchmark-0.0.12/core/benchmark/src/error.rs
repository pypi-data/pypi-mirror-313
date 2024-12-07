use std::{convert::Infallible, fmt};

use pyo3::prelude::*;
use pyo3_error::PyErrChain;
use thiserror::Error;

use core_error::{pyerr_chain_from_location_err, LocationError};
use core_measure::stats::AnalysisError;

#[derive(Debug, thiserror::Error)]
pub enum BenchmarkSingleCaseError {
    #[error("failed to execute Python code")]
    Python(#[source] LocationError<PyErrChain>),
    #[error("failed to analyse some measurements")]
    Analysis(#[source] LocationError<AnalysisError>),
}

impl From<PyErr> for BenchmarkSingleCaseError {
    #[track_caller]
    fn from(err: PyErr) -> Self {
        Python::with_gil(|py| Self::Python(pyerr_chain_from_location_err(py, err).into()))
    }
}

impl From<AnalysisError> for BenchmarkSingleCaseError {
    #[track_caller]
    fn from(err: AnalysisError) -> Self {
        Self::Analysis(err.into())
    }
}

impl From<Infallible> for BenchmarkSingleCaseError {
    fn from(err: Infallible) -> Self {
        match err {}
    }
}

impl From<LocationError<PyErr>> for BenchmarkSingleCaseError {
    fn from(err: LocationError<PyErr>) -> Self {
        Python::with_gil(|py| Self::Python(err.map(|err| pyerr_chain_from_location_err(py, err))))
    }
}

impl From<LocationError<AnalysisError>> for BenchmarkSingleCaseError {
    fn from(err: LocationError<AnalysisError>) -> Self {
        Self::Analysis(err)
    }
}

impl From<LocationError<Infallible>> for BenchmarkSingleCaseError {
    fn from(err: LocationError<Infallible>) -> Self {
        err.infallible()
    }
}

#[derive(Debug, Clone, Error)]
pub enum BenchmarkCaseError {
    #[error("failed to execute Python code")]
    Python(#[source] LocationError<StringifiedError>),
    #[error("failed to analyse some measurements")]
    Analysis(#[source] LocationError<StringifiedError>),
    #[error("failed to distribute a benchmark case")]
    Distributed(#[source] LocationError<StringifiedError>),
}

// FIXME: eliminate extraneous clones
impl serde::Serialize for BenchmarkCaseError {
    fn serialize<S: serde::Serializer>(&self, serializer: S) -> Result<S::Ok, S::Error> {
        if serializer.is_human_readable() {
            match self {
                Self::Python(source) => BenchmarkCaseErrorHumanReadable::Python(source.clone()),
                Self::Analysis(source) => BenchmarkCaseErrorHumanReadable::Analysis(source.clone()),
                Self::Distributed(source) => {
                    BenchmarkCaseErrorHumanReadable::Distributed(source.clone())
                },
            }
            .serialize(serializer)
        } else {
            match self {
                Self::Python(source) => BenchmarkCaseErrorBinary::Python {
                    python: source.clone(),
                },
                Self::Analysis(source) => BenchmarkCaseErrorBinary::Analysis {
                    analysis: source.clone(),
                },
                Self::Distributed(source) => BenchmarkCaseErrorBinary::Distributed {
                    distributed: source.clone(),
                },
            }
            .serialize(serializer)
        }
    }
}

impl<'de> serde::Deserialize<'de> for BenchmarkCaseError {
    fn deserialize<D: serde::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        if deserializer.is_human_readable() {
            match BenchmarkCaseErrorHumanReadable::deserialize(deserializer)? {
                BenchmarkCaseErrorHumanReadable::Python(source) => Ok(Self::Python(source)),
                BenchmarkCaseErrorHumanReadable::Analysis(source) => Ok(Self::Analysis(source)),
                BenchmarkCaseErrorHumanReadable::Distributed(source) => {
                    Ok(Self::Distributed(source))
                },
            }
        } else {
            match BenchmarkCaseErrorBinary::deserialize(deserializer)? {
                BenchmarkCaseErrorBinary::Python { python } => Ok(Self::Python(python)),
                BenchmarkCaseErrorBinary::Analysis { analysis } => Ok(Self::Analysis(analysis)),
                BenchmarkCaseErrorBinary::Distributed { distributed } => {
                    Ok(Self::Distributed(distributed))
                },
            }
        }
    }
}

#[derive(serde::Serialize, serde::Deserialize)]
#[serde(rename = "BenchmarkCaseError")]
#[serde(rename_all = "kebab-case")]
enum BenchmarkCaseErrorHumanReadable {
    Python(LocationError<StringifiedError>),
    Analysis(LocationError<StringifiedError>),
    Distributed(LocationError<StringifiedError>),
}

#[derive(serde::Serialize, serde::Deserialize)]
#[serde(rename = "BenchmarkCaseError")]
enum BenchmarkCaseErrorBinary {
    Python {
        python: LocationError<StringifiedError>,
    },
    Analysis {
        analysis: LocationError<StringifiedError>,
    },
    Distributed {
        distributed: LocationError<StringifiedError>,
    },
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct StringifiedError {
    message: String,
    source: Option<Box<StringifiedError>>,
}

impl StringifiedError {
    #[must_use]
    pub const fn from_string(message: String) -> Self {
        Self {
            message,
            source: None,
        }
    }

    #[must_use]
    pub fn from_err<E: std::error::Error>(err: E) -> Self {
        let mut chain = Vec::new();

        let mut source = err.source();

        while let Some(err) = source.take() {
            source = err.source();
            chain.push(Self {
                message: format!("{err}"),
                source: None,
            });
        }

        let mut source = None;

        while let Some(mut err) = chain.pop() {
            err.source = source.take();
            source = Some(Box::new(err));
        }

        Self {
            message: format!("{err}"),
            source,
        }
    }

    #[must_use]
    pub fn message(&self) -> &str {
        &self.message
    }
}

impl fmt::Display for StringifiedError {
    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        fmt.write_str(&self.message)
    }
}

impl std::error::Error for StringifiedError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        #[expect(clippy::option_if_let_else)]
        match &self.source {
            None => None,
            Some(source) => Some(source),
        }
    }
}

impl From<BenchmarkSingleCaseError> for BenchmarkCaseError {
    fn from(err: BenchmarkSingleCaseError) -> Self {
        match err {
            BenchmarkSingleCaseError::Python(err) => {
                Self::Python(err.map(StringifiedError::from_err))
            },
            BenchmarkSingleCaseError::Analysis(err) => {
                Self::Analysis(err.map(StringifiedError::from_err))
            },
        }
    }
}
