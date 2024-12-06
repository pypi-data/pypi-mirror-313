mod array;
mod array_of_table;
mod comma;
mod inline_table;
mod key;
mod key_value;
mod root;
mod table;
mod value;

use crate::{parser::Parser, token_set::TokenSet};
use support::*;
use syntax::{SyntaxKind::*, T};

const TS_LINE_END: TokenSet = TokenSet::new(&[LINE_BREAK, EOF]);
const TS_COMMEMT_OR_LINE_END: TokenSet = TokenSet::new(&[COMMENT, LINE_BREAK, EOF]);
const TS_NEXT_SECTION: TokenSet = TokenSet::new(&[T!['['], T!("[["), EOF]);

pub(crate) trait Parse {
    fn parse(p: &mut Parser<'_>);
}

pub fn invalid_line(p: &mut Parser<'_>, kind: crate::ErrorKind) {
    p.error(crate::Error::new(kind, p.current_range()));
    p.bump_any();
    while !p.at_ts(TS_LINE_END) {
        p.bump_any();
    }
}

mod support {
    use crate::{token_set::TokenSet, SyntaxKind::*};

    const DANGLING_COMMENTS_KINDS: TokenSet = TokenSet::new(&[COMMENT, LINE_BREAK, WHITESPACE]);
    const LEADING_COMMENTS_KINDS: TokenSet = TokenSet::new(&[COMMENT, LINE_BREAK, WHITESPACE]);
    const TAILING_COMMENT_KINDS: TokenSet = TokenSet::new(&[COMMENT, WHITESPACE]);

    pub fn begin_dangling_comments(p: &mut crate::parser::Parser<'_>) {
        let mut n = 0;
        let mut comment_count = 0;
        while p.nth_at_ts(n, DANGLING_COMMENTS_KINDS) {
            let kind = p.nth(n);
            match kind {
                COMMENT => {
                    comment_count += 1;
                }
                LINE_BREAK => {
                    if p.nth_at(n + 1, LINE_BREAK) {
                        if comment_count > 0 {
                            (0..=n).for_each(|_| p.bump_any());
                            while p.eat(LINE_BREAK) || p.eat(WHITESPACE) {}
                            break;
                        }
                        n += 1;
                    }
                }
                _ => {}
            }
            n += 1;
        }
    }

    pub fn end_dangling_comments(p: &mut crate::parser::Parser<'_>) {
        while p.eat_ts(DANGLING_COMMENTS_KINDS) {}
    }

    pub fn peek_leading_comments(p: &mut crate::parser::Parser<'_>) -> usize {
        let mut n = 0;
        while p.nth_at_ts(n, LEADING_COMMENTS_KINDS) {
            n += 1;
        }

        n
    }

    #[inline]
    pub fn leading_comments(p: &mut crate::parser::Parser<'_>) {
        while p.eat_ts(LEADING_COMMENTS_KINDS) {}
    }

    #[inline]
    pub fn tailing_comment(p: &mut crate::parser::Parser<'_>) {
        while p.eat_ts(TAILING_COMMENT_KINDS) {}
    }
}
