use std::borrow::Cow;

use config::TomlVersion;

pub struct Linter<'a> {
    toml_version: TomlVersion,
    options: Cow<'a, crate::LintOptions>,
    diagnostics: Vec<crate::Diagnostic>,
}

impl<'a> Linter<'a> {
    #[inline]
    pub fn new(toml_version: TomlVersion, options: &'a crate::LintOptions) -> Self {
        Self {
            toml_version,
            options: Cow::Borrowed(options),
            diagnostics: Vec::new(),
        }
    }

    #[inline]
    #[allow(dead_code)]
    pub fn toml_version(&self) -> TomlVersion {
        self.toml_version
    }

    #[inline]
    #[allow(dead_code)]
    pub fn options(&self) -> &crate::LintOptions {
        &self.options
    }

    #[inline]
    pub fn into_diagnostics(self) -> Vec<crate::Diagnostic> {
        self.diagnostics
    }

    #[inline]
    pub fn add_diagnostic(&mut self, diagnostic: crate::Diagnostic) {
        self.diagnostics.push(diagnostic);
    }
}
