use pyo3::prelude::*;

use core_compressor::{
    compress::{CodecPerformanceMeasurement, DataArrayCompressor},
    compressor::ConcreteCompressor,
};
use core_measure::{
    measurement::{Bytes, CompressionRatio, InstructionsPerByte, ThroughputPerSecond, WallTime},
    Measurable,
};

use crate::{error::BenchmarkSingleCaseError, measuring::Measurements};

pub fn compress_and_perform_performance_measurements<'py>(
    py: Python<'py>,
    compressor: &ConcreteCompressor,
    py_data_array: Borrowed<'_, 'py, PyAny>,
    measurements: &mut Measurements,
) -> Result<Bound<'py, PyAny>, BenchmarkSingleCaseError> {
    let py_compressor = compressor.build_py(py)?;

    let timing = WallTime::start()?;

    // Eagerly compute the compression ⇄ decompression
    let (py_data_array_compressed, measurement) =
        DataArrayCompressor::compute_compress_decompress(py, py_data_array, &py_compressor)?;

    let timing = WallTime::end(timing)?;

    let mut total_instructions = None;

    for (measurements, measurement) in measurements.per_codec.iter_mut().zip(measurement.iter()) {
        measurements.compression_ratios.push(CompressionRatio::new(
            measurement.decoded_bytes,
            measurement.encoded_bytes,
        ));
        measurements
            .encode_throughput
            .push(ThroughputPerSecond::new(
                measurement.encode_timing,
                measurement.decoded_bytes,
            ));
        measurements
            .decode_throughput
            .push(ThroughputPerSecond::new(
                measurement.decode_timing,
                measurement.decoded_bytes,
            ));
        if let Some(encode_instructions) = measurement.encode_instructions {
            measurements
                .encode_instructions
                .push(InstructionsPerByte::new(
                    encode_instructions,
                    measurement.decoded_bytes,
                ));
            *total_instructions.get_or_insert(0) += encode_instructions;
        }
        if let Some(decode_instructions) = measurement.decode_instructions {
            measurements
                .decode_instructions
                .push(InstructionsPerByte::new(
                    decode_instructions,
                    measurement.decoded_bytes,
                ));
            *total_instructions.get_or_insert(0) += decode_instructions;
        }
        measurements
            .encoded_bytes
            .push(Bytes::from(measurement.encoded_bytes));
        measurements
            .decoded_bytes
            .push(Bytes::from(measurement.decoded_bytes));
    }

    let (compression_ratio, throughput, instructions) =
        match (measurement.first(), measurement.last()) {
            (
                Some(CodecPerformanceMeasurement { decoded_bytes, .. }),
                Some(CodecPerformanceMeasurement { encoded_bytes, .. }),
            ) => (
                CompressionRatio::new(*decoded_bytes, *encoded_bytes),
                ThroughputPerSecond::new(timing, *decoded_bytes),
                total_instructions
                    .map(|instructions| InstructionsPerByte::new(instructions, *decoded_bytes)),
            ),
            _ => (
                CompressionRatio::unchanged(),
                ThroughputPerSecond::zero(),
                None,
            ),
        };
    measurements.compression_ratio.push(compression_ratio);
    measurements.throughput.push(throughput);
    if let Some(instructions) = instructions {
        measurements.instructions.push(instructions);
    }

    Ok(py_data_array_compressed)
}
