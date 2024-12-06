use crate::Lint;

impl Lint for ast::Boolean {
    fn lint(&self, _l: &mut crate::Linter) {}
}
