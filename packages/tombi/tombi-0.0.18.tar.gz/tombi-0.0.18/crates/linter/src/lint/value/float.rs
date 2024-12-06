use crate::Lint;

impl Lint for ast::Float {
    fn lint(&self, _l: &mut crate::Linter) {}
}
