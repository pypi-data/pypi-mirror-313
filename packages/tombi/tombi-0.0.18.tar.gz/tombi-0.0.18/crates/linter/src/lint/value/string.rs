use crate::Lint;

impl Lint for ast::BasicString {
    fn lint(&self, _l: &mut crate::Linter) {}
}

impl Lint for ast::LiteralString {
    fn lint(&self, _l: &mut crate::Linter) {}
}

impl Lint for ast::MultiLineBasicString {
    fn lint(&self, _l: &mut crate::Linter) {}
}

impl Lint for ast::MultiLineLiteralString {
    fn lint(&self, _l: &mut crate::Linter) {}
}
