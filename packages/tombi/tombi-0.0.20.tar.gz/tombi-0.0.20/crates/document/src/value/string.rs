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
}

impl String {
    pub fn new_basic_string(text: &str) -> Self {
        Self {
            kind: StringKind::BasicString,
            value: text.to_string(),
        }
    }

    pub fn new_literal_string(text: &str) -> Self {
        Self {
            kind: StringKind::LiteralString,
            value: text.to_string(),
        }
    }

    pub fn new_multi_line_basic_string(text: &str) -> Self {
        Self {
            kind: StringKind::MultiLineBasicString,
            value: text.to_string(),
        }
    }

    pub fn new_multi_line_literal_string(text: &str) -> Self {
        Self {
            kind: StringKind::MultiLineLiteralString,
            value: text.to_string(),
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
}

impl TryFrom<ast::BasicString> for String {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::BasicString) -> Result<Self, Self::Error> {
        let token = node.token().unwrap();
        Ok(Self::new_basic_string(token.text()))
    }
}

impl TryFrom<ast::LiteralString> for String {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::LiteralString) -> Result<Self, Self::Error> {
        let token = node.token().unwrap();
        Ok(Self::new_literal_string(token.text()))
    }
}

impl TryFrom<ast::MultiLineBasicString> for String {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::MultiLineBasicString) -> Result<Self, Self::Error> {
        let token = node.token().unwrap();
        Ok(Self::new_multi_line_basic_string(token.text()))
    }
}

impl TryFrom<ast::MultiLineLiteralString> for String {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::MultiLineLiteralString) -> Result<Self, Self::Error> {
        let token = node.token().unwrap();
        Ok(Self::new_multi_line_literal_string(token.text()))
    }
}

#[cfg(feature = "serde")]
impl serde::Serialize for String {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: serde::Serializer,
    {
        match self.kind {
            StringKind::BasicString => self.value[1..self.value.len() - 1].replace(r#"\""#, r#"""#),
            StringKind::LiteralString => self.value[1..self.value.len() - 1].replace(r#"\'"#, "'"),
            StringKind::MultiLineBasicString => {
                self.value[3..self.value.len() - 3].replace(r#"\""#, r#"""#)
            }
            StringKind::MultiLineLiteralString => {
                self.value[3..self.value.len() - 3].replace(r#"\'"#, "'")
            }
        }
        .serialize(serializer)
    }
}
