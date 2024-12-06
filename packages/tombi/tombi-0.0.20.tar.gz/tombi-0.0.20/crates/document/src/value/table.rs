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
}

impl Table {
    pub(crate) fn new_root() -> Self {
        Self {
            kind: TableKind::Root,
            key_values: Default::default(),
        }
    }

    pub fn new() -> Self {
        Self {
            kind: TableKind::Table,
            key_values: Default::default(),
        }
    }

    pub fn new_array_of_tables() -> Self {
        Self {
            kind: TableKind::ArrayOfTables,
            key_values: Default::default(),
        }
    }

    pub fn new_inline_table() -> Self {
        Self {
            kind: TableKind::InlineTable,
            key_values: Default::default(),
        }
    }

    pub fn new_dotted_keys_table() -> Self {
        Self {
            kind: TableKind::DottedKeys,
            key_values: Default::default(),
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
}

impl TryFrom<ast::Table> for Table {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::Table) -> Result<Self, Self::Error> {
        let mut table = Table::new();
        let mut errors = Vec::new();

        for key_value in node.key_values() {
            match key_value.try_into() {
                Ok(other) => {
                    if let Err(errs) = table.merge(other) {
                        errors.extend(errs)
                    }
                }
                Err(errs) => errors.extend(errs),
            }
        }

        for key in node
            .header()
            .unwrap()
            .keys()
            .collect::<Vec<_>>()
            .into_iter()
            .rev()
        {
            if let Ok(k) = key.try_into() {
                match Table::new()
                    .insert(k, Value::Table(std::mem::replace(&mut table, Table::new())))
                {
                    Ok(t) => table = t,
                    Err(errs) => {
                        errors.extend(errs);
                    }
                }
            }
        }

        if errors.is_empty() {
            Ok(table)
        } else {
            Err(errors)
        }
    }
}

impl TryFrom<ast::ArrayOfTable> for Table {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::ArrayOfTable) -> Result<Self, Self::Error> {
        let mut table = Table::new_array_of_tables();
        let mut errors = Vec::new();

        for key_value in node.key_values() {
            match key_value.try_into() {
                Ok(other) => {
                    if let Err(errs) = table.merge(other) {
                        errors.extend(errs)
                    }
                }
                Err(errs) => errors.extend(errs),
            }
        }

        for key in node
            .header()
            .unwrap()
            .keys()
            .collect::<Vec<_>>()
            .into_iter()
            .rev()
        {
            if let Ok(k) = key.try_into() {
                match Table::new_array_of_tables().insert(
                    k,
                    Value::Table(std::mem::replace(&mut table, Table::new_array_of_tables())),
                ) {
                    Ok(t) => table = t,
                    Err(errs) => {
                        errors.extend(errs);
                    }
                }
            }
        }

        if errors.is_empty() {
            Ok(table)
        } else {
            Err(errors)
        }
    }
}

impl TryFrom<ast::KeyValue> for Table {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::KeyValue) -> Result<Table, Self::Error> {
        let mut errors = Vec::new();
        let mut keys = node
            .keys()
            .unwrap()
            .keys()
            .map(TryInto::<Key>::try_into)
            .fold(Vec::new(), |mut acc, res| {
                match res {
                    Ok(key) => acc.push(key),
                    Err(err) => errors.extend(err),
                }
                acc
            });

        let value: Value = match node.value().unwrap().try_into() {
            Ok(value) => value,
            Err(errs) => {
                errors.extend(errs);
                return Err(errors);
            }
        };

        let mut table = if let Some(key) = keys.pop() {
            match Table::new().insert(key, value) {
                Ok(table) => table,
                Err(errs) => {
                    errors.extend(errs);
                    return Err(errors);
                }
            }
        } else {
            return Err(errors);
        };

        for key in keys.into_iter().rev() {
            match Table::new_dotted_keys_table().insert(
                key,
                Value::Table(std::mem::replace(
                    &mut table,
                    Table::new_dotted_keys_table(),
                )),
            ) {
                Ok(t) => table = t,
                Err(errs) => {
                    errors.extend(errs);
                }
            }
        }

        if errors.is_empty() {
            Ok(table)
        } else {
            Err(errors)
        }
    }
}

impl TryFrom<ast::InlineTable> for Table {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::InlineTable) -> Result<Self, Self::Error> {
        let mut table = Table::new_inline_table();
        let mut errors = Vec::new();

        for key_value in node.key_values() {
            match key_value.try_into() {
                Ok(other) => {
                    if let Err(errs) = table.merge(other) {
                        errors.extend(errs)
                    }
                }
                Err(errs) => errors.extend(errs),
            }
        }

        if errors.is_empty() {
            Ok(table)
        } else {
            Err(errors)
        }
    }
}

#[cfg(feature = "serde")]
impl serde::Serialize for Table {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: serde::Serializer,
    {
        self.key_values.serialize(serializer)
    }
}
