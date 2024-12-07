use std::path::PathBuf;

use pyo3::{intern, prelude::*, types::PyDict};

use core_error::LocationError;

pub fn import_fcbench_codecs(
    py: Python,
    codec_paths: impl IntoIterator<Item = PathBuf>,
) -> Result<(), LocationError<PyErr>> {
    let sys_modules: Bound<PyDict> = py.import("sys")?.getattr("modules")?.extract()?;

    let fcbench = PyModule::new(py, "fcbench")?;

    let codecs = codecs_frontend::init_codecs(py, fcbench.as_borrowed())?;

    println!("- Loading the WASM codecs");

    for path in codec_paths {
        let codec_class = codecs_frontend::WasmCodecClassLoader::load(py, path.clone(), &codecs)?;
        println!(
            "  - Loaded the {} codec from {path:?}",
            codec_class
                .getattr(intern!(py, "__name__"))?
                .extract::<String>()?
        );
    }

    fcbench.add_submodule(&codecs)?;

    // According to
    // https://pyo3.rs/v0.21.0/python-from-rust/calling-existing-code#want-to-embed-python-in-rust-with-additional-modules
    // manually inserting a module into `sys.modules` is the correct way if the
    // module cannot be inserted with [`pyo3::append_to_inittab`] since it is
    // created after Python is initialised
    sys_modules.set_item(format!("{}.{}", fcbench.name()?, codecs.name()?), &codecs)?;
    sys_modules.set_item(fcbench.name()?, &fcbench)?;

    // add alias from fcpy.codecs to fcbench.codecs
    sys_modules.set_item(format!("fcpy.{}", codecs.name()?), codecs)?;
    sys_modules.set_item("fcpy", fcbench)?;

    Ok(())
}
