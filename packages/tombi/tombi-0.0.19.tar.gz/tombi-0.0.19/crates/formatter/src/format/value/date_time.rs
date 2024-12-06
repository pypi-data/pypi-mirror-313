use ast::AstNode;

use crate::format::{
    comment::{LeadingComment, TailingComment},
    Format,
};
use std::fmt::Write;

use super::LiteralNode;

macro_rules! impl_date_time_format {
    (impl Format for $type:ty;) => {
        impl Format for $type {
            fn fmt(&self, f: &mut crate::Formatter) -> Result<(), std::fmt::Error> {
                for comment in self.leading_comments() {
                    LeadingComment(comment).fmt(f)?;
                }

                let token = self.token().unwrap();
                let mut text = token.text().to_string();
                if let Some(delimiter) = f.date_time_delimiter() {
                    text.replace_range(10..11, &delimiter.to_string());
                }

                f.write_indent()?;
                write!(f, "{}", text)?;

                if let Some(comment) = self.tailing_comment() {
                    TailingComment(comment).fmt(f)?;
                }

                Ok(())
            }
        }
    };
}

impl_date_time_format! {
    impl Format for ast::OffsetDateTime;
}

impl_date_time_format! {
    impl Format for ast::LocalDateTime;
}

impl LiteralNode for ast::LocalDate {
    fn token(&self) -> Option<syntax::SyntaxToken> {
        self.token()
    }
}

impl LiteralNode for ast::LocalTime {
    fn token(&self) -> Option<syntax::SyntaxToken> {
        self.token()
    }
}

#[cfg(test)]
mod tests {
    use crate::test_format;

    test_format! {
        #[test]
        fn offset_datetime_key_value1("odt1 = 1979-05-27T07:32:00Z") -> Ok(source);
    }

    test_format! {
        #[test]
        fn offset_datetime_key_value2("odt2 = 1979-05-27T00:32:00-07:00") -> Ok(source);
    }

    test_format! {
        #[test]
        fn offset_datetime_key_value3("odt3 = 1979-05-27T00:32:00.999999-07:00") -> Ok(source);
    }

    test_format! {
        #[test]
        fn offset_datetime_key_value4("odt4 = 1979-05-27 00:32:00.999999-07:00") -> Ok("odt4 = 1979-05-27T00:32:00.999999-07:00");
    }

    test_format! {
        #[test]
        fn local_datetime_key_value1("ldt1 = 1979-05-27T07:32:00") -> Ok(source);
    }

    test_format! {
        #[test]
        fn local_datetime_key_value2("ldt2 = 1979-05-27T00:32:00.999999") -> Ok(source);
    }

    test_format! {
        #[test]
        fn local_datetime_key_value3("ldt3 = 1979-05-27 00:32:00.999999") -> Ok("ldt3 = 1979-05-27T00:32:00.999999");
    }

    test_format! {
        #[test]
        fn valid_local_date_key_value("ld1 = 1979-05-27") -> Ok(source);
    }

    test_format! {
        #[test]
        fn valid_local_time_key_value1("lt1 = 07:32:00") -> Ok(source);
    }

    test_format! {
        #[test]
        fn valid_local_time_key_value2("lt2 = 00:32:00.999999") -> Ok(source);
    }
}
