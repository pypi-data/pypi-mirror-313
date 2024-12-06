use syntax::T;

use crate::parse::{leading_comments, tailing_comment};

use super::{Parse, Parser};

impl Parse for ast::Comma {
    fn parse(p: &mut Parser<'_>) {
        let m = p.start();

        leading_comments(p);

        assert!(p.at(T![,]));

        p.eat(T![,]);
        tailing_comment(p);
        m.complete(p, T!(,));
    }
}
