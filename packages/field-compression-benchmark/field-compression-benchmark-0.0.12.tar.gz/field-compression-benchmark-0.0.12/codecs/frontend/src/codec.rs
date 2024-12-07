use std::sync::{Arc, Mutex};

use codecs_wasm_host::{CodecPlugin, GuestError, RuntimeError};
use core_error::LocationError;
use numcodecs::{
    AnyArray, AnyArrayView, AnyArrayViewMut, AnyCowArray, Codec, DynCodec, DynCodecType,
};
use schemars::Schema;
use serde::Serializer;
use wasm_component_layer::Component;

#[derive(Debug, thiserror::Error)]
pub enum WasmCodecError {
    #[error("{codec_id} codec was poisoned")]
    Poisoned { codec_id: Arc<str> },
    #[error("{codec_id} codec's WASM host runtime raised an error")]
    Runtime {
        codec_id: Arc<str>,
        source: LocationError<RuntimeError>,
    },
    #[error("{codec_id} codec's WASM guest raised an error")]
    Guest {
        codec_id: Arc<str>,
        source: GuestError,
    },
}

pub struct WasmCodec {
    codec: Mutex<codecs_wasm_host::WasmCodec>,
    ty: WasmCodecType,
}

impl WasmCodec {
    pub fn try_clone(&self) -> Result<Self, serde_json::Error> {
        let mut config = self.get_config(serde_json::value::Serializer)?;

        if let Some(config) = config.as_object_mut() {
            config.remove("id");
        }

        let codec = self.ty.codec_from_config(config)?;

        Ok(codec)
    }

    pub fn instruction_counter(&self) -> Result<u64, WasmCodecError> {
        let codec = self.codec.lock().map_err(|_| WasmCodecError::Poisoned {
            codec_id: self.ty.codec_id.clone(),
        })?;
        Ok(codec.instruction_counter())
    }
}

impl Clone for WasmCodec {
    fn clone(&self) -> Self {
        #[expect(clippy::expect_used)]
        self.try_clone()
            .expect("cloning a wasm codec should not fail")
    }
}

impl Codec for WasmCodec {
    type Error = WasmCodecError;

    fn encode(&self, data: AnyCowArray) -> Result<AnyArray, Self::Error> {
        let encoded = self
            .codec
            .lock()
            .map_err(|_| WasmCodecError::Poisoned {
                codec_id: self.ty.codec_id.clone(),
            })?
            .encode(data)
            .map_err(|err| WasmCodecError::Runtime {
                codec_id: self.ty.codec_id.clone(),
                source: err,
            })?
            .map_err(|err| WasmCodecError::Guest {
                codec_id: self.ty.codec_id.clone(),
                source: err,
            })?;
        Ok(encoded)
    }

    fn decode(&self, encoded: AnyCowArray) -> Result<AnyArray, Self::Error> {
        let decoded = self
            .codec
            .lock()
            .map_err(|_| WasmCodecError::Poisoned {
                codec_id: self.ty.codec_id.clone(),
            })?
            .decode(encoded)
            .map_err(|err| WasmCodecError::Runtime {
                codec_id: self.ty.codec_id.clone(),
                source: err,
            })?
            .map_err(|err| WasmCodecError::Guest {
                codec_id: self.ty.codec_id.clone(),
                source: err,
            })?;
        Ok(decoded)
    }

    fn decode_into(
        &self,
        encoded: AnyArrayView,
        decoded: AnyArrayViewMut,
    ) -> Result<(), Self::Error> {
        self.codec
            .lock()
            .map_err(|_| WasmCodecError::Poisoned {
                codec_id: self.ty.codec_id.clone(),
            })?
            .decode_into(encoded, decoded)
            .map_err(|err| WasmCodecError::Runtime {
                codec_id: self.ty.codec_id.clone(),
                source: err,
            })?
            .map_err(|err| WasmCodecError::Guest {
                codec_id: self.ty.codec_id.clone(),
                source: err,
            })?;
        Ok(())
    }
}

impl DynCodec for WasmCodec {
    type Type = WasmCodecType;

    fn ty(&self) -> Self::Type {
        WasmCodecType {
            codec_id: self.ty.codec_id.clone(),
            codec_config_schema: self.ty.codec_config_schema.clone(),
            component: self.ty.component.clone(),
            plugin_instantiater: self.ty.plugin_instantiater.clone(),
        }
    }

    fn get_config<S: Serializer>(&self, serializer: S) -> Result<S::Ok, S::Error> {
        let ok = self
            .codec
            .lock()
            .map_err(serde::ser::Error::custom)?
            .get_config(serializer)?;
        Ok(ok)
    }
}

pub struct WasmCodecType {
    pub(super) codec_id: Arc<str>,
    pub(super) codec_config_schema: Arc<Schema>,
    pub(super) component: Component,
    #[expect(clippy::type_complexity)]
    pub(super) plugin_instantiater:
        Arc<dyn Send + Sync + Fn(&Component) -> Result<CodecPlugin, LocationError<RuntimeError>>>,
}

impl DynCodecType for WasmCodecType {
    type Codec = WasmCodec;

    fn codec_id(&self) -> &str {
        &self.codec_id
    }

    fn codec_from_config<'de, D: serde::Deserializer<'de>>(
        &self,
        config: D,
    ) -> Result<Self::Codec, D::Error> {
        let plugin =
            (self.plugin_instantiater)(&self.component).map_err(serde::de::Error::custom)?;
        let codec = CodecPlugin::from_config(plugin, config).map_err(serde::de::Error::custom)?;

        Ok(WasmCodec {
            codec: Mutex::new(codec),
            ty: Self {
                codec_id: self.codec_id.clone(),
                codec_config_schema: self.codec_config_schema.clone(),
                component: self.component.clone(),
                plugin_instantiater: self.plugin_instantiater.clone(),
            },
        })
    }

    fn codec_config_schema(&self) -> Schema {
        (*self.codec_config_schema).clone()
    }
}
