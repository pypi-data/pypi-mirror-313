#[derive(thiserror::Error, Debug, Clone, PartialEq, Eq)]
pub enum Error {
    #[cfg(feature = "load")]
    #[error("syntax error: {0}")]
    Syntax(syntax::SyntaxError),

    #[error("duplicate key: {key}")]
    DuplicateKey { key: String, range: text::Range },

    #[error("invalid integer: {error}")]
    ParseIntError {
        error: std::num::ParseIntError,
        range: text::Range,
    },

    #[error("invalid float: {error}")]
    ParseFloatError {
        error: std::num::ParseFloatError,
        range: text::Range,
    },

    #[error("invalid offset date time: {error}")]
    ParseOffsetDateTimeError {
        error: chrono::ParseError,
        range: text::Range,
    },

    #[error("invalid local date time: {error}")]
    ParseLocalDateTimeError {
        error: chrono::ParseError,
        range: text::Range,
    },

    #[error("invalid local date: {error}")]
    ParseLocalDateError {
        error: chrono::format::ParseError,
        range: text::Range,
    },

    #[error("invalid local time: {error}")]
    ParseLocalTimeError {
        error: chrono::format::ParseError,
        range: text::Range,
    },
}
