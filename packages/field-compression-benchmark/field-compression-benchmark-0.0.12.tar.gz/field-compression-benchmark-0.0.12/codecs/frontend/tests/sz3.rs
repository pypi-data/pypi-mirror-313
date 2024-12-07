#![allow(unused_crate_dependencies)]

#[cfg(all(single_wasm_runtime, feature = "wasmtime"))]
#[test]
fn sz3_encode_heisenbug() -> Result<(), pyo3::PyErr> {
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

        let sz3_class = codecs_frontend::WasmCodecClassLoader::load(
            py,
            Path::new("..")
                .join("..")
                .join("data")
                .join("codecs")
                .join("sz3.wasm"),
            &codecs,
        )?;

        let eb_abs = 5.623_413_251_903_49e-07;

        let sz3_config = PyDict::new(py);
        sz3_config.set_item("eb_mode", "abs")?;
        sz3_config.set_item("eb_abs", eb_abs)?;
        let sz3_codec = sz3_class.codec_from_config(sz3_config.as_borrowed())?;

        #[expect(clippy::unreadable_literal)]
        let data = [
            6.019042195593153,
            5.7760916245613645,
            -1.0284666644749214,
            1.5727866902901886,
            -1.2340438839630905,
            0.7767894445014174,
            2.659782439485495,
            5.560226236111176,
            1.2748576219137917,
            -4.267278962564942,
            1.8548097632045832,
            -0.5646192258182232,
            7.24354544546497,
            2.882656133481929,
            -4.636650035799854,
            4.073543134009759,
            0.7744188215262569,
            1.944717921085279,
            5.553662637138078,
            5.107073824860485,
            -2.487060794890152,
            -0.2782659775977417,
            -0.34144259497033824,
            9.912700198007123,
            0.9133706206035915,
            -0.5617508673076727,
            5.362177057516491,
            6.237931377062622,
            -1.6816032579015052,
            2.252819047644973,
            8.504477133051891,
            6.103788340146005,
            -4.1709318619734805,
            3.3273686280150656,
            4.897006004942515,
            3.2280440425178316,
        ];

        let encoded: Bound<PyArray1<u8>> = sz3_codec
            .encode(PyArray1::from_slice(py, &data).as_any().into())?
            .extract()?;
        let decoded: Bound<PyArray1<f64>> =
            sz3_codec.decode(encoded.as_any().into(), None)?.extract()?;

        let decoded = decoded.try_readonly()?;
        let decoded = decoded.as_slice()?;

        assert_eq!(decoded.len(), data.len());

        for (da, de) in data.iter().zip(decoded) {
            assert!((*da - *de).abs() <= eb_abs);
        }

        Ok(())
    })?;

    Ok(())
}
