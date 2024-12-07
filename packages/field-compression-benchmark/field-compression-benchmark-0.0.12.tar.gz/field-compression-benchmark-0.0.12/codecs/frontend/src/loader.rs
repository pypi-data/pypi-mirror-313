use std::{convert::Infallible, path::Path, sync::Arc};

use codecs_wasm_host::{CodecPlugin, RuntimeError};
use pyo3::prelude::*;
use wasm_component_layer::{Component, Linker, Store};
use wasm_runtime_layer::{backend::WasmEngine, Engine};

use core_error::LocationError;

use crate::{
    codec::WasmCodecType, engine::ValidatedEngine, logging, stdio,
    transform::transform_wasm_component,
};

#[derive(Debug, thiserror::Error)]
pub enum WasmCodecLoaderError {
    #[error(transparent)]
    Runtime(LocationError<RuntimeError>),
    #[error("failed to read the WASM codec binary file")]
    ReadWasmBinaryFile { source: std::io::Error },
    #[error("failed to instantiate the WASM codec to extract its metadata")]
    Instantiation { source: LocationError<RuntimeError> },
}

#[pyclass(frozen)]
pub struct WasmCodecClassLoader {
    _inner: Infallible,
}

#[pymethods]
impl WasmCodecClassLoader {
    #[cfg(single_wasm_runtime)]
    #[staticmethod]
    #[expect(clippy::needless_pass_by_value)] // pyo3 requires path to be owned
    pub fn load<'py>(
        py: Python<'py>,
        path: std::path::PathBuf,
        module: &Bound<'py, PyModule>,
    ) -> Result<Bound<'py, numcodecs_python::PyCodecClass>, PyErr> {
        use core_error::pyerr_from_location_err;

        let ty = Self::new_type_from_path_with_default_engine(&path)
            .map_err(|err| pyerr_from_location_err(py, err))?;

        numcodecs_python::export_codec_class(py, ty, module.as_borrowed())
    }
}

impl WasmCodecClassLoader {
    pub fn new_type<E: Send + Sync + WasmEngine>(
        wasm_component: impl Into<Vec<u8>>,
        engine: E,
    ) -> Result<WasmCodecType, LocationError<WasmCodecLoaderError>>
    where
        Store<(), ValidatedEngine<E>>: Send + Sync,
    {
        let wasm_component = transform_wasm_component(wasm_component)?;

        let engine = Engine::new(ValidatedEngine::new(engine));
        let component = Component::new(&engine, &wasm_component)
            .map_err(LocationError::from2)
            .map_err(WasmCodecLoaderError::Runtime)?;

        let plugin_instantiater = Arc::new(move |component: &Component| {
            let mut ctx = Store::new(&engine, ());

            let mut linker = Linker::default();
            stdio::add_to_linker(&mut linker, &mut ctx).map_err(LocationError::from2)?;
            logging::add_to_linker(&mut linker, &mut ctx).map_err(LocationError::from2)?;

            let instance = linker
                .instantiate(&mut ctx, component)
                .map_err(LocationError::from2)?;

            CodecPlugin::new(instance, ctx)
        });

        let mut plugin: CodecPlugin = (plugin_instantiater)(&component)
            .map_err(|err| WasmCodecLoaderError::Instantiation { source: err })?;
        let codec_id = plugin.codec_id().map_err(WasmCodecLoaderError::Runtime)?;
        let codec_config_schema = plugin
            .codec_config_schema()
            .map_err(WasmCodecLoaderError::Runtime)?;

        Ok(WasmCodecType {
            codec_id: Arc::from(codec_id),
            codec_config_schema: Arc::from(codec_config_schema),
            component,
            plugin_instantiater,
        })
    }

    pub fn new_type_from_path<E: Send + Sync + WasmEngine>(
        path: &Path,
        engine: E,
    ) -> Result<WasmCodecType, LocationError<WasmCodecLoaderError>>
    where
        Store<(), ValidatedEngine<E>>: Send + Sync,
    {
        let wasm_component = std::fs::read(path)
            .map_err(|err| WasmCodecLoaderError::ReadWasmBinaryFile { source: err })?;

        Self::new_type(wasm_component, engine)
    }

    #[cfg(single_wasm_runtime)]
    pub fn new_type_from_path_with_default_engine(
        path: &Path,
    ) -> Result<WasmCodecType, LocationError<WasmCodecLoaderError>> {
        let engine = Self::default_engine(path)?;

        Self::new_type_from_path(path, engine)
    }
}

#[cfg(all(single_wasm_runtime, feature = "wasmtime"))]
impl WasmCodecClassLoader {
    // codecs don't need to preallocate the full 4GB wasm32 memory space, but
    //  still give them a reasonable static allocation for better codegen
    const DYNAMIC_MEMORY_RESERVED_FOR_GROWTH: u32 = Self::WASM_PAGE_SIZE * 16 * 64 /* 64MiB */;
    const MEMORY_GUARD_SIZE: u32 = Self::WASM_PAGE_SIZE * 16 * 64 /* 64MiB */;
    const STATIC_MEMORY_MAXIMUM_SIZE: u32 = Self::WASM_PAGE_SIZE * 16 * 64 /* 64MiB */;
    const WASM_PAGE_SIZE: u32 = 0x10000 /* 64kiB */;

    fn default_engine(
        path: &Path,
    ) -> Result<wasmtime_runtime_layer::Engine, LocationError<WasmCodecLoaderError>> {
        let mut config = wasmtime::Config::new();
        config
            .cranelift_nan_canonicalization(true)
            .cranelift_opt_level(wasmtime::OptLevel::Speed)
            .static_memory_maximum_size(u64::from(Self::STATIC_MEMORY_MAXIMUM_SIZE))
            .memory_guard_size(u64::from(Self::MEMORY_GUARD_SIZE))
            .dynamic_memory_reserved_for_growth(u64::from(Self::DYNAMIC_MEMORY_RESERVED_FOR_GROWTH))
            // WASM feature restrictions, follows the feature validation in
            //  ValidatedModule::new
            .wasm_bulk_memory(true)
            .wasm_custom_page_sizes(false)
            .wasm_extended_const(false)
            .wasm_function_references(false)
            .wasm_gc(false)
            .wasm_memory64(false)
            .wasm_multi_memory(true)
            .wasm_multi_value(true)
            .wasm_reference_types(false)
            .wasm_relaxed_simd(false)
            .wasm_simd(true)
            .wasm_tail_call(false)
            // wasmtime is compiled without the `threads` feature
            // .wasm_threads(false)
            .wasm_wide_arithmetic(true);

        // TODO: allow configuration to be taken from somewhere else
        let cache_path = path.with_file_name("wasmtime.toml");
        if cache_path.exists() {
            config
                .cache_config_load(cache_path)
                .map_err(LocationError::from2)
                .map_err(WasmCodecLoaderError::Runtime)?;
        }

        let engine = wasmtime::Engine::new(&config)
            .map_err(LocationError::from2)
            .map_err(WasmCodecLoaderError::Runtime)?;
        Ok(wasmtime_runtime_layer::Engine::new(engine))
    }
}

#[cfg(all(single_wasm_runtime, feature = "pyodide"))]
impl WasmCodecClassLoader {
    #[expect(clippy::unnecessary_wraps)]
    fn default_engine(
        _path: &Path,
    ) -> Result<pyodide_webassembly_runtime_layer::Engine, LocationError<WasmCodecLoaderError>>
    {
        Ok(pyodide_webassembly_runtime_layer::Engine::default())
    }
}
