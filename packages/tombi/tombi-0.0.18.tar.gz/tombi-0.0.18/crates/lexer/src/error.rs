#[derive(Debug, PartialEq, Eq)]
pub struct Error {
    kind: ErrorKind,
    span: text::Span,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ErrorKind {
    InvalidOffsetDatetime,
    InvalidLocalDatetime,
    InvalidLocalDate,
    InvalidLocalTime,
}

impl Error {
    pub fn new(kind: ErrorKind, span: text::Span) -> Self {
        Self { kind, span }
    }

    pub fn kind(&self) -> ErrorKind {
        self.kind
    }

    pub fn span(&self) -> text::Span {
        self.span
    }
}
