use crate::Lint;

impl Lint for ast::Root {
    fn lint(&self, l: &mut crate::Linter) {
        for item in self.items() {
            item.lint(l);
        }
    }
}

impl Lint for ast::RootItem {
    fn lint(&self, l: &mut crate::Linter) {
        match self {
            Self::Table(t) => t.lint(l),
            Self::ArrayOfTable(t) => t.lint(l),
            Self::KeyValue(k) => k.lint(l),
        }
    }
}
