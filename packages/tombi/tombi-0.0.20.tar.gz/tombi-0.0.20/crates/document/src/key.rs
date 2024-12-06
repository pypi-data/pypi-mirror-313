#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct Key {
    value: String,
    range: text::Range,
}

impl Key {
    pub(crate) fn new(text: impl ToString, range: text::Range) -> Self {
        Self {
            value: text.to_string(),
            range,
        }
    }

    pub fn value(&self) -> &str {
        &self.value
    }

    pub(crate) fn range(&self) -> text::Range {
        self.range
    }
}

impl std::fmt::Display for Key {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.value)
    }
}

impl TryFrom<ast::Key> for Key {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::Key) -> Result<Self, Self::Error> {
        let (text, range) = match node {
            ast::Key::BareKey(bare_key) => {
                let token = bare_key.token().unwrap();
                (token.text().to_string(), token.text_range())
            }
            ast::Key::BasicString(basic_string) => {
                let token = basic_string.token().unwrap();
                (
                    token.text()[1..token.text().len() - 1].replace(r#"\""#, "\""),
                    token.text_range(),
                )
            }
            ast::Key::LiteralString(literal_string) => {
                let token = literal_string.token().unwrap();
                (
                    token.text()[1..token.text().len() - 1].replace(r#"\'"#, "'"),
                    token.text_range(),
                )
            }
        };
        Ok(Key::new(text, range))
    }
}

#[cfg(feature = "serde")]
impl serde::Serialize for Key {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: serde::Serializer,
    {
        self.value.serialize(serializer)
    }
}

#[cfg(test)]
mod test {
    use crate::test_serialize;
    use serde_json::json;

    test_serialize! {
        #[test]
        fn bare_key(r#"key = 1"#) -> Ok(json!({"key": 1}))
    }

    test_serialize! {
        #[test]
        fn basic_string_key(r#""key" = 1"#) -> Ok(json!({"key": 1}))
    }

    test_serialize! {
        #[test]
        fn literal_string_key(r#"'key' = 'value'"#) -> Ok(json!({"key": "value"}))
    }
}
