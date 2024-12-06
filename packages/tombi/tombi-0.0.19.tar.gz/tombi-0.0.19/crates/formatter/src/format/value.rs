mod array;
mod boolean;
mod date_time;
mod float;
mod inline_table;
mod integer;
mod string;

use crate::format::comment::{LeadingComment, TailingComment};
use crate::Format;
use std::fmt::Write;
use syntax::SyntaxToken;

trait LiteralNode {
    fn token(&self) -> Option<SyntaxToken>;
}

impl<T> Format for T
where
    T: LiteralNode + ast::AstNode,
{
    fn fmt(&self, f: &mut crate::Formatter) -> Result<(), std::fmt::Error> {
        for comment in self.leading_comments() {
            LeadingComment(comment).fmt(f)?;
        }

        f.write_indent()?;
        write!(f, "{}", self.token().unwrap())?;

        if let Some(comment) = self.tailing_comment() {
            TailingComment(comment).fmt(f)?;
        }

        Ok(())
    }
}
