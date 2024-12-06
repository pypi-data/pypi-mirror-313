use super::{Array, Key, Value};
use indexmap::{map::Entry, IndexMap};

#[derive(Debug)]
pub struct Table {
    range: text::Range,
    key_values: IndexMap<Key, Value>,
}

impl Table {
    pub fn new(range: text::Range) -> Self {
        Self {
            range,
            key_values: IndexMap::new(),
        }
    }

    pub fn insert(mut self, key: Key, value: Value) -> Self {
        match self.key_values.entry(key) {
            Entry::Occupied(mut entry1) => {
                let value1 = entry1.get_mut();
                match (value1, value) {
                    (Value::Table(table1), Value::Table(table2)) => table1.merge(table2),
                    _ => {}
                }
            }
            Entry::Vacant(entry1) => {
                entry1.insert(value);
            }
        }

        self
    }

    pub fn merge(&mut self, other: Self) {
        for (key2, value2) in other.key_values {
            match self.key_values.entry(key2) {
                Entry::Occupied(mut entry1) => {
                    let value1 = entry1.get_mut();
                    match (value1, value2) {
                        (Value::Table(table1), Value::Table(table2)) => table1.merge(table2),
                        (Value::Array(array1), Value::Array(array2)) => array1.merge(array2),
                        _ => {}
                    }
                }
                Entry::Vacant(entry1) => {
                    entry1.insert(value2);
                }
            }
        }
    }

    pub fn range(&self) -> text::Range {
        self.range
    }

    pub fn key_values(&self) -> &IndexMap<Key, Value> {
        &self.key_values
    }
}

impl From<ast::Table> for Table {
    fn from(node: ast::Table) -> Self {
        let mut table = Table::new(node.range());

        for key_value in node.key_values() {
            table.merge(key_value.into())
        }

        for key in node
            .header()
            .unwrap()
            .keys()
            .map(Into::into)
            .collect::<Vec<Key>>()
            .into_iter()
            .rev()
        {
            table = Table::new(key.range()).insert(
                key,
                Value::Table(std::mem::replace(&mut table, Table::new(node.range()))),
            );
        }

        table
    }
}

impl From<ast::ArrayOfTable> for Table {
    fn from(node: ast::ArrayOfTable) -> Self {
        let mut table = Table::new(node.range());

        for key_value in node.key_values() {
            table.merge(key_value.into())
        }

        let mut array = Array::new(node.range());
        array.push(Value::Table(table));
        let mut value = Value::Array(array);

        for key in node
            .header()
            .unwrap()
            .keys()
            .map(Into::into)
            .collect::<Vec<Key>>()
            .into_iter()
            .rev()
        {
            value = Value::Table(Table::new(key.range()).insert(key, value));
        }

        if let Value::Table(table) = value {
            table
        } else {
            unreachable!()
        }
    }
}

impl From<ast::KeyValue> for Table {
    fn from(node: ast::KeyValue) -> Self {
        let mut keys = node
            .keys()
            .unwrap()
            .keys()
            .map(Into::into)
            .collect::<Vec<Key>>();

        let value: Value = node.value().unwrap().into();

        let mut table = if let Some(key) = keys.pop() {
            Table::new(key.range() + value.range()).insert(key, value)
        } else {
            Table::new(value.range())
        };

        for key in keys.into_iter().rev() {
            table = Table::new(key.range() + table.range()).insert(
                key,
                Value::Table(std::mem::replace(&mut table, Table::new(node.range()))),
            );
        }

        table
    }
}

impl From<ast::InlineTable> for Table {
    fn from(node: ast::InlineTable) -> Self {
        let mut table = Table::new(
            node.brace_start().unwrap().text_range() + node.brace_end().unwrap().text_range(),
        );

        for key_value in node.key_values() {
            table.merge(key_value.into())
        }

        table
    }
}
