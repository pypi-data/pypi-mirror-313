use std::num::NonZeroUsize;

use core_dataset::dataset::DatasetSettings;

const ONE: NonZeroUsize = NonZeroUsize::MIN;
const TEN: NonZeroUsize = ONE.saturating_add(9);
const HUNDRED: NonZeroUsize = TEN.saturating_mul(TEN);
const THOUSAND: NonZeroUsize = HUNDRED.saturating_mul(TEN);

#[derive(Debug, Clone, Default, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
#[serde(default)]
pub struct BenchmarkSettings {
    pub measurements: MeasurementSettings,
    pub datasets: DatasetSettings,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
#[serde(default)]
pub struct MeasurementSettings {
    pub num_repeats: NonZeroUsize,
    pub bootstrap: BootstrapSettings,
    pub metrics: MetricsSettings,
}

impl Default for MeasurementSettings {
    fn default() -> Self {
        Self {
            num_repeats: TEN,
            bootstrap: BootstrapSettings::default(),
            metrics: MetricsSettings::default(),
        }
    }
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
#[serde(default)]
pub struct BootstrapSettings {
    pub seed: u64,
    pub samples: Option<NonZeroUsize>,
}

impl Default for BootstrapSettings {
    fn default() -> Self {
        Self {
            seed: 42,
            samples: Some(THOUSAND),
        }
    }
}

#[derive(Clone, Debug, Default, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
#[serde(default)]
pub struct MetricsSettings {
    pub error: ErrorSettings,
    pub pca: PCASettings,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
#[serde(default)]
pub struct ErrorSettings {
    pub bins: NonZeroUsize,
    pub resamples: NonZeroUsize,
}

impl Default for ErrorSettings {
    fn default() -> Self {
        Self {
            bins: HUNDRED,
            resamples: HUNDRED,
        }
    }
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
#[serde(default)]
pub struct PCASettings {
    pub max_modes: NonZeroUsize,
}

impl Default for PCASettings {
    fn default() -> Self {
        Self { max_modes: TEN }
    }
}
