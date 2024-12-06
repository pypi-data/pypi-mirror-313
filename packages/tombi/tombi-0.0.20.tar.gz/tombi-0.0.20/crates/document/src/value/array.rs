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
}

impl Array {
    pub fn new() -> Self {
        Self {
            kind: ArrayKind::Array,
            values: vec![],
        }
    }

    pub fn new_array_of_tables() -> Self {
        Self {
            kind: ArrayKind::ArrayOfTables,
            values: vec![],
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
}

impl TryFrom<ast::Array> for Array {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::Array) -> Result<Self, Self::Error> {
        let mut array = Array::new();
        let mut errors = Vec::new();

        for value in node.values() {
            match value.try_into() {
                Ok(value) => array.push(value),
                Err(errs) => errors.extend(errs),
            }
        }

        Ok(array)
    }
}

#[cfg(feature = "serde")]
impl serde::Serialize for Array {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: serde::Serializer,
    {
        self.values.serialize(serializer)
    }
}
