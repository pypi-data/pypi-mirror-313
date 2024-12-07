#![cfg_attr(not(test), no_main)]

numcodecs_wasm_guest::export_codec!(
    codecs_wasm_logging::LoggingCodec<numcodecs_reinterpret::ReinterpretCodec>
);
