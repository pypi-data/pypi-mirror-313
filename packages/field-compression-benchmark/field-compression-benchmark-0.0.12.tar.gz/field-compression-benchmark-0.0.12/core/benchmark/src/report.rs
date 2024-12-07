use std::{borrow::Cow, path::Path};

use core_compressor::compressor::ConcreteCompressorSummary;
use core_dataset::{dataset::DatasetFormat, variable::DataVariableSummary};

use vecmap::VecMap;

use crate::{
    case::BenchmarkCaseId, error::BenchmarkCaseError, measuring::CompressorBenchmarkStats,
    settings::BenchmarkSettings,
};

#[derive(Debug, Default, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
#[serde(default)]
pub struct BenchmarkReport<'a> {
    pub settings: BenchmarkSettings,
    #[serde(borrow)]
    pub results: VecMap<BenchmarkCaseId, BenchmarkCaseReport<'a>>,
    pub summary: BenchmarkSummary,
}

#[derive(Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct BenchmarkCaseReport<'a> {
    #[serde(borrow)]
    pub dataset: Cow<'a, Path>,
    pub format: DatasetFormat,
    #[serde(borrow)]
    pub variable: DataVariableSummary<'a>,
    #[serde(borrow)]
    pub compressor: ConcreteCompressorSummary<'a>,
    pub result: Result<BenchmarkCaseOutput, BenchmarkCaseError>,
}

#[derive(Debug, Default, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
#[serde(default)]
pub struct BenchmarkSummary {
    pub success: usize,
    pub failures: usize,
    pub cancelled: usize,
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct BenchmarkCaseOutput {
    pub stats: CompressorBenchmarkStats,
}
