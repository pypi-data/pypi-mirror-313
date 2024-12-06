#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Boolean {
    value: bool,
    range: text::Range,
}

impl Boolean {
    pub(crate) fn new(text: &str, range: text::Range) -> Self {
        Self {
            value: match text {
                "true" => true,
                "false" => false,
                _ => unreachable!(),
            },
            range,
        }
    }

    #[inline]
    pub fn value(&self) -> bool {
        self.value
    }

    #[inline]
    pub fn range(&self) -> text::Range {
        self.range
    }
}
