use std::{fmt, path::PathBuf};

use pyo3::prelude::*;
use vecmap::VecMap;

use crate::{
    codec::{Codec, CodecSeed},
    compressor::Compressor,
    parameter::ParameterEvalContext,
};

pub struct CompressorSeed<'a, 'py> {
    py: Python<'py>,
    path: Option<PathBuf>,
    compressors: Option<&'a mut VecMap<String, Option<PathBuf>>>,
}

impl<'a, 'py> CompressorSeed<'a, 'py> {
    #[must_use]
    pub fn new(
        py: Python<'py>,
        path: Option<PathBuf>,
        compressors: Option<&'a mut VecMap<String, Option<PathBuf>>>,
    ) -> Self {
        Self {
            py,
            path,
            compressors,
        }
    }
}

impl<'de> serde::de::DeserializeSeed<'de> for CompressorSeed<'_, 'de> {
    type Value = Compressor;

    fn deserialize<D: serde::Deserializer<'de>>(
        self,
        deserializer: D,
    ) -> Result<Self::Value, D::Error> {
        serde::Deserializer::deserialize_struct(deserializer, "Compressor", FIELDS, self)
    }
}

const FIELDS: &[&str] = &["name", "codec", "codecs"];

#[derive(Clone, Copy)]
enum Field {
    Name,
    Codec,
    Excessive,
}

impl<'de> serde::de::DeserializeSeed<'de> for Field {
    type Value = ();

    fn deserialize<D: serde::Deserializer<'de>>(
        self,
        deserializer: D,
    ) -> Result<Self::Value, D::Error> {
        serde::Deserializer::deserialize_identifier(deserializer, self)
    }
}

impl serde::de::Visitor<'_> for Field {
    type Value = ();

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("a compressor config field identifier")
    }

    fn visit_str<E: serde::de::Error>(self, value: &str) -> Result<Self::Value, E> {
        match (self, value) {
            (Self::Name, "name") | (Self::Codec, "codec" | "codecs") => Ok(()),
            _ => Err(serde::de::Error::unknown_field(
                value,
                match self {
                    Self::Name => &["name"],
                    Self::Codec => &["codec", "codecs"],
                    Self::Excessive => &[],
                },
            )),
        }
    }

    fn visit_bytes<E: serde::de::Error>(self, value: &[u8]) -> Result<Self::Value, E> {
        match (self, value) {
            (Self::Name, b"name") | (Self::Codec, b"codec" | b"codecs") => Ok(()),
            _ => {
                let value = String::from_utf8_lossy(value);
                Err(serde::de::Error::unknown_field(
                    &value,
                    match self {
                        Self::Name => &["name"],
                        Self::Codec => &["codec", "codecs"],
                        Self::Excessive => &[],
                    },
                ))
            },
        }
    }
}

struct CompressorNameSeed<'a> {
    path: Option<PathBuf>,
    compressors: Option<&'a mut VecMap<String, Option<PathBuf>>>,
}

impl<'de> serde::de::DeserializeSeed<'de> for CompressorNameSeed<'_> {
    type Value = String;

    fn deserialize<D: serde::Deserializer<'de>>(
        self,
        deserializer: D,
    ) -> Result<Self::Value, D::Error> {
        deserializer.deserialize_str(self)
    }
}

struct CompressorCodecsSeed<'py> {
    py: Python<'py>,
}

impl<'de> serde::de::DeserializeSeed<'de> for CompressorCodecsSeed<'_> {
    type Value = VecMap<String, Codec>;

    fn deserialize<D: serde::Deserializer<'de>>(
        self,
        deserializer: D,
    ) -> Result<Self::Value, D::Error> {
        deserializer.deserialize_seq(self)
    }
}

impl<'de> serde::de::Visitor<'de> for CompressorCodecsSeed<'_> {
    type Value = VecMap<String, Codec>;

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("a list of codecs")
    }

    fn visit_seq<A: serde::de::SeqAccess<'de>>(self, mut seq: A) -> Result<Self::Value, A::Error> {
        let mut codecs = VecMap::with_capacity(seq.size_hint().unwrap_or(0));
        let mut eval_context = ParameterEvalContext::new().map_err(serde::de::Error::custom)?;

        #[expect(clippy::equatable_if_let)]
        while let Some(()) =
            seq.next_element_seed(CodecSeed::new(self.py, &mut codecs, &mut eval_context))?
        {
            // no-op
        }

        Ok(codecs)
    }
}

impl serde::de::Visitor<'_> for CompressorNameSeed<'_> {
    type Value = String;

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("a compressor name")
    }

    fn visit_str<E: serde::de::Error>(self, v: &str) -> Result<Self::Value, E> {
        if let Some(compressors) = self.compressors {
            if let Some(path) = compressors.insert(String::from(v), self.path.clone()) {
                return Err(serde::de::Error::custom(format!(
                    "duplicate compressor {v:?} at {path:?} and {:?}",
                    self.path
                )));
            }
        }

        Ok(String::from(v))
    }
}

impl<'de> serde::de::Visitor<'de> for CompressorSeed<'_, '_> {
    type Value = Compressor;

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("a compressor config")
    }

    fn visit_map<A: serde::de::MapAccess<'de>>(self, mut map: A) -> Result<Self::Value, A::Error> {
        let Some(()) = map.next_key_seed(Field::Name)? else {
            return Err(serde::de::Error::custom(
                "a compressor must start with a `name` field",
            ));
        };

        let name = map.next_value_seed(CompressorNameSeed {
            path: self.path.clone(),
            compressors: self.compressors,
        })?;

        let Some(()) = map.next_key_seed(Field::Codec)? else {
            return Err(serde::de::Error::missing_field("codec"));
        };

        let codecs = map.next_value_seed(CompressorCodecsSeed { py: self.py })?;

        map.next_key_seed(Field::Excessive)?;

        Ok(Compressor {
            config_path: self.path,
            name,
            codecs,
        })
    }
}
