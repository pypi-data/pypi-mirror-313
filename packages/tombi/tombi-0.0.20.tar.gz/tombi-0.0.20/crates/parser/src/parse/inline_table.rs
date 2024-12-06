use config::TomlVersion;
use syntax::{SyntaxKind::*, T};

use crate::ErrorKind::*;
use crate::{
    parse::{
        begin_dangling_comments, end_dangling_comments, leading_comments, peek_leading_comments,
        tailing_comment, Parse,
    },
    parser::Parser,
};

impl Parse for ast::InlineTable {
    fn parse(p: &mut Parser<'_>) {
        let m = p.start();

        leading_comments(p);

        let begin_range = p.current_range();

        assert!(p.at(T!['{']));

        p.eat(T!['{']);

        begin_dangling_comments(p);

        let mut last_comma_range = None;
        loop {
            let n = peek_leading_comments(p);
            if p.nth_at(n, EOF) || p.nth_at(n, T!['}']) {
                break;
            }

            ast::KeyValue::parse(p);

            let n = peek_leading_comments(p);
            if p.nth_at(n, T![,]) {
                last_comma_range = Some(p.nth_range(n));
                ast::Comma::parse(p);
            } else {
                last_comma_range = None;
                if !p.nth_at(n, T!['}']) {
                    p.error(crate::Error::new(ExpectedComma, p.current_range()));
                    p.bump_any();
                }
            }
        }

        end_dangling_comments(p);

        let end_range = p.current_range();

        if !p.eat(T!['}']) {
            p.error(crate::Error::new(ExpectedBraceEnd, p.current_range()));
        }

        if p.toml_version() == TomlVersion::V1_0_0 {
            if begin_range.start().line() != end_range.start().line() {
                p.error(crate::Error::new(
                    InlineTableMustSingleLine,
                    begin_range + end_range,
                ));
            }
            if let Some(comma_range) = last_comma_range {
                p.error(crate::Error::new(
                    ForbiddenInlineTableLastComma,
                    comma_range,
                ));
            }
        }

        tailing_comment(p);

        m.complete(p, INLINE_TABLE);
    }
}

#[cfg(test)]
mod test {
    use crate::test_parser;
    use crate::ErrorKind::*;
    use config::TomlVersion;

    test_parser! {
        #[test]
        fn empty_inline_table("key = {}") -> Ok(_)
    }

    test_parser! {
        #[test]
        fn inline_table_single_key("key = { key = 1 }") -> Ok(_)
    }

    test_parser! {
        #[test]
        fn inline_table_multi_keys("key = { key = 1, key = 2 }") -> Ok(_)
    }

    test_parser! {
        #[test]
        fn inline_table_multi_keys_with_tailing_comma_v1_0_0("key = { key = 1, key = 2, }", TomlVersion::V1_0_0) -> Err([
            SyntaxError(ForbiddenInlineTableLastComma, 0:24..0:25),
        ])
    }

    test_parser! {
        #[test]
        fn inline_table_multi_keys_with_tailing_comma_v1_1_0("key = { key = 1, key = 2, }", TomlVersion::V1_1_0_Preview) -> Ok(_)
    }

    test_parser! {
        #[test]
        fn inline_table_multi_line_v1_0_0(r#"
            key = {
                key1 = 1,
                key2 = 2,
            }
            "#,
            TomlVersion::V1_0_0
        ) -> Err([
            SyntaxError(InlineTableMustSingleLine, 0:6..3:1),
            SyntaxError(ForbiddenInlineTableLastComma, 2:12..2:13),

        ])
    }

    test_parser! {
        #[test]
        fn inline_table_multi_line_v1_1_0(r#"
            key = {
                key1 = 1,
                key2 = 2,
            }
            "#,
            TomlVersion::V1_1_0_Preview
        ) -> Ok(_)
    }
}
