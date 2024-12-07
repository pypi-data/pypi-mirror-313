#![allow(clippy::missing_errors_doc)] // FIXME
#![allow(clippy::redundant_pub_crate)]

use pyo3::prelude::*;

use codecs_build as _;

mod benchmark;
pub mod compressor;
mod dataclass;
mod dataset;
mod metrics;
pub mod model;

#[pymodule]
#[pyo3(name = "_fcbench")]
fn fcbench<'py>(py: Python<'py>, module: &Bound<'py, PyModule>) -> Result<(), PyErr> {
    let logger = pyo3_log::Logger::new(py, pyo3_log::Caching::Nothing)?;
    logger
        .install()
        .map_err(|err| core_error::pyerr_from_location_err(py, err))?;

    let benchmark = benchmark::create_module(py)?;
    let codecs = codecs_frontend::init_codecs(py, module.as_borrowed())
        .map_err(core_error::LocationError::into_error)?;
    let compressor = compressor::create_module(py)?;
    let dataset = dataset::create_module(py)?;
    let metrics = metrics::create_module(py)?;
    let model = model::create_module(py)?;

    module.add_submodule(&benchmark)?;
    module.add_submodule(&codecs)?;
    module.add_submodule(&compressor)?;
    module.add_submodule(&dataset)?;
    module.add_submodule(&metrics)?;
    module.add_submodule(&model)?;

    Ok(())
}
