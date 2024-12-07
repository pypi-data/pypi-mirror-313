fn main() {
    let wasmtime = check_has_feature("wasmtime");
    let pyodide = check_has_feature("pyodide");

    if wasmtime ^ pyodide {
        println!("cargo::rustc-cfg=single_wasm_runtime");
    }

    println!("cargo::rustc-check-cfg=cfg(single_wasm_runtime)");
}

// Inspired by the MIT-licensed https://crates.io/crates/cfg_aliases crate
fn check_has_feature(feature: &str) -> bool {
    std::env::var(format!(
        "CARGO_FEATURE_{}",
        feature.to_uppercase().replace('-', "_")
    ))
    .map(|x| x == "1")
    .unwrap_or(false)
}
