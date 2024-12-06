use syntax::SyntaxKind;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Token {
    kind: SyntaxKind,
    span: text::Span,
    range: text::Range,
}

impl Token {
    pub fn new(kind: SyntaxKind, (span, range): (text::Span, text::Range)) -> Self {
        Self { kind, span, range }
    }

    pub const fn eof() -> Self {
        Self {
            kind: SyntaxKind::EOF,
            span: text::Span::MAX,
            range: text::Range::MAX,
        }
    }

    #[inline]
    pub fn is_eof(&self) -> bool {
        self.kind == SyntaxKind::EOF
    }

    #[inline]
    pub fn kind(&self) -> SyntaxKind {
        self.kind
    }

    #[inline]
    pub fn span(&self) -> text::Span {
        self.span
    }

    #[inline]
    pub fn range(&self) -> text::Range {
        self.range
    }
}
