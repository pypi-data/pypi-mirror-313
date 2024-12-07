use std::fmt;

use numcodecs_python::PyCodecClass;
use pyo3::{
    intern,
    prelude::*,
    sync::GILOnceCell,
    types::{IntoPyDict, PyString},
};
use vecmap::{VecMap, VecSet};

use crate::parameter::{Parameter, ParameterEvalContext, ParameterSeed};

use super::{Codec, Utf8CStr};

pub struct CodecSeed<'a, 'py> {
    py: Python<'py>,
    codecs: &'a mut VecMap<String, Codec>,
    eval_context: &'a mut ParameterEvalContext,
}

impl<'a, 'py> CodecSeed<'a, 'py> {
    pub fn new(
        py: Python<'py>,
        codecs: &'a mut VecMap<String, Codec>,
        eval_context: &'a mut ParameterEvalContext,
    ) -> Self {
        Self {
            py,
            codecs,
            eval_context,
        }
    }
}

impl<'de> serde::de::DeserializeSeed<'de> for CodecSeed<'_, '_> {
    type Value = ();

    fn deserialize<D: serde::Deserializer<'de>>(
        self,
        deserializer: D,
    ) -> Result<Self::Value, D::Error> {
        serde::Deserializer::deserialize_struct(deserializer, "Codec", FIELDS, self)
    }
}

const FIELDS: &[&str] = &["name", "import_path", "import", "kind", "parameters"];

#[derive(Clone, Copy)]
enum Field {
    Name,
    Import,
    Kind,
    Parameters,
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
        formatter.write_str("a codec config field identifier")
    }

    fn visit_str<E: serde::de::Error>(self, value: &str) -> Result<Self::Value, E> {
        match (self, value) {
            (Self::Name, "name")
            | (Self::Import, "import_path" | "import")
            | (Self::Kind, "kind")
            | (Self::Parameters, "parameters") => Ok(()),
            _ => Err(serde::de::Error::unknown_field(
                value,
                match self {
                    Self::Name => &["name"],
                    Self::Import => &["import_path", "import"],
                    Self::Kind => &["kind"],
                    Self::Parameters => &["parameters"],
                    Self::Excessive => &[],
                },
            )),
        }
    }

    fn visit_bytes<E: serde::de::Error>(self, value: &[u8]) -> Result<Self::Value, E> {
        match (self, value) {
            (Self::Name, b"name")
            | (Self::Import, b"import_path" | b"import")
            | (Self::Kind, b"kind")
            | (Self::Parameters, b"parameters") => Ok(()),
            _ => {
                let value = String::from_utf8_lossy(value);
                Err(serde::de::Error::unknown_field(
                    &value,
                    match self {
                        Self::Name => &["name"],
                        Self::Import => &["import_path", "import"],
                        Self::Kind => &["kind"],
                        Self::Parameters => &["parameters"],
                        Self::Excessive => &[],
                    },
                ))
            },
        }
    }
}

struct CodecNameSeed<'a, 'py> {
    py: Python<'py>,
    codecs: &'a VecMap<String, Codec>,
}

impl<'de> serde::de::DeserializeSeed<'de> for CodecNameSeed<'_, '_> {
    type Value = String;

    fn deserialize<D: serde::Deserializer<'de>>(
        self,
        deserializer: D,
    ) -> Result<Self::Value, D::Error> {
        deserializer.deserialize_str(self)
    }
}

impl serde::de::Visitor<'_> for CodecNameSeed<'_, '_> {
    type Value = String;

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("a codec name")
    }

    fn visit_str<E: serde::de::Error>(self, v: &str) -> Result<Self::Value, E> {
        if self.codecs.contains_key(v) {
            return Err(serde::de::Error::custom(format!(
                "duplicate codec name `{v}`"
            )));
        }

        let is_identifier: bool = (|| {
            PyString::new(self.py, v)
                .call_method0(intern!(self.py, "isidentifier"))?
                .extract()
        })()
        .map_err(serde::de::Error::custom)?;

        if !is_identifier {
            return Err(serde::de::Error::custom(format!(
                "invalid codec name `{v}`: not a valid identifier"
            )));
        }

        Ok(String::from(v))
    }
}

struct CodecImportSeed<'py> {
    py: Python<'py>,
}

impl<'de> serde::de::DeserializeSeed<'de> for CodecImportSeed<'_> {
    type Value = (Box<Utf8CStr>, VecSet<String>);

    fn deserialize<D: serde::Deserializer<'de>>(
        self,
        deserializer: D,
    ) -> Result<Self::Value, D::Error> {
        deserializer.deserialize_str(self)
    }
}

impl serde::de::Visitor<'_> for CodecImportSeed<'_> {
    type Value = (Box<Utf8CStr>, VecSet<String>);

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("a codec import string")
    }

    fn visit_str<E: serde::de::Error>(self, v: &str) -> Result<Self::Value, E> {
        fn visit_str_inner(py: Python, import_path: &Utf8CStr) -> Result<VecSet<String>, PyErr> {
            static INSPECT_SIGNATURE: GILOnceCell<Py<PyAny>> = GILOnceCell::new();

            let mut locals = Vec::new();
            for (pos, c) in import_path.as_str().char_indices() {
                if c == '.' {
                    if let Some(module) = import_path.as_str().get(..pos) {
                        locals.push((module, py.import(module)?));
                    }
                }
            }
            let locals = locals.into_py_dict(py)?;

            let ty: Bound<PyCodecClass> = py
                .eval(import_path.as_cstr(), None, Some(&locals))?
                .extract()?;

            // TODO: Could we look into the parameter annotations and check the type?
            let parameters = INSPECT_SIGNATURE
                .import(py, "inspect", "signature")?
                .call1((ty.getattr(intern!(py, "__init__"))?,))?
                .getattr(intern!(py, "parameters"))?
                .call_method0(intern!(py, "keys"))?
                .try_iter()?
                .map(|name| name.and_then(|name| name.extract()))
                .collect::<Result<VecSet<_>, _>>()?;

            Ok(parameters)
        }

        let mut v = String::from(v);
        if !v.contains('\0') {
            v.push('\0');
        }
        let v = Utf8CStr::from_boxed_str(v.into_boxed_str()).map_err(serde::de::Error::custom)?;

        match visit_str_inner(self.py, &v) {
            Ok(parameters) => Ok((v, parameters)),
            Err(err) => Err(serde::de::Error::custom(err)),
        }
    }
}

struct CodecParameterNameSeed<'a> {
    import_path: &'a str,
    parameters: &'a VecSet<String>,
    parameters_seen: &'a mut VecSet<String>,
}

impl<'de> serde::de::DeserializeSeed<'de> for CodecParameterNameSeed<'_> {
    type Value = String;

    fn deserialize<D: serde::Deserializer<'de>>(
        self,
        deserializer: D,
    ) -> Result<Self::Value, D::Error> {
        deserializer.deserialize_str(self)
    }
}

impl serde::de::Visitor<'_> for CodecParameterNameSeed<'_> {
    type Value = String;

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("a parameter name")
    }

    fn visit_str<E: serde::de::Error>(self, v: &str) -> Result<Self::Value, E> {
        if !self.parameters.contains(v) {
            return Err(serde::de::Error::custom(format!(
                "codec {} does not have a parameter named {v:?}",
                self.import_path
            )));
        }

        if !self.parameters_seen.insert(String::from(v)) {
            return Err(serde::de::Error::custom(format!(
                "duplicate parameter name {v:?}"
            )));
        }

        Ok(String::from(v))
    }
}

struct CodecParametersSeed<'a> {
    name: &'a str,
    import_path: &'a str,
    parameters: VecSet<String>,
    parameters_seen: VecSet<String>,
    eval_context: &'a mut ParameterEvalContext,
}

impl<'de> serde::de::DeserializeSeed<'de> for CodecParametersSeed<'_> {
    type Value = VecMap<String, Parameter>;

    fn deserialize<D: serde::Deserializer<'de>>(
        self,
        deserializer: D,
    ) -> Result<Self::Value, D::Error> {
        deserializer.deserialize_map(self)
    }
}

impl<'de> serde::de::Visitor<'de> for CodecParametersSeed<'_> {
    type Value = VecMap<String, Parameter>;

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("a map of parameters")
    }

    fn visit_map<A: serde::de::MapAccess<'de>>(
        mut self,
        mut map: A,
    ) -> Result<Self::Value, A::Error> {
        let mut parameters = VecMap::with_capacity(map.size_hint().unwrap_or(0));

        while let Some(name) = map.next_key_seed(CodecParameterNameSeed {
            import_path: self.import_path,
            parameters: &self.parameters,
            parameters_seen: &mut self.parameters_seen,
        })? {
            let parameter = map.next_value_seed(ParameterSeed::new(self.eval_context))?;

            self.eval_context
                .set_value(
                    self.name,
                    &name,
                    &parameter
                        .example(self.name, &name, self.eval_context)
                        .map_err(serde::de::Error::custom)?,
                )
                .map_err(serde::de::Error::custom)?;

            parameters.insert(name, parameter);
        }

        Ok(parameters)
    }
}

impl<'de> serde::de::Visitor<'de> for CodecSeed<'_, '_> {
    type Value = ();

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("a codec config")
    }

    fn visit_map<A: serde::de::MapAccess<'de>>(self, mut map: A) -> Result<Self::Value, A::Error> {
        let Some(()) = map.next_key_seed(Field::Name)? else {
            return Err(serde::de::Error::custom(
                "a codec must start with a `name` field",
            ));
        };

        let name = map.next_value_seed(CodecNameSeed {
            py: self.py,
            codecs: self.codecs,
        })?;

        let Some(()) = map.next_key_seed(Field::Import)? else {
            return Err(serde::de::Error::custom(
                "a codec must continue with an `import` field",
            ));
        };

        let (import, parameters) = map.next_value_seed(CodecImportSeed { py: self.py })?;

        let Some(()) = map.next_key_seed(Field::Kind)? else {
            return Err(serde::de::Error::custom(
                "a codec must continue with a `kind` field",
            ));
        };

        let kind = map.next_value()?;

        let Some(()) = map.next_key_seed(Field::Parameters)? else {
            return Err(serde::de::Error::custom(
                "a codec must continue with a `parameters` field",
            ));
        };

        let parameters = map.next_value_seed(CodecParametersSeed {
            name: &name,
            import_path: import.as_str(),
            parameters_seen: VecSet::with_capacity(parameters.len()),
            parameters,
            eval_context: self.eval_context,
        })?;

        map.next_key_seed(Field::Excessive)?;

        self.codecs.insert(
            name.clone(),
            Codec {
                name,
                import_path: import,
                kind,
                parameters,
            },
        );

        Ok(())
    }
}
