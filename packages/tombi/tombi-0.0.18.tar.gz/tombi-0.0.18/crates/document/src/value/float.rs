#[derive(Debug, Clone, PartialEq)]
pub struct Float {
    value: f64,
    range: text::Range,
}

impl Float {
    pub fn try_new(text: &str, range: text::Range) -> Result<Self, std::num::ParseFloatError> {
        Ok(Self {
            value: text.parse()?,
            range,
        })
    }

    pub fn value(&self) -> f64 {
        self.value
    }

    pub fn range(&self) -> text::Range {
        self.range
    }
}
