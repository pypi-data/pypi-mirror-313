#[derive(thiserror::Error, Debug, Clone, Copy, PartialEq, Eq)]
#[repr(u16)]
pub enum ErrorKind {
    #[error("expected key")]
    ExpectedKey,

    #[error("expected value")]
    ExpectedValue,

    #[error("unknown token")]
    UnknownToken,

    #[error("unknown line")]
    UnknownLine,

    #[error("expected '='")]
    ExpectedEqual,

    #[error("expected ','")]
    ExpectedComma,

    #[error("expected ']'")]
    ExpectedBracketEnd,

    #[error("expected ']]'")]
    ExpectedDoubleBracketEnd,

    #[error("expected '}}'")]
    ExpectedBraceEnd,

    #[error("expected '\\n' or comment")]
    ExpectedLineBreakOrComment,

    #[error("Invalid key")]
    InvalidKey,

    #[error("Inline table must be single line")]
    InlineTableMustSingleLine,

    #[error("Forbidden last comma in inline table")]
    ForbiddenInlineTableLastComma,
}

#[derive(thiserror::Error, Debug, Clone, PartialEq, Eq)]
pub struct Error {
    kind: ErrorKind,
    range: text::Range,
}

impl Error {
    pub fn new(kind: ErrorKind, range: text::Range) -> Self {
        Self { kind, range }
    }

    pub fn kind(&self) -> ErrorKind {
        self.kind
    }

    pub fn message(&self) -> String {
        self.kind.to_string()
    }

    pub fn range(&self) -> text::Range {
        self.range
    }
}

impl std::fmt::Display for Error {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        self.kind.fmt(f)
    }
}
