use std::borrow::Cow;

use nonempty::NonEmpty;
use serde::Deserialize;
use sorted_vec::SortedSet;

mod config;

pub(super) use config::DataDerivativeFormulaSetSeed;

#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum DataDerivative {
    Differentiate { differentiate: String },
    Integrate { integrate: String },
}

impl<'de> serde::Deserialize<'de> for DataDerivative {
    fn deserialize<D: serde::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        if deserializer.is_human_readable() {
            match DataDerivativeSummaryInnerHumanReadable::deserialize(deserializer)? {
                DataDerivativeSummaryInnerHumanReadable::Differentiate { differentiate } => {
                    Ok(Self::Differentiate {
                        differentiate: differentiate.into_owned(),
                    })
                },
                DataDerivativeSummaryInnerHumanReadable::Integrate { integrate } => {
                    Ok(Self::Integrate {
                        integrate: integrate.into_owned(),
                    })
                },
            }
        } else {
            match DataDerivativeSummaryInnerBinary::deserialize(deserializer)? {
                DataDerivativeSummaryInnerBinary::Differentiate { differentiate } => {
                    Ok(Self::Differentiate {
                        differentiate: differentiate.into_owned(),
                    })
                },
                DataDerivativeSummaryInnerBinary::Integrate { integrate } => Ok(Self::Integrate {
                    integrate: integrate.into_owned(),
                }),
            }
        }
    }
}

impl DataDerivative {
    #[must_use]
    pub fn summary(&self) -> DataDerivativeSummary {
        let inner = match self {
            Self::Differentiate { differentiate } => DataDerivativeSummaryInner::Differentiate {
                differentiate: Cow::Borrowed(differentiate.as_str()),
            },
            Self::Integrate { integrate } => DataDerivativeSummaryInner::Integrate {
                integrate: Cow::Borrowed(integrate.as_str()),
            },
        };

        DataDerivativeSummary { inner }
    }
}

#[derive(
    Clone, Debug, PartialEq, Eq, PartialOrd, Ord, Hash, serde::Serialize, serde::Deserialize,
)]
#[serde(rename = "DataDerivative")]
#[serde(transparent)]
pub struct DataDerivativeSummary<'a> {
    #[serde(borrow)]
    inner: DataDerivativeSummaryInner<'a>,
}

#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord, Hash)]
enum DataDerivativeSummaryInner<'a> {
    Differentiate { differentiate: Cow<'a, str> },
    Integrate { integrate: Cow<'a, str> },
}

// FIXME: eliminate extraneous clones
impl serde::Serialize for DataDerivativeSummaryInner<'_> {
    fn serialize<S: serde::Serializer>(&self, serializer: S) -> Result<S::Ok, S::Error> {
        if serializer.is_human_readable() {
            match self.clone() {
                Self::Differentiate { differentiate } => {
                    DataDerivativeSummaryInnerHumanReadable::Differentiate { differentiate }
                },
                Self::Integrate { integrate } => {
                    DataDerivativeSummaryInnerHumanReadable::Integrate { integrate }
                },
            }
            .serialize(serializer)
        } else {
            match self.clone() {
                Self::Differentiate { differentiate } => {
                    DataDerivativeSummaryInnerBinary::Differentiate { differentiate }
                },
                Self::Integrate { integrate } => {
                    DataDerivativeSummaryInnerBinary::Integrate { integrate }
                },
            }
            .serialize(serializer)
        }
    }
}

impl<'a, 'de: 'a> serde::Deserialize<'de> for DataDerivativeSummaryInner<'a> {
    fn deserialize<D: serde::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        if deserializer.is_human_readable() {
            match DataDerivativeSummaryInnerHumanReadable::deserialize(deserializer)? {
                DataDerivativeSummaryInnerHumanReadable::Differentiate { differentiate } => {
                    Ok(Self::Differentiate { differentiate })
                },
                DataDerivativeSummaryInnerHumanReadable::Integrate { integrate } => {
                    Ok(Self::Integrate { integrate })
                },
            }
        } else {
            match DataDerivativeSummaryInnerBinary::deserialize(deserializer)? {
                DataDerivativeSummaryInnerBinary::Differentiate { differentiate } => {
                    Ok(Self::Differentiate { differentiate })
                },
                DataDerivativeSummaryInnerBinary::Integrate { integrate } => {
                    Ok(Self::Integrate { integrate })
                },
            }
        }
    }
}

#[derive(serde::Serialize, serde::Deserialize)]
#[serde(rename = "DataDerivative")]
#[serde(untagged)]
enum DataDerivativeSummaryInnerHumanReadable<'a> {
    Differentiate {
        #[serde(borrow)]
        differentiate: Cow<'a, str>,
    },
    Integrate {
        #[serde(borrow)]
        integrate: Cow<'a, str>,
    },
}

#[derive(serde::Serialize, serde::Deserialize)]
#[serde(rename = "DataDerivative")]
enum DataDerivativeSummaryInnerBinary<'a> {
    Differentiate {
        #[serde(borrow)]
        differentiate: Cow<'a, str>,
    },
    Integrate {
        #[serde(borrow)]
        integrate: Cow<'a, str>,
    },
}

pub(super) fn serialize<S: serde::Serializer>(
    derivatives: &SortedSet<NonEmpty<DataDerivativeSummary>>,
    serializer: S,
) -> Result<S::Ok, S::Error> {
    serde::Serializer::collect_seq(serializer, derivatives.iter())
}

pub(super) fn deserialize<'de, D: serde::Deserializer<'de>>(
    deserializer: D,
) -> Result<SortedSet<NonEmpty<DataDerivativeSummary<'de>>>, D::Error> {
    let vec = Vec::deserialize(deserializer)?;
    Ok(SortedSet::from_unsorted(vec))
}
