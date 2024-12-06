use crate::Format;
use std::fmt::Write;

use super::comment::{LeadingComment, TailingComment};

impl Format for ast::ArrayOfTable {
    fn fmt(&self, f: &mut crate::Formatter) -> Result<(), std::fmt::Error> {
        let header = self.header().unwrap();

        for comment in self.header_leading_comments() {
            LeadingComment(comment).fmt(f)?;
        }

        write!(f, "[[{header}]]")?;

        if let Some(comment) = self.header_tailing_comment() {
            TailingComment(comment).fmt(f)?;
        }

        for key_value in self.key_values() {
            write!(f, "{}", f.line_ending())?;
            key_value.fmt(f)?;
        }

        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use crate::test_format;

    test_format! {
        #[test]
        fn array_of_table_only_header(
            r#"[[package]]"#
        ) -> Ok(source);
    }

    test_format! {
        #[test]
        fn array_of_table_only_header_with_basic_string_key(
            r#"[[dependencies."unicase"]]"#
        ) -> Ok(source);
    }

    test_format! {
        #[test]
        fn array_of_table_only_header_nexted_keys(
            r#"[[dependencies.unicase]]"#
        ) -> Ok(source);
    }

    test_format! {
        #[test]
        fn array_of_table(
            r#"
            [[package]]
            name = "toml-rs"
            version = "0.4.0"
            "#
        ) -> Ok(source);
    }

    test_format! {
        #[test]
        fn array_of_table_with_full_comment1(
            r#"
            # header leading comment1
            # header leading comment2
            [[header]]  # header tailing comment
            # key value leading comment1
            # key value leading comment2
            key = "value"  # key tailing comment
            "#
        ) -> Ok(source);
    }
}
