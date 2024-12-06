use std::path::PathBuf;

/// Returns the path to the root directory of `tombi` project.
pub fn project_root() -> PathBuf {
    let dir = std::env::var("CARGO_MANIFEST_DIR")
        .unwrap_or_else(|_| env!("CARGO_MANIFEST_DIR").to_owned());
    PathBuf::from(dir)
        .parent()
        .unwrap()
        .parent()
        .unwrap()
        .to_owned()
}

#[cfg(feature = "load")]
#[test]
fn load_tombi_toml() {
    use config::TomlVersion;
    use document::Document;

    let toml_path = project_root().join("tombi.toml");
    dbg!(&toml_path);
    assert!(toml_path.exists());

    let toml_source = std::fs::read_to_string(&toml_path).unwrap();
    let document = Document::load(&toml_source, TomlVersion::default()).unwrap();

    dbg!(document);
    assert!(false);
}
