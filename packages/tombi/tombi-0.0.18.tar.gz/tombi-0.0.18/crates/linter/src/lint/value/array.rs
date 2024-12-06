use crate::Lint;

impl Lint for ast::Array {
    fn lint(&self, _l: &mut crate::Linter) {}
}
