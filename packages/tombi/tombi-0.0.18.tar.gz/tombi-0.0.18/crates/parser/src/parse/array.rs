use syntax::T;

use crate::ErrorKind::*;
use crate::{
    parse::{
        begin_dangling_comments, end_dangling_comments, leading_comments, peek_leading_comments,
        tailing_comment, Parse,
    },
    parser::Parser,
};
use syntax::SyntaxKind::*;

impl Parse for ast::Array {
    fn parse(p: &mut Parser<'_>) {
        let m = p.start();

        leading_comments(p);

        assert!(p.at(T!['[']));

        p.eat(T!['[']);

        begin_dangling_comments(p);

        loop {
            let n = peek_leading_comments(p);
            if p.nth_at(n, EOF) || p.nth_at(n, T![']']) {
                break;
            }

            ast::Value::parse(p);

            let n = peek_leading_comments(p);
            if p.nth_at(n, T![,]) {
                ast::Comma::parse(p);
            } else if !p.nth_at(n, T![']']) {
                p.error(crate::Error::new(ExpectedComma, p.current_range()));
                p.bump_any();
            }
        }

        end_dangling_comments(p);

        if !p.eat(T![']']) {
            p.error(crate::Error::new(ExpectedBracketEnd, p.current_range()));
        }

        tailing_comment(p);

        m.complete(p, ARRAY);
    }
}
