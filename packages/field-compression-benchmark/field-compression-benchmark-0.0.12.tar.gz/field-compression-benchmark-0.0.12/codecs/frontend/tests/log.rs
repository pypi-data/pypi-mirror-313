#![allow(unused_crate_dependencies)]

#[cfg(all(single_wasm_runtime, feature = "wasmtime"))]
#[test]
fn log() -> Result<(), pyo3::PyErr> {
    use std::path::Path;

    use core_error::pyerr_from_location_err;
    use numpy::{PyArray1, PyArrayMethods};
    use pyo3::{prelude::*, types::PyDict};

    use numcodecs_python::{PyCodecClassMethods, PyCodecMethods};

    // create a Python runtime
    pyo3::prepare_freethreaded_python();

    Python::with_gil(|py| -> Result<(), PyErr> {
        simple_logger::init_with_level(log::Level::Info)
            .map_err(|err| pyerr_from_location_err(py, err))?;

        let fcbench = PyModule::new(py, "fcbench")?;

        let codecs = codecs_frontend::init_codecs(py, fcbench.as_borrowed())
            .map_err(core_error::LocationError::into_error)?;

        let log_class = codecs_frontend::WasmCodecClassLoader::load(
            py,
            Path::new("..")
                .join("..")
                .join("data")
                .join("codecs")
                .join("log.wasm"),
            &codecs,
        )?;

        let log_codec = log_class.codec_from_config(PyDict::new(py).as_borrowed())?;

        let data = (1..1000).map(f64::from).collect::<Vec<_>>();

        let encoded: Bound<PyArray1<f64>> = log_codec
            .encode(PyArray1::from_slice(py, &data).as_any().into())?
            .extract()?;

        let decoded: Bound<PyArray1<f64>> =
            log_codec.decode(encoded.as_any().into(), None)?.extract()?;

        let encoded = encoded.try_readonly()?;
        let encoded = encoded.as_slice()?;

        assert_eq!(encoded.len(), data.len());

        for (da, en) in data.iter().zip(encoded) {
            // allow for some implementation difference between wasm and host
            assert!((*da).ln().to_bits().abs_diff((*en).to_bits()) <= 1);
        }

        let decoded = decoded.try_readonly()?;
        let decoded = decoded.as_slice()?;

        assert_eq!(decoded.len(), data.len());

        for (da, de) in data.iter().zip(decoded) {
            assert!((*da - *de).abs() <= 1e-12);
        }

        Ok(())
    })?;

    Ok(())
}
