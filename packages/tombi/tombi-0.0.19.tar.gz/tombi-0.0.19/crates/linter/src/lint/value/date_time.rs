use crate::Lint;

impl Lint for ast::OffsetDateTime {
    fn lint(&self, _l: &mut crate::Linter) {}
}

impl Lint for ast::LocalDateTime {
    fn lint(&self, _l: &mut crate::Linter) {}
}

impl Lint for ast::LocalDate {
    fn lint(&self, _l: &mut crate::Linter) {}
}

impl Lint for ast::LocalTime {
    fn lint(&self, _l: &mut crate::Linter) {}
}
