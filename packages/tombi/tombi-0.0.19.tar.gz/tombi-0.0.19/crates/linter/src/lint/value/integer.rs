use crate::Lint;

impl Lint for ast::IntegerBin {
    fn lint(&self, _l: &mut crate::Linter) {}
}

impl Lint for ast::IntegerOct {
    fn lint(&self, _l: &mut crate::Linter) {}
}

impl Lint for ast::IntegerDec {
    fn lint(&self, _l: &mut crate::Linter) {}
}

impl Lint for ast::IntegerHex {
    fn lint(&self, _l: &mut crate::Linter) {}
}
