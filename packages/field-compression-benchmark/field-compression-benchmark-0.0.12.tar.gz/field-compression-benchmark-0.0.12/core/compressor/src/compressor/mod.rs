use std::{
    borrow::Cow,
    fmt, fs,
    ops::ControlFlow,
    path::{Path, PathBuf},
};

use numcodecs_python::PyCodec;
use pyo3::prelude::*;
use thiserror::Error;
use vecmap::{VecMap, VecSet};

use core_error::LocationError;

mod config;

use self::config::CompressorSeed;
use crate::{
    codec::{Codec, ConcreteCodec, ConcreteCodecIterator, ConcreteCodecSummary},
    parameter::{ParameterEvalContext, ParameterEvalError},
};

#[derive(Debug, Clone)]
pub struct Compressor {
    config_path: Option<PathBuf>,
    name: String,
    codecs: VecMap<String, Codec>,
}

impl Compressor {
    pub fn from_deserialised_config<'py: 'de, 'de, D: serde::Deserializer<'de>>(
        py: Python<'py>,
        deserializer: D,
    ) -> Result<Self, D::Error> {
        serde::de::DeserializeSeed::deserialize(CompressorSeed::new(py, None, None), deserializer)
    }

    pub fn from_config_str(
        py: Python,
        config: &str,
    ) -> Result<Self, LocationError<ParseCompressorError>> {
        Self::from_deserialised_config(py, toml::Deserializer::new(config))
            .map_err(|err| ParseCompressorError::ParseConfig { source: err })
            .map_err(LocationError::new)
    }

    pub fn from_config_file(
        py: Python,
        config_file: &Path,
    ) -> Result<Self, LocationError<ParseCompressorError>> {
        let config =
            fs::read_to_string(config_file).map_err(|err| ParseCompressorError::ReadFile {
                source: err,
                file: config_file.to_path_buf(),
            })?;

        serde::de::DeserializeSeed::deserialize(
            CompressorSeed::new(py, Some(config_file.to_path_buf()), None),
            toml::Deserializer::new(&config),
        )
        .map_err(|err| ParseCompressorError::ParseConfigFile {
            source: err,
            file: config_file.to_path_buf(),
        })
        .map_err(LocationError::new)
    }

    pub fn from_config_files(
        py: Python,
        config_files: &VecSet<PathBuf>,
    ) -> Result<VecMap<String, Self>, LocationError<ParseCompressorError>> {
        let mut compressors = VecMap::with_capacity(config_files.len());
        let mut compressor_names = VecMap::with_capacity(config_files.len());

        for path in config_files {
            let config =
                fs::read_to_string(path).map_err(|err| ParseCompressorError::ReadFile {
                    source: err,
                    file: path.clone(),
                })?;

            let compressor = serde::de::DeserializeSeed::deserialize(
                CompressorSeed::new(py, Some(path.clone()), Some(&mut compressor_names)),
                toml::Deserializer::new(&config),
            )
            .map_err(|err| ParseCompressorError::ParseConfigFile {
                source: err,
                file: path.clone(),
            })?;

            if let Some(conflict) = compressors.insert(compressor.name.clone(), compressor) {
                return Err(ParseCompressorError::DuplicateCompressor {
                    name: conflict.name,
                    path: path.clone(),
                }
                .into());
            }
        }

        Ok(compressors)
    }

    pub fn from_config_directory(
        py: Python,
        config_directory: &Path,
    ) -> Result<VecMap<String, Self>, LocationError<ParseCompressorError>> {
        let mut config_files = VecSet::new();

        for path in
            fs::read_dir(config_directory).map_err(|err| ParseCompressorError::ReadDirectory {
                source: err,
                directory: config_directory.to_path_buf(),
            })?
        {
            let path = path
                .map_err(|err| ParseCompressorError::QueryFile {
                    source: err,
                    directory: config_directory.to_path_buf(),
                })?
                .path();

            if !matches!(path.extension(), Some(ext) if ext == "toml") {
                // Skip all non-config files in the directory
                continue;
            }

            config_files.insert(path);
        }

        Self::from_config_files(py, &config_files)
    }

    pub fn ensure_py_imports(&self, py: Python) -> Result<(), LocationError<PyErr>> {
        for codec in self.codecs.values() {
            let _codec = codec.import_py(py)?;
        }

        Ok(())
    }

    pub fn iter_concrete(&self) -> Result<ConcreteCompressorIterator, ParameterEvalError> {
        let codecs = self
            .codecs
            .values()
            .map(Codec::cyclic_iter_concrete)
            .collect::<Vec<_>>();

        Ok(ConcreteCompressorIterator {
            compressor: self,
            codecs,
            all_done: false,
            eval_context: ParameterEvalContext::new()?,
        })
    }

    #[must_use]
    pub fn name(&self) -> &str {
        &self.name
    }

    #[must_use]
    pub fn config_path(&self) -> Option<&Path> {
        self.config_path.as_deref()
    }

    #[must_use]
    pub fn codecs(&self) -> impl ExactSizeIterator<Item = &Codec> {
        self.codecs.values()
    }

    pub fn minimise(&mut self) {
        self.codecs.values_mut().for_each(Codec::minimise);
    }
}

impl fmt::Display for Compressor {
    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        fmt.write_fmt(format_args!("{}: raw ⇄ ", self.name))?;

        for codec in self.codecs.values() {
            fmt.write_fmt(format_args!("{codec} ⇄ "))?;
        }

        fmt.write_str("compressed")
    }
}

#[derive(Debug, Error)]
pub enum ParseCompressorError {
    #[error("failed to read the compressor config directory {directory:?}")]
    ReadDirectory {
        source: std::io::Error,
        directory: PathBuf,
    },
    #[error("failed to query a compressor config file in {directory:?}")]
    QueryFile {
        source: std::io::Error,
        directory: PathBuf,
    },
    #[error("failed to read the compressor config file {file:?}")]
    ReadFile {
        source: std::io::Error,
        file: PathBuf,
    },
    #[error("failed to parse the compressor config")]
    ParseConfig { source: toml::de::Error },
    #[error("failed to parse the compressor config file {file:?}")]
    ParseConfigFile {
        source: toml::de::Error,
        file: PathBuf,
    },
    #[error("duplicate compressor {name:?} at {path:?}")]
    DuplicateCompressor { name: String, path: PathBuf },
}

#[derive(Debug, Clone)]
pub struct ConcreteCompressor<'a> {
    compressor: &'a Compressor,
    codecs: Vec<ConcreteCodec<'a>>,
}

impl<'a> ConcreteCompressor<'a> {
    pub fn build_py<'py>(
        &self,
        py: Python<'py>,
    ) -> Result<Vec<Bound<'py, PyCodec>>, LocationError<PyErr>> {
        self.codecs
            .iter()
            .map(|codec| codec.build_py(py))
            .collect::<Result<Vec<_>, _>>()
    }

    #[must_use]
    pub fn name(&self) -> &str {
        self.compressor.name()
    }

    #[must_use]
    pub fn config_path(&self) -> Option<&Path> {
        self.compressor.config_path()
    }

    #[must_use]
    pub fn codecs(&self) -> impl ExactSizeIterator<Item = &ConcreteCodec<'a>> {
        self.codecs.iter()
    }

    #[must_use]
    pub fn summary(&self) -> ConcreteCompressorSummary<'a> {
        ConcreteCompressorSummary {
            name: Cow::Borrowed(self.compressor.name.as_str()),
            codecs: self.codecs.iter().map(ConcreteCodec::summary).collect(),
        }
    }
}

impl fmt::Display for ConcreteCompressor<'_> {
    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        fmt.write_fmt(format_args!("{}: raw ⇄ ", self.compressor.name()))?;

        for codec in &self.codecs {
            fmt.write_fmt(format_args!("{codec} ⇄ "))?;
        }

        fmt.write_str("compressed")
    }
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
#[serde(rename = "Compressor")]
#[serde(deny_unknown_fields)]
pub struct ConcreteCompressorSummary<'a> {
    name: Cow<'a, str>,
    #[serde(borrow)]
    codecs: Vec<ConcreteCodecSummary<'a>>,
}

pub struct ConcreteCompressorIterator<'a> {
    compressor: &'a Compressor,
    codecs: Vec<ConcreteCodecIterator<'a>>,
    all_done: bool,
    eval_context: ParameterEvalContext,
}

impl<'a> Iterator for ConcreteCompressorIterator<'a> {
    type Item = Result<ConcreteCompressor<'a>, ParameterEvalError>;

    fn next(&mut self) -> Option<Self::Item> {
        if self.all_done {
            return None;
        }

        self.all_done = true;
        self.eval_context.reset();

        #[expect(clippy::needless_collect)]
        // we must not short-circuit early to ensure further iteration is not broken
        let codecs = self
            .codecs
            .iter_mut()
            .map(|codec| -> Result<_, ParameterEvalError> {
                if self.all_done {
                    match codec.next(&mut self.eval_context)? {
                        ControlFlow::Break(codec) => Ok(codec),
                        ControlFlow::Continue(codec) => {
                            self.all_done = false;
                            Ok(codec)
                        },
                    }
                } else {
                    codec.get(&mut self.eval_context)
                }
            })
            .collect::<Vec<_>>();

        let codecs = codecs.into_iter().collect::<Result<Vec<_>, _>>();

        Some(codecs.map(|codecs| ConcreteCompressor {
            compressor: self.compressor,
            codecs,
        }))
    }
}

// Correctness: all_done guarantees that None is always returned after the first
//              `None`
impl std::iter::FusedIterator for ConcreteCompressorIterator<'_> {}
