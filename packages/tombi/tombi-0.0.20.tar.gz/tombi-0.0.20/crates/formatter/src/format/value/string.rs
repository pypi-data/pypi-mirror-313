use super::LiteralNode;

impl LiteralNode for ast::BasicString {
    fn token(&self) -> Option<syntax::SyntaxToken> {
        self.token()
    }
}

impl LiteralNode for ast::MultiLineBasicString {
    fn token(&self) -> Option<syntax::SyntaxToken> {
        self.token()
    }
}

impl LiteralNode for ast::LiteralString {
    fn token(&self) -> Option<syntax::SyntaxToken> {
        self.token()
    }
}

impl LiteralNode for ast::MultiLineLiteralString {
    fn token(&self) -> Option<syntax::SyntaxToken> {
        self.token()
    }
}

#[cfg(test)]
mod tests {
    use crate::test_format;

    test_format! {
        #[test]
        fn basic_string_key_value1(r#"key = "value""#) -> Ok(r#"key = "value""#);
    }

    test_format! {
        #[test]
        fn basic_string_key_value2(r#"key    = "value""#) -> Ok(r#"key = "value""#);
    }
}
