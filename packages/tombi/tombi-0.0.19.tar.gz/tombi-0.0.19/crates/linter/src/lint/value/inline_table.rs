use crate::Lint;

impl Lint for ast::InlineTable {
    fn lint(&self, _l: &mut crate::Linter) {}
}
