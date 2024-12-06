use super::Value;

#[derive(Debug)]
pub struct Array {
    range: text::Range,
    values: Vec<Value>,
}

impl Array {
    pub(crate) fn new(range: text::Range) -> Self {
        Self {
            range,
            values: Vec::new(),
        }
    }

    pub(crate) fn push(&mut self, value: Value) {
        self.values.push(value);
    }

    pub fn merge(&mut self, other: Self) {
        self.values.extend(other.values);
    }

    pub fn range(&self) -> text::Range {
        self.range
    }

    pub fn values(&self) -> &[Value] {
        &self.values
    }
}

impl From<ast::Array> for Array {
    fn from(node: ast::Array) -> Self {
        Self {
            range: node.bracket_start().unwrap().text_range()
                + node.bracket_end().unwrap().text_range(),
            values: node.values().map(Into::into).collect(),
        }
    }
}
