#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum StringKind {
    BasicString,
    LiteralString,
    MultiLineBasicString,
    MultiLineLiteralString,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct String {
    kind: StringKind,
    value: std::string::String,
    range: text::Range,
}

impl String {
    pub fn new_basic_string(text: &str, range: text::Range) -> Self {
        Self {
            kind: StringKind::BasicString,
            value: text.to_string(),
            range,
        }
    }

    pub fn new_literal_string(text: &str, range: text::Range) -> Self {
        Self {
            kind: StringKind::LiteralString,
            value: text.to_string(),
            range,
        }
    }

    pub fn new_multi_line_basic_string(text: &str, range: text::Range) -> Self {
        Self {
            kind: StringKind::MultiLineBasicString,
            value: text.to_string(),
            range,
        }
    }

    pub fn new_multi_line_literal_string(text: &str, range: text::Range) -> Self {
        Self {
            kind: StringKind::MultiLineLiteralString,
            value: text.to_string(),
            range,
        }
    }

    #[inline]
    pub fn kind(&self) -> StringKind {
        self.kind
    }

    #[inline]
    pub fn value(&self) -> &str {
        &self.value
    }

    #[inline]
    pub fn range(&self) -> text::Range {
        self.range
    }
}
