use crate::Rule;
use ast::AstNode;

pub struct KeyEmptyRule;

impl Rule<ast::Key> for KeyEmptyRule {
    fn check(node: &ast::Key, l: &mut crate::Linter) {
        if match node {
            ast::Key::BareKey(_) => false,
            ast::Key::BasicString(node) => node.syntax().text() == "\"\"",
            ast::Key::LiteralString(node) => node.syntax().text() == "''",
        } {
            l.add_diagnostic(diagnostic::Diagnostic::new_warning(
                crate::ErrorKind::KeyEmpty.to_string(),
                node.syntax().text_range(),
            ));
        };
    }
}

#[cfg(test)]
mod tests {
    use std::vec;

    #[test]
    fn test_key_empty() {
        let err = crate::lint("'' = 1").unwrap_err();
        assert_eq!(
            err,
            vec![diagnostic::Diagnostic::new_warning(
                crate::ErrorKind::KeyEmpty.to_string(),
                text::Range::new((0, 0).into(), (0, 2).into()),
            )]
        );
    }
}
