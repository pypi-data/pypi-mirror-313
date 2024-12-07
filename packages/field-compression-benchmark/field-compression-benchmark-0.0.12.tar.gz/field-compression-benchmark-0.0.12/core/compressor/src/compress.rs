#![allow(clippy::redundant_pub_crate)]

use std::time::Duration;

use codecs_frontend::WasmCodec;
use numpy::{PyUntypedArray, PyUntypedArrayMethods};
use pyo3::{
    intern,
    prelude::*,
    sync::GILOnceCell,
    types::{IntoPyDict, PyBool, PyTuple},
};

use core_error::LocationError;
use core_measure::{measurement::WallTime, Measurable};
use numcodecs_python::{PyCodec, PyCodecAdapter, PyCodecMethods};

pub enum DataArrayCompressor {}

impl DataArrayCompressor {
    pub fn compute_compress_decompress<'py>(
        py: Python<'py>,
        da: Borrowed<'_, 'py, PyAny>,
        compressor: &[Bound<'py, PyCodec>],
    ) -> Result<(Bound<'py, PyAny>, Vec<CodecPerformanceMeasurement>), LocationError<PyErr>> {
        static XARRAY_MAP_BLOCKS: GILOnceCell<Py<PyAny>> = GILOnceCell::new();
        static DASK_CONFIG_SET: GILOnceCell<Py<PyAny>> = GILOnceCell::new();

        let tracker = Bound::<CompressorPerformanceTracker>::new(
            py,
            CompressorPerformanceTracker {
                per_codec: vec![
                    CodecPerformanceMeasurement {
                        encode_timing: Duration::ZERO,
                        decode_timing: Duration::ZERO,
                        encode_instructions: None,
                        decode_instructions: None,
                        encoded_bytes: 0,
                        decoded_bytes: 0,
                    };
                    compressor.len()
                ],
            },
        )?;

        let kwargs = [
            (
                intern!(py, "codecs"),
                PyTuple::new(py, compressor)?.as_any(),
            ),
            (intern!(py, "tracker"), tracker.as_any()),
        ]
        .into_py_dict(py)?;

        // The compression-decompression must run single-threaded since the tracker
        //  requires mutable borrows
        let context = DASK_CONFIG_SET.import(py, "dask.config", "set")?.call(
            PyTuple::empty(py),
            Some(&[(intern!(py, "scheduler"), intern!(py, "synchronous"))].into_py_dict(py)?),
        )?;

        context.call_method0(intern!(py, "__enter__"))?;
        let decompressed = (|| -> Result<Bound<PyAny>, LocationError<PyErr>> {
            XARRAY_MAP_BLOCKS
                .import(py, "xarray", "map_blocks")?
                .call1((
                    wrap_pyfunction!(compress_decompress_data_array_single_chunk, py)?,
                    da,
                    PyTuple::empty(py),
                    kwargs,
                ))?
                .call_method0(intern!(py, "compute"))
                .map_err(LocationError::new)
        })();
        context.call_method1(
            intern!(py, "__exit__"),
            (Option::<()>::None, Option::<()>::None, Option::<()>::None),
        )?;

        let decompressed = decompressed?;

        let mut tracker: PyRefMut<CompressorPerformanceTracker> = tracker
            .try_borrow_mut()
            .map_err(PyErr::from)
            .map_err(LocationError::new)?;
        let CompressorPerformanceTracker {
            per_codec: measurement,
        } = &mut *tracker;

        Ok((decompressed, std::mem::take(measurement)))
    }
}

pub enum NumpyArrayCompressor {}

impl NumpyArrayCompressor {
    pub fn compress_decompress<'py>(
        py: Python<'py>,
        array: Bound<'py, PyUntypedArray>,
        compressor: Vec<Bound<'py, PyCodec>>,
    ) -> Result<(Bound<'py, PyUntypedArray>, Vec<CodecPerformanceMeasurement>), LocationError<PyErr>>
    {
        // ensure that the uncompressed data is in a unique and contiguous array
        let array: Bound<PyUntypedArray> = {
            let contiguous: Bound<PyUntypedArray> = numpy_ascontiguousarray(py, &array)?;
            if contiguous.is(&array) {
                numpy_copy(py, &contiguous)?
            } else {
                array
            }
        };

        let mut tracker = CompressorPerformanceTracker {
            per_codec: vec![
                CodecPerformanceMeasurement {
                    encode_timing: Duration::ZERO,
                    decode_timing: Duration::ZERO,
                    encode_instructions: None,
                    decode_instructions: None,
                    encoded_bytes: 0,
                    decoded_bytes: 0,
                };
                compressor.len()
            ],
        };

        let decompressed =
            compress_decompress_contiguous_numpy_array(py, array, compressor, &mut tracker)?;

        Ok((decompressed, tracker.per_codec))
    }
}

#[derive(Clone, serde::Serialize, serde::Deserialize)]
pub struct CodecPerformanceMeasurement {
    pub encode_timing: Duration,
    pub decode_timing: Duration,
    pub encode_instructions: Option<u64>,
    pub decode_instructions: Option<u64>,
    pub encoded_bytes: usize,
    pub decoded_bytes: usize,
}

#[pyclass]
// not frozen as the tracker is mutated to update the stats
struct CompressorPerformanceTracker {
    per_codec: Vec<CodecPerformanceMeasurement>,
}

#[pyfunction]
fn compress_decompress_data_array_single_chunk<'py>(
    py: Python<'py>,
    da: &Bound<'py, PyAny>,
    codecs: Vec<Bound<'py, PyCodec>>,
    tracker: &mut CompressorPerformanceTracker,
) -> Result<Bound<'py, PyAny>, PyErr> {
    let dims: Bound<PyTuple> = da.getattr(intern!(py, "dims"))?.extract()?;
    let new_chunks = dims.iter().map(|dim| (dim, -1)).into_py_dict(py)?;

    if da.getattr(intern!(py, "size"))?.extract::<usize>()? == 0 {
        // compressing and decompressing preserves the input shape
        return da
            .call_method(
                intern!(py, "copy"),
                PyTuple::empty(py),
                Some(&[(intern!(py, "deep"), false)].into_py_dict(py)?),
            )?
            .call_method1(intern!(py, "chunk"), (new_chunks,));
    }

    // eagerly compute the uncompressed input chunk
    let values = da.getattr(intern!(py, "values"))?;
    // ensure that the uncompressed data is in a unique and contiguous array
    let array: Bound<PyUntypedArray> = numpy_ascontiguousarray(py, &values)?;
    let array: Bound<PyUntypedArray> = if array.is(&values) {
        numpy_copy(py, &array)?
    } else {
        array
    };

    let decoded = compress_decompress_contiguous_numpy_array(py, array, codecs, tracker)?;

    da.call_method(
        intern!(py, "copy"),
        PyTuple::empty(py),
        Some(
            &[
                (intern!(py, "deep"), PyBool::new(py, false).as_any()),
                (intern!(py, "data"), decoded.as_any()),
            ]
            .into_py_dict(py)?,
        ),
    )?
    .call_method1(intern!(py, "chunk"), (new_chunks,))
}

fn compress_decompress_contiguous_numpy_array<'py>(
    py: Python<'py>,
    array: Bound<'py, PyUntypedArray>,
    codecs: Vec<Bound<'py, PyCodec>>,
    tracker: &mut CompressorPerformanceTracker,
) -> Result<Bound<'py, PyUntypedArray>, PyErr> {
    static NUMCODECS_ENSURE_NDARRAY_LIKE: GILOnceCell<Py<PyAny>> = GILOnceCell::new();
    static NUMPY_EMPTY: GILOnceCell<Py<PyAny>> = GILOnceCell::new();

    // pre-obtain methods that are needed in the hot encode and decode loops
    let ensure_ndarray_like =
        NUMCODECS_ENSURE_NDARRAY_LIKE.import(py, "numcodecs.compat", "ensure_ndarray_like")?;
    let nbytes = intern!(py, "nbytes");
    let empty = NUMPY_EMPTY.import(py, "numpy", "empty")?;
    let reshape = intern!(py, "reshape");

    let mut silhouettes = Vec::with_capacity(codecs.len());

    // encode the chunk as: codecs[-1].encode( ... codecs[0].encode(array) ... )
    let encoded = codecs.iter().zip(tracker.per_codec.iter_mut()).try_fold(
        array,
        |encoded, (codec, measurement)| -> Result<Bound<PyUntypedArray>, PyErr> {
            silhouettes.push((PyTuple::new(py, encoded.shape())?, encoded.dtype()));

            let pre_instructions = PyCodecAdapter::with_downcast(codec, |codec: &WasmCodec| {
                codec.instruction_counter().ok()
            })
            .flatten();
            let encode_start = match WallTime::start() {
                Ok(encode_start) => encode_start,
                Err(err) => err.infallible(),
            };
            let encoded: Bound<PyUntypedArray> = ensure_ndarray_like
                .call1((codec.encode(encoded.as_any().as_borrowed())?,))?
                .extract()?;
            if !encoded.is_contiguous() {
                return Err(PyErr::from(numpy::NotContiguousError));
            }
            let encode_timing = match WallTime::end(encode_start) {
                Ok(encode_timing) => encode_timing,
                Err(err) => err.infallible(),
            };
            let post_instructions = PyCodecAdapter::with_downcast(codec, |codec: &WasmCodec| {
                codec.instruction_counter().ok()
            })
            .flatten();

            measurement.encode_timing += encode_timing;
            if let (Some(pre), Some(post)) = (pre_instructions, post_instructions) {
                *measurement.encode_instructions.get_or_insert(0) += post - pre;
            }
            measurement.encoded_bytes += encoded.getattr(nbytes)?.extract::<usize>()?;

            Ok(encoded)
        },
    )?;

    // decode the chunk as: codecs[0].decode( ... codecs[-1].decode(encoded) ... )
    let decoded = codecs
        .into_iter()
        .zip(tracker.per_codec.iter_mut())
        .zip(silhouettes.into_iter())
        .try_rfold(
            encoded,
            |decoded,
             ((codec, measurement), (shape, dtype))|
             -> Result<Bound<PyUntypedArray>, PyErr> {
                let out: Bound<PyUntypedArray> =
                    empty.call1((shape.as_borrowed(), dtype))?.extract()?;

                let pre_instructions =
                    PyCodecAdapter::with_downcast(&codec, |codec: &WasmCodec| {
                        codec.instruction_counter().ok()
                    })
                    .flatten();
                let decode_start = match WallTime::start() {
                    Ok(decode_start) => decode_start,
                    Err(err) => err.infallible(),
                };
                let decoded: Bound<PyUntypedArray> = codec
                    .decode(
                        decoded.as_any().as_borrowed(),
                        Some(out.as_any().as_borrowed()),
                    )?
                    .call_method1(reshape, (shape,))?
                    .extract()?;
                let decode_timing = match WallTime::end(decode_start) {
                    Ok(decode_timing) => decode_timing,
                    Err(err) => err.infallible(),
                };
                let post_instructions =
                    PyCodecAdapter::with_downcast(&codec, |codec: &WasmCodec| {
                        codec.instruction_counter().ok()
                    })
                    .flatten();

                measurement.decode_timing += decode_timing;
                if let (Some(pre), Some(post)) = (pre_instructions, post_instructions) {
                    *measurement.decode_instructions.get_or_insert(0) += post - pre;
                }
                measurement.decoded_bytes += decoded.getattr(nbytes)?.extract::<usize>()?;

                Ok(decoded)
            },
        )?;

    Ok(decoded)
}

fn numpy_ascontiguousarray<'py>(
    py: Python<'py>,
    a: &Bound<'py, PyAny>,
) -> Result<Bound<'py, PyUntypedArray>, PyErr> {
    static NUMPY_ASCONTIGUOUSARRAY: GILOnceCell<Py<PyAny>> = GILOnceCell::new();

    NUMPY_ASCONTIGUOUSARRAY
        .import(py, "numpy", "ascontiguousarray")?
        .call1((a,))?
        .extract()
}

fn numpy_copy<'py>(
    py: Python<'py>,
    a: &Bound<'py, PyAny>,
) -> Result<Bound<'py, PyUntypedArray>, PyErr> {
    static NUMPY_COPY: GILOnceCell<Py<PyAny>> = GILOnceCell::new();

    NUMPY_COPY
        .import(py, "numpy", "copy")?
        .call1((a,))?
        .extract()
}
