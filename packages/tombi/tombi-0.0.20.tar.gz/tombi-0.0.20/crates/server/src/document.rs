#[derive(Debug, Clone)]
pub struct DocumentInfo {
    pub source: String,
}

impl DocumentInfo {
    pub fn new(source: impl Into<String>) -> Self {
        let source = source.into();
        Self { source }
    }
}
