#![allow(clippy::missing_errors_doc)] // FIXME
#![cfg_attr(any(test, not(single_wasm_runtime)), allow(unused_crate_dependencies))]

#[macro_use]
extern crate log;

mod codec;
mod engine;
mod loader;
mod logging;
mod stdio;
mod transform;

pub use codec::{WasmCodec, WasmCodecError, WasmCodecType};
pub use loader::{WasmCodecClassLoader, WasmCodecLoaderError};

#[cfg(single_wasm_runtime)]
pub fn init_codecs<'py>(
    py: pyo3::Python<'py>,
    module: pyo3::Borrowed<'_, 'py, pyo3::types::PyModule>,
) -> Result<pyo3::Bound<'py, pyo3::types::PyModule>, core_error::LocationError<pyo3::PyErr>> {
    use pyo3::{prelude::*, PyTypeInfo};

    let codecs = pyo3::types::PyModule::new(py, "codecs")?;

    codecs.add_class::<WasmCodecClassLoader>()?;

    // FIXME: the __module__ is wrong in fcbench and the benchmark suite
    let __module__ = pyo3::intern!(py, "__module__");
    let module_str = format!("{}.{}", module.name()?, codecs.name()?);

    WasmCodecClassLoader::type_object(py).setattr(__module__, &module_str)?;

    module.add_submodule(&codecs)?;

    Ok(codecs)
}
