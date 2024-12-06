use crate::Value;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub enum ArrayKind {
    #[default]
    /// An array of tables.
    ///
    /// ```toml
    /// [[array]]
    /// ```
    ArrayOfTables,

    /// An array.
    ///
    /// ```toml
    /// key = [1, 2, 3]
    /// ```
    Array,
}

#[derive(Debug, Clone, PartialEq, Default)]
pub struct Array {
    kind: ArrayKind,
    values: Vec<Value>,
    range: text::Range,
}

impl Array {
    pub fn new(range: text::Range) -> Self {
        Self {
            kind: ArrayKind::Array,
            values: vec![],
            range,
        }
    }

    pub fn new_array_of_tables(range: text::Range) -> Self {
        Self {
            kind: ArrayKind::ArrayOfTables,
            values: vec![],
            range,
        }
    }

    pub fn push(&mut self, value: Value) {
        self.values.push(value);
    }

    pub fn kind(&self) -> ArrayKind {
        self.kind
    }

    pub fn values(&self) -> &[Value] {
        &self.values
    }

    pub fn range(&self) -> text::Range {
        self.range
    }
}
