use ast::AstNode;

use crate::Format;
use std::fmt::Write;

use super::comment::LeadingComment;

impl Format for ast::KeyValue {
    fn fmt(&self, f: &mut crate::Formatter) -> Result<(), std::fmt::Error> {
        for comment in self.leading_comments() {
            LeadingComment(comment).fmt(f)?;
        }

        f.write_indent()?;
        self.keys().unwrap().fmt(f)?;

        write!(f, " = ")?;

        f.skip_indent();
        self.value().unwrap().fmt(f)?;

        // NOTE: tailing comment is output by `value.fmt(f)`.

        Ok(())
    }
}

impl Format for ast::Keys {
    fn fmt(&self, f: &mut crate::Formatter) -> Result<(), std::fmt::Error> {
        let keys = self
            .keys()
            .map(|key| key.syntax().text().to_string())
            .collect::<Vec<_>>()
            .join(".");

        write!(f, "{}", keys)
    }
}

impl Format for ast::BareKey {
    fn fmt(&self, f: &mut crate::Formatter) -> Result<(), std::fmt::Error> {
        write!(f, "{}", self.syntax().text())
    }
}

impl Format for ast::Key {
    fn fmt(&self, f: &mut crate::Formatter) -> Result<(), std::fmt::Error> {
        match self {
            Self::BareKey(it) => it.fmt(f),
            Self::BasicString(it) => it.fmt(f),
            Self::LiteralString(it) => it.fmt(f),
        }
    }
}

impl Format for ast::Value {
    fn fmt(&self, f: &mut crate::Formatter) -> Result<(), std::fmt::Error> {
        match self {
            Self::Array(it) => it.fmt(f),
            Self::BasicString(it) => it.fmt(f),
            Self::Boolean(it) => it.fmt(f),
            Self::Float(it) => it.fmt(f),
            Self::InlineTable(it) => it.fmt(f),
            Self::IntegerBin(it) => it.fmt(f),
            Self::IntegerDec(it) => it.fmt(f),
            Self::IntegerHex(it) => it.fmt(f),
            Self::IntegerOct(it) => it.fmt(f),
            Self::LiteralString(it) => it.fmt(f),
            Self::LocalDate(it) => it.fmt(f),
            Self::LocalDateTime(it) => it.fmt(f),
            Self::LocalTime(it) => it.fmt(f),
            Self::MultiLineBasicString(it) => it.fmt(f),
            Self::MultiLineLiteralString(it) => it.fmt(f),
            Self::OffsetDateTime(it) => it.fmt(f),
        }
    }
}

#[cfg(test)]
mod tests {
    use crate::test_format;

    test_format! {
        #[test]
        fn bare_key_value1(r#"key = "value""#) -> Ok("key = \"value\"");
    }
    test_format! {
        #[test]
        fn bare_key_value2(r#"key    = "value""#) -> Ok("key = \"value\"");
    }
    test_format! {
        #[test]
        fn dotted_keys_value1(r#"key1.key2.key3 = "value""#) -> Ok(source);
    }
    test_format! {
        #[test]
        fn dotted_keys_value2(r#"site."google.com" = true"#) -> Ok(source);
    }
    test_format! {
        #[test]
        fn key_value_with_comment(
            r#"
            # leading comment1
            # leading comment2
            key = "value"  # tailing comment
            "#
        ) -> Ok(source);
    }
}
