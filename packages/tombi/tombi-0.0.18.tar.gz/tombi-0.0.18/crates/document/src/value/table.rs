use indexmap::map::Entry;
use indexmap::IndexMap;

use crate::Key;
use crate::Value;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TableKind {
    Root,
    Table,
    InlineTable,
    ArrayOfTables,
    DottedKeys,
}

#[derive(Debug, Clone, PartialEq)]
pub struct Table {
    kind: TableKind,
    key_values: IndexMap<Key, Value>,
    range: text::Range,
}

impl Table {
    pub(crate) fn new_root(range: text::Range) -> Self {
        Self {
            kind: TableKind::Root,
            key_values: Default::default(),
            range,
        }
    }

    pub fn new(range: text::Range) -> Self {
        Self {
            kind: TableKind::Table,
            key_values: Default::default(),
            range,
        }
    }

    pub fn new_array_of_tables(range: text::Range) -> Self {
        Self {
            kind: TableKind::ArrayOfTables,
            key_values: Default::default(),
            range,
        }
    }

    pub fn new_inline_table(range: text::Range) -> Self {
        Self {
            kind: TableKind::InlineTable,
            key_values: Default::default(),
            range,
        }
    }

    pub fn new_dotted_keys_table(range: text::Range) -> Self {
        Self {
            kind: TableKind::DottedKeys,
            key_values: Default::default(),
            range,
        }
    }

    pub fn key_values(&self) -> &IndexMap<Key, Value> {
        &self.key_values
    }

    pub fn merge(&mut self, other: Self) -> Result<(), Vec<crate::Error>> {
        let mut errors = vec![];
        // Merge the key_values of the two tables recursively
        for (key, value2) in other.key_values {
            match self.key_values.entry(key.clone()) {
                Entry::Occupied(mut entry) => {
                    let value1 = entry.get_mut();
                    match (value1, value2) {
                        (Value::Table(table1), Value::Table(table2)) => {
                            if let Err(errs) = table1.merge(table2) {
                                errors.extend(errs);
                            };
                        }
                        _ => {
                            errors.push(crate::Error::DuplicateKey {
                                key: key.value().to_string(),
                                range: key.range(),
                            });
                        }
                    }
                }
                Entry::Vacant(entry) => {
                    entry.insert(value2);
                }
            }
        }

        if errors.is_empty() {
            Ok(())
        } else {
            Err(errors)
        }
    }

    pub(crate) fn insert(mut self, key: Key, value: Value) -> Result<Self, Vec<crate::Error>> {
        let mut errors = Vec::new();

        match self.key_values.entry(key) {
            Entry::Occupied(mut entry) => {
                let existing_value = entry.get_mut();
                match (existing_value, value) {
                    (Value::Table(table1), Value::Table(table2)) => {
                        if let Err(errs) = table1.merge(table2) {
                            errors.extend(errs);
                        }
                    }
                    _ => {
                        errors.push(crate::Error::DuplicateKey {
                            key: entry.key().value().to_string(),
                            range: entry.key().range(),
                        });
                    }
                }
            }
            Entry::Vacant(entry) => {
                entry.insert(value);
            }
        }

        if errors.is_empty() {
            Ok(self)
        } else {
            Err(errors)
        }
    }

    pub fn entry(&mut self, key: Key) -> Entry<'_, Key, Value> {
        self.key_values.entry(key)
    }

    #[inline]
    pub fn kind(&self) -> TableKind {
        self.kind
    }

    #[inline]
    pub fn range(&self) -> text::Range {
        self.range
    }
}
