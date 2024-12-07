use std::{borrow::Cow, error::Error, fmt};

use pyo3::prelude::*;
use pyo3_error::{err_with_location, IoErrorToPyErr, MapErrorToPyErr, PyErrChain};

#[derive(
    Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Hash, serde::Serialize, serde::Deserialize,
)]
pub struct Location {
    file: Cow<'static, str>,
    line: u32,
    column: u32,
}

impl Location {
    #[must_use]
    #[track_caller]
    pub const fn caller() -> Self {
        let location = std::panic::Location::caller();

        // Ideally, the location would also store the function name, see
        //  https://github.com/rust-lang/rust/issues/95529

        Self {
            file: Cow::Borrowed(location.file()),
            line: location.line(),
            column: location.column(),
        }
    }
}

impl fmt::Display for Location {
    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        write!(fmt, "{}:{}:{}", self.file, self.line, self.column)
    }
}

#[derive(Clone, PartialEq, Eq, PartialOrd, Ord, Hash, serde::Serialize, serde::Deserialize)]
#[serde(transparent)]
pub struct LocationError<E: Error> {
    inner: Box<LocationErrorInner<E>>,
}

impl<E: Error> LocationError<E> {
    #[must_use]
    #[track_caller]
    pub fn new(error: E) -> Self {
        Self {
            inner: Box::new(LocationErrorInner {
                error,
                location: Location::caller(),
            }),
        }
    }

    #[must_use]
    #[track_caller]
    pub fn from2<E2: Into<E>>(error: E2) -> Self {
        Self::new(error.into())
    }
}

impl<E: Error> LocationError<E> {
    #[must_use]
    pub const fn error(&self) -> &E {
        &self.inner.error
    }

    #[must_use]
    pub fn error_mut(&mut self) -> &mut E {
        &mut self.inner.error
    }

    #[must_use]
    pub fn into_error(self) -> E {
        self.inner.error
    }

    #[must_use]
    pub const fn location(&self) -> &Location {
        &self.inner.location
    }

    #[must_use]
    pub fn map<F: Error>(self, map: impl FnOnce(E) -> F) -> LocationError<F> {
        LocationError {
            inner: Box::new(LocationErrorInner {
                error: map(self.inner.error),
                location: self.inner.location,
            }),
        }
    }

    #[must_use]
    pub fn map_ref<'a, F: Error>(&'a self, map: impl FnOnce(&'a E) -> F) -> LocationError<F> {
        LocationError {
            inner: Box::new(LocationErrorInner {
                error: map(&self.inner.error),
                location: self.inner.location.clone(),
            }),
        }
    }
}

impl<E: Error + Into<std::convert::Infallible>> LocationError<E> {
    pub fn infallible(self) -> ! {
        #[expect(unreachable_code)]
        match self.into_error().into() {}
    }
}

impl<E: Error> From<E> for LocationError<E> {
    #[track_caller]
    fn from(error: E) -> Self {
        Self::new(error)
    }
}

impl<E: Error> fmt::Debug for LocationError<E> {
    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        fmt.debug_struct("LocationError")
            .field("error", self.error())
            .field("location", self.location())
            .finish()
    }
}

impl<E: Error> fmt::Display for LocationError<E> {
    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        write!(fmt, "{}, at {}", self.error(), self.location())
    }
}

impl<E: Error> Error for LocationError<E> {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        self.inner.error.source()
    }
}

#[derive(Clone, PartialEq, Eq, PartialOrd, Ord, Hash, serde::Serialize, serde::Deserialize)]
#[serde(rename = "LocationError")]
struct LocationErrorInner<E: Error> {
    error: E,
    location: Location,
}

pub struct AnyError {
    error: Box<dyn Error + Send + Sync>,
}

impl AnyError {
    #[must_use]
    pub fn msg<M: fmt::Display>(msg: M) -> Self {
        Self {
            error: format!("{msg}").into(),
        }
    }

    #[must_use]
    pub fn new<E: 'static + Send + Sync + Error>(err: E) -> Self {
        Self { error: err.into() }
    }

    #[must_use]
    pub fn from2<E: Into<Box<dyn Error + Send + Sync>>>(err: E) -> Self {
        Self { error: err.into() }
    }
}

impl fmt::Display for AnyError {
    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        write!(fmt, "{}", self.error)
    }
}

impl fmt::Debug for AnyError {
    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        write!(fmt, "{:?}", self.error)
    }
}

impl Error for AnyError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        Some(self.error.as_ref())
    }
}

#[inline]
pub fn pyerr_from_location_err<T: Into<Box<dyn Error + 'static>>>(py: Python, err: T) -> PyErr {
    PyErrChain::pyerr_from_err_with_translator::<T, IoErrorToPyErr, MapLocationErrorToPyErr>(
        py, err,
    )
}

pub fn pyerr_chain_from_location_err<T: Into<Box<dyn Error + 'static>>>(
    py: Python,
    err: T,
) -> PyErrChain {
    PyErrChain::new_with_translator::<T, IoErrorToPyErr, MapLocationErrorToPyErr>(py, err)
}

struct MapLocationErrorToPyErr;

impl MapErrorToPyErr for MapLocationErrorToPyErr {
    fn try_map<T: Error + 'static>(
        py: Python,
        err: Box<dyn Error + 'static>,
        map: impl FnOnce(Box<T>) -> PyErr,
    ) -> Result<PyErr, Box<dyn Error + 'static>> {
        let err = match err.downcast::<T>() {
            Ok(err) => return Ok(map(err)),
            Err(err) => err,
        };

        let err = match err.downcast::<LocationError<T>>() {
            Ok(err) => {
                let location = err.location().clone();
                let err = map(Box::new(err.into_error()));
                let err =
                    err_with_location(py, err, &location.file, location.line, location.column);
                return Ok(err);
            },
            Err(err) => err,
        };

        Err(err)
    }

    fn try_map_send_sync<T: Error + 'static>(
        py: Python,
        err: Box<dyn Error + Send + Sync + 'static>,
        map: impl FnOnce(Box<T>) -> PyErr,
    ) -> Result<PyErr, Box<dyn Error + Send + Sync + 'static>> {
        let err = match err.downcast::<T>() {
            Ok(err) => return Ok(map(err)),
            Err(err) => err,
        };

        let err = match err.downcast::<LocationError<T>>() {
            Ok(err) => {
                let location = err.location().clone();
                let err = map(Box::new(err.into_error()));
                let err =
                    err_with_location(py, err, &location.file, location.line, location.column);
                return Ok(err);
            },
            Err(err) => err,
        };

        Err(err)
    }

    fn try_map_ref<T: Error + 'static>(
        py: Python,
        err: &(dyn Error + 'static),
        map: impl FnOnce(&T) -> PyErr,
    ) -> Option<PyErr> {
        if let Some(err) = err.downcast_ref::<T>() {
            return Some(map(err));
        }

        if let Some(err) = err.downcast_ref::<LocationError<T>>() {
            let location = err.location();
            let err = map(err.error());
            let err = err_with_location(py, err, &location.file, location.line, location.column);
            return Some(err);
        }

        None
    }
}
