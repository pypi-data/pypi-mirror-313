use std::num::NonZeroUsize;

use nonempty::NonEmpty;
use rand::Rng;

use core_error::LocationError;
use core_goodness::{
    bit_information::BitInformationGoodness, correlation::CompressionCorrelationGoodness,
    error::CompressionError, pca::PreservedPCAGoodness, ps2nr::PeakSignalToNoiseRatio,
    uniformity::CompressionUniformityGoodness,
};
use core_measure::{
    measurement::{Bytes, CompressionRatio, InstructionsPerByte, ThroughputPerSecond},
    stats::{AnalysisError, BenchmarkStats},
};

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct CompressorBenchmarkStats {
    pub goodness: NonEmpty<GoodnessBenchmarkStats>,
    pub throughput: BenchmarkStats<ThroughputPerSecond>,
    pub instructions: Option<BenchmarkStats<InstructionsPerByte>>,
    pub compression_ratio: BenchmarkStats<CompressionRatio>,
    pub per_codec: Vec<CodecBenchmarkStats>,
}

pub(crate) struct Measurements {
    pub goodness: NonEmpty<GoodnessMeasurements>,
    pub compression_ratio: Vec<CompressionRatio>,
    pub throughput: Vec<ThroughputPerSecond>,
    pub instructions: Vec<InstructionsPerByte>,
    pub per_codec: Vec<CodecMeasurements>,
}

impl Measurements {
    #[must_use]
    pub fn new(
        num_measurements: usize,
        histogram_resample: usize,
        num_derivatives: usize,
        num_codecs: usize,
    ) -> Self {
        Self {
            goodness: NonEmpty {
                head: GoodnessMeasurements {
                    uniformity: Vec::with_capacity(1),
                    uniformity_rel: Vec::with_capacity(1),
                    correlation: Vec::with_capacity(1),
                    preserved_pca: Vec::with_capacity(1),
                    bit_information: Vec::with_capacity(1),
                    error: Vec::with_capacity(histogram_resample),
                    error_abs: Vec::with_capacity(histogram_resample),
                    error_rel: Vec::with_capacity(histogram_resample),
                    error_rel_abs: Vec::with_capacity(histogram_resample),
                    error_rmse: Vec::with_capacity(1),
                    ps2nr: Vec::with_capacity(1),
                },
                tail: vec![
                    GoodnessMeasurements {
                        uniformity: Vec::with_capacity(1),
                        uniformity_rel: Vec::with_capacity(1),
                        correlation: Vec::with_capacity(1),
                        preserved_pca: Vec::with_capacity(1),
                        bit_information: Vec::with_capacity(1),
                        error: Vec::with_capacity(histogram_resample),
                        error_abs: Vec::with_capacity(histogram_resample),
                        error_rel: Vec::with_capacity(histogram_resample),
                        error_rel_abs: Vec::with_capacity(histogram_resample),
                        error_rmse: Vec::with_capacity(1),
                        ps2nr: Vec::with_capacity(1),
                    };
                    num_derivatives
                ],
            },
            compression_ratio: Vec::with_capacity(num_measurements),
            throughput: Vec::with_capacity(num_measurements),
            instructions: Vec::with_capacity(num_measurements),
            per_codec: vec![
                CodecMeasurements {
                    compression_ratios: Vec::with_capacity(num_measurements),
                    encode_throughput: Vec::with_capacity(num_measurements),
                    decode_throughput: Vec::with_capacity(num_measurements),
                    encode_instructions: Vec::with_capacity(num_measurements),
                    decode_instructions: Vec::with_capacity(num_measurements),
                    encoded_bytes: Vec::with_capacity(num_measurements),
                    decoded_bytes: Vec::with_capacity(num_measurements),
                };
                num_codecs
            ],
        }
    }

    pub fn analyse(
        &self,
        rng: &mut impl Rng,
        bootstrap_samples: Option<NonZeroUsize>,
    ) -> Result<CompressorBenchmarkStats, LocationError<AnalysisError>> {
        Ok(CompressorBenchmarkStats {
            goodness: NonEmpty {
                head: self.goodness.head.analyse(rng, bootstrap_samples)?,
                tail: self
                    .goodness
                    .tail
                    .iter()
                    .map(|measurement| measurement.analyse(rng, bootstrap_samples))
                    .collect::<Result<_, _>>()?,
            },
            throughput: BenchmarkStats::try_from_bootstrap_analysis(
                &self.throughput,
                rng,
                bootstrap_samples,
            )?,
            instructions: if self.instructions.is_empty() {
                None
            } else {
                Some(BenchmarkStats::try_from_bootstrap_analysis(
                    &self.instructions,
                    rng,
                    bootstrap_samples,
                )?)
            },
            compression_ratio: BenchmarkStats::try_from_bootstrap_analysis(
                &self.compression_ratio,
                rng,
                bootstrap_samples,
            )?,
            per_codec: self
                .per_codec
                .iter()
                .map(|measurement| measurement.analyse(rng, bootstrap_samples))
                .collect::<Result<_, _>>()?,
        })
    }
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct GoodnessBenchmarkStats {
    pub uniformity: BenchmarkStats<CompressionUniformityGoodness>,
    pub uniformity_rel: BenchmarkStats<CompressionUniformityGoodness>,
    pub correlation: BenchmarkStats<CompressionCorrelationGoodness>,
    pub preserved_pca: BenchmarkStats<PreservedPCAGoodness>,
    pub bit_information: BenchmarkStats<BitInformationGoodness>,
    pub error: BenchmarkStats<CompressionError>,
    pub error_abs: BenchmarkStats<CompressionError>,
    pub error_rel: BenchmarkStats<CompressionError>,
    pub error_rel_abs: BenchmarkStats<CompressionError>,
    pub error_rmse: BenchmarkStats<CompressionError>,
    pub ps2nr: BenchmarkStats<PeakSignalToNoiseRatio>,
}

#[derive(Clone)]
pub(crate) struct GoodnessMeasurements {
    pub uniformity: Vec<CompressionUniformityGoodness>,
    pub uniformity_rel: Vec<CompressionUniformityGoodness>,
    pub correlation: Vec<CompressionCorrelationGoodness>,
    pub preserved_pca: Vec<PreservedPCAGoodness>,
    pub bit_information: Vec<BitInformationGoodness>,
    pub error: Vec<CompressionError>,
    pub error_abs: Vec<CompressionError>,
    pub error_rel: Vec<CompressionError>,
    pub error_rel_abs: Vec<CompressionError>,
    pub error_rmse: Vec<CompressionError>,
    pub ps2nr: Vec<PeakSignalToNoiseRatio>,
}

impl GoodnessMeasurements {
    pub fn analyse(
        &self,
        rng: &mut impl Rng,
        bootstrap_samples: Option<NonZeroUsize>,
    ) -> Result<GoodnessBenchmarkStats, LocationError<AnalysisError>> {
        Ok(GoodnessBenchmarkStats {
            uniformity: BenchmarkStats::try_from_bootstrap_analysis(
                &self.uniformity,
                rng,
                bootstrap_samples,
            )?,
            uniformity_rel: BenchmarkStats::try_from_bootstrap_analysis(
                &self.uniformity_rel,
                rng,
                bootstrap_samples,
            )?,
            correlation: BenchmarkStats::try_from_bootstrap_analysis(
                &self.correlation,
                rng,
                bootstrap_samples,
            )?,
            preserved_pca: BenchmarkStats::try_from_bootstrap_analysis(
                &self.preserved_pca,
                rng,
                bootstrap_samples,
            )?,
            bit_information: BenchmarkStats::try_from_bootstrap_analysis(
                &self.bit_information,
                rng,
                bootstrap_samples,
            )?,
            error: BenchmarkStats::try_from_bootstrap_analysis(
                &self.error,
                rng,
                bootstrap_samples,
            )?,
            error_abs: BenchmarkStats::try_from_bootstrap_analysis(
                &self.error_abs,
                rng,
                bootstrap_samples,
            )?,
            error_rel: BenchmarkStats::try_from_bootstrap_analysis(
                &self.error_rel,
                rng,
                bootstrap_samples,
            )?,
            error_rel_abs: BenchmarkStats::try_from_bootstrap_analysis(
                &self.error_rel_abs,
                rng,
                bootstrap_samples,
            )?,
            error_rmse: BenchmarkStats::try_from_bootstrap_analysis(
                &self.error_rmse,
                rng,
                bootstrap_samples,
            )?,
            ps2nr: BenchmarkStats::try_from_bootstrap_analysis(
                &self.ps2nr,
                rng,
                bootstrap_samples,
            )?,
        })
    }
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct CodecBenchmarkStats {
    pub compression_ratio: BenchmarkStats<CompressionRatio>,
    pub encode_throughput: BenchmarkStats<ThroughputPerSecond>,
    pub decode_throughput: BenchmarkStats<ThroughputPerSecond>,
    pub encode_instructions: Option<BenchmarkStats<InstructionsPerByte>>,
    pub decode_instructions: Option<BenchmarkStats<InstructionsPerByte>>,
    pub encoded_bytes: BenchmarkStats<Bytes>,
    pub decoded_bytes: BenchmarkStats<Bytes>,
}

#[derive(Clone)]
pub(crate) struct CodecMeasurements {
    pub compression_ratios: Vec<CompressionRatio>,
    pub encode_throughput: Vec<ThroughputPerSecond>,
    pub decode_throughput: Vec<ThroughputPerSecond>,
    pub encode_instructions: Vec<InstructionsPerByte>,
    pub decode_instructions: Vec<InstructionsPerByte>,
    pub encoded_bytes: Vec<Bytes>,
    pub decoded_bytes: Vec<Bytes>,
}

impl CodecMeasurements {
    pub(crate) fn analyse(
        &self,
        rng: &mut impl Rng,
        bootstrap_samples: Option<NonZeroUsize>,
    ) -> Result<CodecBenchmarkStats, LocationError<AnalysisError>> {
        Ok(CodecBenchmarkStats {
            compression_ratio: BenchmarkStats::try_from_bootstrap_analysis(
                &self.compression_ratios,
                rng,
                bootstrap_samples,
            )?,
            encode_throughput: BenchmarkStats::try_from_bootstrap_analysis(
                &self.encode_throughput,
                rng,
                bootstrap_samples,
            )?,
            decode_throughput: BenchmarkStats::try_from_bootstrap_analysis(
                &self.decode_throughput,
                rng,
                bootstrap_samples,
            )?,
            encode_instructions: if self.encode_instructions.is_empty() {
                None
            } else {
                Some(BenchmarkStats::try_from_bootstrap_analysis(
                    &self.encode_instructions,
                    rng,
                    bootstrap_samples,
                )?)
            },
            decode_instructions: if self.decode_instructions.is_empty() {
                None
            } else {
                Some(BenchmarkStats::try_from_bootstrap_analysis(
                    &self.decode_instructions,
                    rng,
                    bootstrap_samples,
                )?)
            },
            encoded_bytes: BenchmarkStats::try_from_bootstrap_analysis(
                &self.encoded_bytes,
                rng,
                bootstrap_samples,
            )?,
            decoded_bytes: BenchmarkStats::try_from_bootstrap_analysis(
                &self.decoded_bytes,
                rng,
                bootstrap_samples,
            )?,
        })
    }
}
