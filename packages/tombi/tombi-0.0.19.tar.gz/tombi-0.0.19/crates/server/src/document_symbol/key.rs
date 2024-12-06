#[derive(Debug, Clone)]
pub struct Key {
    text: String,
    range: text::Range,
}

impl PartialEq for Key {
    fn eq(&self, other: &Self) -> bool {
        self.text == other.text
    }
}

impl Eq for Key {}

impl std::hash::Hash for Key {
    fn hash<H: std::hash::Hasher>(&self, state: &mut H) {
        self.text.hash(state)
    }
}

impl Key {
    pub fn range(&self) -> text::Range {
        self.range
    }
}

impl From<ast::Key> for Key {
    fn from(node: ast::Key) -> Self {
        Self {
            text: node.to_string(),
            range: node.token().unwrap().text_range(),
        }
    }
}

impl std::fmt::Display for Key {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.text)
    }
}
