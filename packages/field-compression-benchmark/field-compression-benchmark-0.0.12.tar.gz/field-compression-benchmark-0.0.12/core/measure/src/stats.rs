use std::{fmt, num::NonZeroUsize};

use rand::{distributions::Slice, Rng};
use thiserror::Error;

use core_error::{AnyError, LocationError};

use crate::{measurement::AnyMeasurement, Measurement};

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct BenchmarkStats<T: Measurement> {
    pub mean: ConfidenceInterval<T>,
    pub median: ConfidenceInterval<T>,
}

impl<T: Measurement> BenchmarkStats<T> {
    pub fn try_from_bootstrap_analysis(
        samples: &[T],
        rng: &mut impl Rng,
        bootstrap_samples: Option<NonZeroUsize>,
    ) -> Result<Self, LocationError<AnalysisError<AnyMeasurement>>> {
        Self::try_from_bootstrap_analysis_explicit_error(samples, rng, bootstrap_samples)
            .map_err(|err| err.map(AnalysisError::erase))
    }

    pub fn try_from_bootstrap_analysis_explicit_error(
        samples: &[T],
        rng: &mut impl Rng,
        bootstrap_samples: Option<NonZeroUsize>,
    ) -> Result<Self, LocationError<AnalysisError<T>>> {
        if let [first, rest @ ..] = samples {
            if rest.iter().all(|x| x == first) {
                return Ok(Self {
                    mean: ConfidenceInterval::from_const(*first),
                    median: ConfidenceInterval::from_const(*first),
                });
            }
        }

        let samples = samples.iter().map(Measurement::to_f64).collect::<Vec<_>>();
        let samples_dist = Slice::new(&samples).map_err(|_| AnalysisError::EmptySamples)?;

        let mut resampled = samples.clone();

        let Some(bootstrap_samples) = bootstrap_samples else {
            resampled.sort_by(f64::total_cmp);

            #[expect(clippy::cast_precision_loss)]
            let mean = resampled.iter().sum::<f64>() / (samples.len() as f64);
            let median = interpolate_to_percentage(&resampled, 0.5)?;

            let mean = T::try_from_f64(mean).map_err(AnalysisError::Conversion)?;
            let median = T::try_from_f64(median).map_err(AnalysisError::Conversion)?;

            return Ok(Self {
                mean: ConfidenceInterval::from_const(mean),
                median: ConfidenceInterval::from_const(median),
            });
        };

        let mut means = Vec::with_capacity(bootstrap_samples.get());
        let mut medians = Vec::with_capacity(bootstrap_samples.get());

        for _ in 0..bootstrap_samples.get() {
            for (s, r) in resampled.iter_mut().zip(rng.sample_iter(samples_dist)) {
                *s = *r;
            }

            resampled.sort_by(f64::total_cmp);

            #[expect(clippy::cast_precision_loss)]
            let mean = resampled.iter().sum::<f64>() / (samples.len() as f64);
            let median = interpolate_to_percentage(&resampled, 0.5)?;

            means.push(mean);
            medians.push(median);
        }

        means.sort_by(f64::total_cmp);
        medians.sort_by(f64::total_cmp);

        Ok(Self {
            mean: ConfidenceInterval {
                p2_5: interpolate_measurement_to_percentage(&means, 0.025)?,
                p15_9: interpolate_measurement_to_percentage(&means, 0.159)?,
                p50: interpolate_measurement_to_percentage(&means, 0.5)?,
                p84_1: interpolate_measurement_to_percentage(&means, 0.841)?,
                p97_5: interpolate_measurement_to_percentage(&means, 0.975)?,
            },
            median: ConfidenceInterval {
                p2_5: interpolate_measurement_to_percentage(&medians, 0.025)?,
                p15_9: interpolate_measurement_to_percentage(&medians, 0.159)?,
                p50: interpolate_measurement_to_percentage(&medians, 0.5)?,
                p84_1: interpolate_measurement_to_percentage(&medians, 0.841)?,
                p97_5: interpolate_measurement_to_percentage(&medians, 0.975)?,
            },
        })
    }
}

impl<T: Measurement> fmt::Display for BenchmarkStats<T> {
    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        if let (Some(const_mean), Some(const_median)) =
            (self.mean.as_const(), self.median.as_const())
        {
            if const_mean == const_median {
                Measurement::fmt(const_mean, fmt)?;
                return fmt.write_str(" (const)");
            }
        }

        let width = fmt.width().unwrap_or(0) + 1;

        fmt.write_fmt(format_args!("\n{:>width$} mean: {}", '-', self.mean))?;
        fmt.write_fmt(format_args!("\n{:>width$} median: {}", '-', self.median))?;

        Ok(())
    }
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ConfidenceInterval<T: Measurement> {
    pub p2_5: T,
    pub p15_9: T,
    pub p50: T,
    pub p84_1: T,
    pub p97_5: T,
}

impl<T: Measurement> ConfidenceInterval<T> {
    #[must_use]
    pub const fn from_const(v: T) -> Self {
        Self {
            p2_5: v,
            p15_9: v,
            p50: v,
            p84_1: v,
            p97_5: v,
        }
    }

    pub fn as_const(&self) -> Option<&T> {
        if self.p2_5 == self.p50
            && self.p15_9 == self.p50
            && self.p84_1 == self.p50
            && self.p97_5 == self.p50
        {
            Some(&self.p50)
        } else {
            None
        }
    }
}

impl ConfidenceInterval<f64> {
    pub fn try_convert<T: Measurement>(
        self,
    ) -> Result<ConfidenceInterval<T>, LocationError<T::Error>> {
        Ok(ConfidenceInterval {
            p2_5: T::try_from_f64(self.p2_5)?,
            p15_9: T::try_from_f64(self.p15_9)?,
            p50: T::try_from_f64(self.p50)?,
            p84_1: T::try_from_f64(self.p84_1)?,
            p97_5: T::try_from_f64(self.p97_5)?,
        })
    }
}

impl<T: Measurement> fmt::Display for ConfidenceInterval<T> {
    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        if let Some(r#const) = self.as_const() {
            Measurement::fmt(r#const, fmt)?;
            return fmt.write_str(" (const)");
        }

        Measurement::fmt(&self.p2_5, fmt)?;
        fmt.write_str(" [")?;
        Measurement::fmt(&self.p15_9, fmt)?;
        fmt.write_str(" - ")?;
        Measurement::fmt(&self.p50, fmt)?;
        fmt.write_str(" - ")?;
        Measurement::fmt(&self.p84_1, fmt)?;
        fmt.write_str("] ")?;
        Measurement::fmt(&self.p97_5, fmt)?;

        Ok(())
    }
}

#[derive(Debug, Error)]
pub enum AnalysisError<T: Measurement = AnyMeasurement> {
    #[error("samples is empty")]
    EmptySamples,
    #[error("failed to convert f64 to measurement")]
    Conversion(#[source] LocationError<T::Error>),
}

impl<T: Measurement> AnalysisError<T> {
    #[must_use]
    pub fn erase(self) -> AnalysisError<AnyMeasurement> {
        match self {
            Self::EmptySamples => AnalysisError::EmptySamples,
            Self::Conversion(err) => AnalysisError::Conversion(err.map(AnyError::new)),
        }
    }
}

#[expect(
    clippy::cast_precision_loss,
    clippy::cast_possible_truncation,
    clippy::cast_sign_loss
)]
fn interpolate_to_percentage<T: Measurement>(
    samples: &[f64],
    percentage: f64,
) -> Result<f64, LocationError<AnalysisError<T>>> {
    let index_floor = ((((samples.len() - 1) as f64) * percentage).floor().max(0.0) as usize)
        .min(samples.len() - 1);
    let index_ceil = ((((samples.len() - 1) as f64) * percentage).ceil().max(0.0) as usize)
        .min(samples.len() - 1);

    let percentage_floor = (index_floor as f64) / ((samples.len() - 1) as f64);
    let percentage_ceil = (index_ceil as f64) / ((samples.len() - 1) as f64);

    if (percentage_ceil - percentage_floor).abs() < f64::EPSILON {
        return samples
            .get(index_floor)
            .copied()
            .ok_or_else(|| AnalysisError::EmptySamples.into());
    }

    let (Some(value_floor), Some(value_ceil)) = (samples.get(index_floor), samples.get(index_ceil))
    else {
        return Err(AnalysisError::EmptySamples.into());
    };

    let value = *value_floor
        + (*value_ceil - *value_floor) * (percentage - percentage_floor)
            / (percentage_ceil - percentage_floor);
    Ok(value)
}

fn interpolate_measurement_to_percentage<T: Measurement>(
    samples: &[f64],
    percentage: f64,
) -> Result<T, LocationError<AnalysisError<T>>> {
    interpolate_to_percentage(samples, percentage).and_then(|value| {
        T::try_from_f64(value)
            .map_err(AnalysisError::Conversion)
            .map_err(LocationError::new)
    })
}
