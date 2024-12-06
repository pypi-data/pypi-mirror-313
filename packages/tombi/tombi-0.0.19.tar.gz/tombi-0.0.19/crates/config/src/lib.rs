pub mod format;
mod lint;
mod toml_version;
pub use format::FormatOptions;
pub use lint::LintOptions;
pub use toml_version::TomlVersion;

const CONFIG_FILENAME: &str = "tombi.toml";
const PYPROJECT_FILENAME: &str = "pyproject.toml";
pub const DEFAULT_FORMAT_OPTIONS: FormatOptions = FormatOptions::default();
pub const DEFAULT_LINT_OPTIONS: LintOptions = LintOptions::default();

/// # Tombi
///
/// **Tombi** (鳶) is a toolkit for TOML; providing a formatter/linter and language server.
/// See the [GitHub repository](https://github.com/yassun7010/tombi) for more information.
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
#[cfg_attr(feature = "serde", serde(rename_all = "kebab-case"))]
#[cfg_attr(feature = "jsonschema", derive(schemars::JsonSchema))]
#[derive(Debug, Default, Clone)]
pub struct Config {
    /// # TOML version.
    pub toml_version: Option<TomlVersion>,

    /// # Formatter options.
    pub format: Option<FormatOptions>,

    /// # Linter options.
    pub lint: Option<LintOptions>,
}

#[doc(hidden)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
#[derive(Debug, Clone, Default)]
struct PyProjectToml {
    tool: Option<Tool>,
}

#[doc(hidden)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
#[derive(Debug, Clone, Default)]
struct Tool {
    tombi: Option<Config>,
}

#[cfg(feature = "serde")]
pub fn load() -> Config {
    let mut current_dir = std::env::current_dir().unwrap();
    loop {
        let config_path = current_dir.join(CONFIG_FILENAME);
        if config_path.exists() {
            tracing::debug!("{} found: {:?}", CONFIG_FILENAME, &config_path);

            let Ok(config_str) = std::fs::read_to_string(&config_path) else {
                tracing::error!("Failed to read {}: {:?}", CONFIG_FILENAME, &config_path);
                continue;
            };
            let Ok(config) = toml::from_str::<Config>(&config_str) else {
                tracing::error!(
                    "Failed to parse {} file: {:?}",
                    CONFIG_FILENAME,
                    &config_path
                );
                continue;
            };
            return config;
        }

        let pyproject_toml_path = current_dir.join(PYPROJECT_FILENAME);
        if pyproject_toml_path.exists() {
            tracing::debug!(
                "\"{}\" found: {:?}",
                PYPROJECT_FILENAME,
                pyproject_toml_path
            );

            let Ok(pyproject_toml_str) = std::fs::read_to_string(&pyproject_toml_path) else {
                tracing::error!(
                    "Failed to read {} file: {:?}",
                    PYPROJECT_FILENAME,
                    &pyproject_toml_path
                );
                continue;
            };
            let Ok(config) = toml::from_str::<PyProjectToml>(&pyproject_toml_str) else {
                tracing::error!(
                    "Failed to parse {} file: {:?}",
                    PYPROJECT_FILENAME,
                    &config_path
                );
                continue;
            };
            if let Some(Tool { tombi: Some(tombi) }) = config.tool {
                return tombi;
            } else {
                tracing::debug!("No [tool.tombi] found in \"{:?}\".", &config_path);
                continue;
            }
        }

        if !current_dir.pop() {
            break;
        }
    }

    tracing::debug!("No config file found.");
    tracing::debug!("Using default config.");

    Config::default()
}
