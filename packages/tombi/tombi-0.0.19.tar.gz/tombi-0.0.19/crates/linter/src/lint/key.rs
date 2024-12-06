use crate::{rule::KeyEmptyRule, Lint, Rule};

impl Lint for ast::Key {
    fn lint(&self, l: &mut crate::Linter) {
        KeyEmptyRule::check(self, l);
    }
}
