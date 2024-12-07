#![allow(clippy::missing_errors_doc)] // FIXME

use std::{error::Error, fmt};

use core_error::LocationError;

pub mod measurement;
pub mod stats;

pub trait Measurable {
    type Error: 'static + Send + Sync + Error;

    type Intermediate;
    type Value: Measurement;

    fn start() -> Result<Self::Intermediate, LocationError<Self::Error>>;
    fn end(start: Self::Intermediate) -> Result<Self::Value, LocationError<Self::Error>>;
}

pub trait Measurement: Sized + PartialEq + Copy + fmt::Debug {
    type Error: 'static + Send + Sync + Error;

    fn to_f64(&self) -> f64;
    fn try_from_f64(v: f64) -> Result<Self, LocationError<Self::Error>>;

    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result;
}
