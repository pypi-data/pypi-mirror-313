use syntax::{
    SyntaxKind::{self, *},
    T,
};

use crate::{parser::Parser, token_set::TokenSet};

use super::Parse;
use crate::ErrorKind::*;

pub(crate) const KEY_FIRST: TokenSet = TokenSet::new(&[
    // name = "Tom"
    SyntaxKind::BARE_KEY,
    // "127.0.0.1" = "value"
    SyntaxKind::BASIC_STRING,
    // 'key2' = "value"
    SyntaxKind::LITERAL_STRING,
    // 1234 = "value"
    SyntaxKind::INTEGER_DEC,
    // 3.14159 = "pi"
    SyntaxKind::FLOAT,
    // true = "value"
    SyntaxKind::BOOLEAN,
]);

impl Parse for ast::Keys {
    fn parse(p: &mut Parser<'_>) {
        let m = p.start();
        if eat_keys(p).is_some() {
            m.complete(p, KEYS);
        } else {
            m.complete(p, INVALID_TOKEN);
        };
    }
}

fn eat_keys(p: &mut Parser<'_>) -> Option<SyntaxKind> {
    if p.nth_at(1, T![.]) {
        // Dotted keys Mode
        loop {
            let m = p.start();
            if let Some(kind) = eat_key(p) {
                m.complete(p, kind);
            } else {
                p.error(crate::Error::new(ExpectedKey, p.current_range()));
                m.complete(p, INVALID_TOKEN);
                return None;
            }
            if !p.eat(T![.]) {
                break;
            }
        }
        Some(DOTTED_KEYS)
    } else {
        let m = p.start();
        if let Some(kind) = eat_key(p) {
            m.complete(p, kind);
            Some(kind)
        } else {
            p.error(crate::Error::new(ExpectedKey, p.current_range()));
            m.complete(p, INVALID_TOKEN);
            None
        }
    }
}

pub fn eat_key(p: &mut Parser<'_>) -> Option<SyntaxKind> {
    let kind = p.current();
    match kind {
        BARE_KEY | BASIC_STRING | LITERAL_STRING => {
            p.bump_any();
            Some(kind)
        }
        INTEGER_DEC => {
            p.bump_remap(BARE_KEY);
            Some(BARE_KEY)
        }
        FLOAT => {
            p.bump_remap(BARE_KEY);
            Some(DOTTED_KEYS)
        }
        BOOLEAN => {
            p.bump_remap(BARE_KEY);
            Some(BARE_KEY)
        }
        _ => None,
    }
}
