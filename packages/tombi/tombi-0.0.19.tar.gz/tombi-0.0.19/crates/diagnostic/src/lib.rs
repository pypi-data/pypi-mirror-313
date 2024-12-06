mod level;
pub mod printer;

pub use level::Level;
pub use printer::Print;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Diagnostic {
    level: level::Level,
    message: String,
    range: text::Range,
    source_file: Option<std::path::PathBuf>,
}

impl Diagnostic {
    #[inline]
    pub fn new_warning(message: impl Into<String>, range: impl Into<text::Range>) -> Self {
        Self {
            level: level::Level::WARNING,
            message: message.into(),
            range: range.into(),
            source_file: None,
        }
    }

    #[inline]
    pub fn new_error(message: impl Into<String>, range: impl Into<text::Range>) -> Self {
        Self {
            level: level::Level::ERROR,
            message: message.into(),
            range: range.into(),
            source_file: None,
        }
    }

    pub fn with_source_file(mut self, source_file: impl Into<std::path::PathBuf>) -> Self {
        self.source_file = Some(source_file.into());
        self
    }

    #[inline]
    pub fn level(&self) -> level::Level {
        self.level
    }

    #[inline]
    pub fn message(&self) -> &str {
        &self.message
    }

    #[inline]
    pub fn position(&self) -> text::Position {
        self.range.start()
    }

    #[inline]
    pub fn range(&self) -> text::Range {
        self.range
    }

    #[inline]
    pub fn source_file(&self) -> Option<&std::path::Path> {
        self.source_file.as_deref()
    }
}
