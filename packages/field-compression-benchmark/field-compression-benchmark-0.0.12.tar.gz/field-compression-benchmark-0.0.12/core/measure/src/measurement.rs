#[cfg(not(target_os = "emscripten"))]
use std::time::Instant;
use std::{
    convert::Infallible,
    fmt,
    time::{Duration, TryFromFloatSecsError},
};

use core_error::{AnyError, LocationError};

use crate::{Measurable, Measurement};

pub struct WallTime;

impl Measurable for WallTime {
    type Error = Infallible;
    type Intermediate = Instant;
    type Value = Duration;

    fn start() -> Result<Self::Intermediate, LocationError<Self::Error>> {
        Ok(Instant::now())
    }

    fn end(start: Self::Intermediate) -> Result<Self::Value, LocationError<Self::Error>> {
        Ok(Instant::elapsed(&start))
    }
}

#[cfg(target_os = "emscripten")]
#[derive(Debug)]
pub struct Instant {
    now_ms: f64,
}

#[cfg(target_os = "emscripten")]
impl Instant {
    #[must_use]
    pub fn now() -> Self {
        extern "C" {
            pub fn emscripten_get_now() -> f64;
        }

        #[expect(unsafe_code)]
        let now_ms = unsafe { emscripten_get_now() };

        Self { now_ms }
    }

    #[must_use]
    #[expect(clippy::similar_names)]
    pub fn elapsed(start: &Self) -> Duration {
        let end = Self::now();

        let delta_ms = end.now_ms - start.now_ms;

        #[expect(
            clippy::cast_precision_loss,
            clippy::cast_possible_truncation,
            clippy::cast_sign_loss
        )]
        let delta_ns = (delta_ms * 1e6) as u64;

        Duration::from_nanos(delta_ns)
    }
}

impl Measurement for Duration {
    type Error = TryFromFloatSecsError;

    fn to_f64(&self) -> f64 {
        self.as_secs_f64()
    }

    fn try_from_f64(seconds: f64) -> Result<Self, LocationError<Self::Error>> {
        Self::try_from_secs_f64(seconds).map_err(LocationError::new)
    }

    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        fmt.write_fmt(format_args!("{self:?}"))
    }
}

#[derive(Copy, Clone, Debug, PartialEq, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ThroughputPerSecond {
    throughput: f64,
}

impl ThroughputPerSecond {
    #[must_use]
    pub fn new(timing: Duration, decoded_bytes: usize) -> Self {
        if timing == Duration::ZERO {
            // it is better to return zero than to divide by it
            Self::zero()
        } else {
            #[expect(clippy::cast_precision_loss)]
            Self {
                throughput: (decoded_bytes as f64) / timing.as_secs_f64(),
            }
        }
    }

    #[must_use]
    pub const fn zero() -> Self {
        Self { throughput: 0.0 }
    }
}

impl Measurement for ThroughputPerSecond {
    type Error = Infallible;

    fn to_f64(&self) -> f64 {
        self.throughput
    }

    fn try_from_f64(throughput: f64) -> Result<Self, LocationError<Self::Error>> {
        Ok(Self { throughput })
    }

    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        fmt.write_fmt(format_args!(
            "{}/s",
            human_bytes::human_bytes(self.throughput)
        ))
    }
}

#[derive(Copy, Clone, Debug, PartialEq, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct InstructionsPerByte {
    ratio: f64,
}

impl InstructionsPerByte {
    #[must_use]
    pub fn new(instructions: u64, decoded_bytes: usize) -> Self {
        #[expect(clippy::cast_precision_loss)]
        Self {
            ratio: (instructions as f64) / (decoded_bytes as f64),
        }
    }
}

impl Measurement for InstructionsPerByte {
    type Error = Infallible;

    fn to_f64(&self) -> f64 {
        self.ratio
    }

    fn try_from_f64(ratio: f64) -> Result<Self, LocationError<Self::Error>> {
        Ok(Self { ratio })
    }

    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        fmt.write_fmt(format_args!("{:.1} #/B", self.ratio))
    }
}

#[derive(Copy, Clone, Debug, PartialEq, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Bytes {
    bytes: f64,
}

impl Measurement for Bytes {
    type Error = Infallible;

    fn to_f64(&self) -> f64 {
        self.bytes
    }

    fn try_from_f64(bytes: f64) -> Result<Self, LocationError<Self::Error>> {
        Ok(Self { bytes })
    }

    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        fmt.write_str(&human_bytes::human_bytes(self.bytes))
    }
}

impl From<usize> for Bytes {
    fn from(bytes: usize) -> Self {
        #[expect(clippy::cast_precision_loss)]
        Self {
            bytes: bytes as f64,
        }
    }
}

#[derive(Copy, Clone, Debug, PartialEq, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct CompressionRatio {
    ratio: f64,
}

impl CompressionRatio {
    #[must_use]
    pub fn new(decoded_bytes: usize, encoded_bytes: usize) -> Self {
        if decoded_bytes == encoded_bytes {
            Self { ratio: 1.0 }
        } else {
            #[expect(clippy::cast_precision_loss)]
            Self {
                ratio: (decoded_bytes as f64) / (encoded_bytes as f64),
            }
        }
    }

    #[must_use]
    pub const fn unchanged() -> Self {
        Self { ratio: 1.0 }
    }
}

impl Measurement for CompressionRatio {
    type Error = Infallible;

    fn to_f64(&self) -> f64 {
        self.ratio
    }

    fn try_from_f64(ratio: f64) -> Result<Self, LocationError<Self::Error>> {
        Ok(Self { ratio })
    }

    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        if self.ratio.to_bits() == f64::to_bits(1.0) {
            fmt.write_str("1.0 (unchanged)")
        } else {
            fmt.write_fmt(format_args!("{:.1}", self.ratio))
        }
    }
}

impl Measurement for f64 {
    type Error = Infallible;

    fn to_f64(&self) -> f64 {
        *self
    }

    fn try_from_f64(v: f64) -> Result<Self, LocationError<Self::Error>> {
        Ok(v)
    }

    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        fmt.write_fmt(format_args!("{self}"))
    }
}

#[derive(Debug, Copy, Clone, PartialEq, Eq)]
pub enum AnyMeasurement {}

impl Measurement for AnyMeasurement {
    type Error = AnyError;

    fn to_f64(&self) -> f64 {
        #[expect(clippy::uninhabited_references)] // FIXME
        match *self {}
    }

    fn try_from_f64(_v: f64) -> Result<Self, LocationError<Self::Error>> {
        Err(AnyError::msg("cannot construct any measurement").into())
    }

    fn fmt(&self, _fmt: &mut fmt::Formatter) -> fmt::Result {
        #[expect(clippy::uninhabited_references)] // FIXME
        match *self {}
    }
}
