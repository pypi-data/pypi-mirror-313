use syntax::T;

use super::Parse;
use crate::ErrorKind::*;
use crate::{
    parse::{
        invalid_line, leading_comments, peek_leading_comments, tailing_comment, TS_LINE_END,
        TS_NEXT_SECTION,
    },
    parser::Parser,
};
use syntax::SyntaxKind::*;

impl Parse for ast::ArrayOfTable {
    fn parse(p: &mut Parser<'_>) {
        let m = p.start();

        leading_comments(p);

        assert!(p.at(T!("[[")));

        p.eat(T!("[["));

        ast::Keys::parse(p);

        if !p.eat(T!("]]")) {
            invalid_line(p, ExpectedDoubleBracketEnd);
        }

        tailing_comment(p);

        loop {
            let n = peek_leading_comments(p);

            if p.nth_at_ts(n, TS_NEXT_SECTION) {
                break;
            }
            ast::KeyValue::parse(p);

            if !p.at_ts(TS_LINE_END) {
                invalid_line(p, ExpectedLineBreakOrComment);
            }
        }

        m.complete(p, ARRAY_OF_TABLE);
    }
}

#[cfg(test)]
mod test {
    use crate::test_parser;
    use crate::ErrorKind::*;

    test_parser! {
        #[test]
        fn invalid_array_of_table1(
            r#"
            [[]]
            key1 = 1
            key2 = 2
            "#
        ) -> Err([SyntaxError(ExpectedKey, 0:2..0:3)])
    }

    test_parser! {
        #[test]
        fn invalid_array_of_table2(
            r#"
            [[aaa.]]
            key1 = 1
            key2 = 2
            "#
        ) -> Err([SyntaxError(ExpectedKey, 0:6..0:7)])
    }

    test_parser! {
        #[test]
        fn invalid_array_of_table3(
            r#"
            [[aaa.bbb
            key1 = 1
            key2 = 2
            "#
        ) -> Err([SyntaxError(ExpectedDoubleBracketEnd, 0:9..1:0)])
    }

    test_parser! {
        #[test]
        fn invalid_array_of_table4(
            r#"
            [[aaa.bbb]
            key1 = 1
            key2 = 2
            "#
        ) -> Err([SyntaxError(ExpectedDoubleBracketEnd, 0:9..0:10)])
    }

    test_parser! {
        #[test]
        fn invalid_array_of_table5(
            r#"
            [[aaa.bbb]]
            key1 = 1 INVALID COMMENT
            key2 = 2
            "#
        ) -> Err([SyntaxError(ExpectedLineBreakOrComment, 1:9..1:16)])
    }
}
