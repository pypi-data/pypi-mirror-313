#[derive(Debug, Clone)]
pub struct Document {
    pub source: String,
}

impl Document {
    pub fn new(source: impl Into<String>) -> Self {
        let source = source.into();
        Self { source }
    }
}
