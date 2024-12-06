mod error;
mod key;
mod value;

use std::ops::Deref;

pub use error::Error;
pub use key::Key;
pub use value::{
    Array, ArrayKind, Boolean, Float, Integer, IntegerKind, LocalDate, LocalDateTime, LocalTime,
    OffsetDateTime, String, Table, TableKind, Value,
};

#[derive(Debug, Clone, PartialEq)]
pub struct Document(Table);

impl Document {
    fn new(range: text::Range) -> Self {
        Self(Table::new_root(range))
    }

    #[cfg(feature = "load")]
    pub fn load(
        source: &str,
        toml_version: config::TomlVersion,
    ) -> Result<Self, Vec<crate::Error>> {
        use ast::AstNode;

        let p = parser::parse(source, toml_version);
        if !p.errors().is_empty() {
            return Err(p
                .errors()
                .into_iter()
                .map(|e| crate::Error::Syntax(e))
                .collect());
        }

        let root = ast::Root::cast(p.into_syntax_node()).unwrap();
        Self::try_from(root)
    }
}

impl From<Document> for Table {
    fn from(document: Document) -> Self {
        document.0
    }
}

impl Deref for Document {
    type Target = Table;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

enum RootItem {
    Table(Table),
    ArrayOfTable(Table),
    KeyValue(Table),
}

impl TryFrom<ast::Root> for Document {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::Root) -> Result<Self, Self::Error> {
        let mut document = Document::new(node.range());
        let mut errors = Vec::new();

        for item in node.items() {
            if let Err(err) = match item.try_into() {
                Ok(RootItem::Table(table)) => document.0.merge(table),
                Ok(RootItem::ArrayOfTable(table)) => document.0.merge(table),
                Ok(RootItem::KeyValue(table)) => document.0.merge(table),
                Err(errs) => Err(errs),
            } {
                errors.extend(err);
            }
        }
        Ok(document)
    }
}

impl TryFrom<ast::RootItem> for RootItem {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::RootItem) -> Result<Self, Self::Error> {
        match node {
            ast::RootItem::Table(table) => table.try_into().map(Self::Table),
            ast::RootItem::ArrayOfTable(array) => array.try_into().map(Self::ArrayOfTable),
            ast::RootItem::KeyValue(key_value) => key_value.try_into().map(Self::KeyValue),
        }
    }
}

impl TryFrom<ast::Table> for Table {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::Table) -> Result<Self, Self::Error> {
        let mut table = Table::new(node.range());
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
                match Table::new(node.range()).insert(
                    k,
                    Value::Table(std::mem::replace(&mut table, Table::new(node.range()))),
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

impl TryFrom<ast::ArrayOfTable> for Table {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::ArrayOfTable) -> Result<Self, Self::Error> {
        let mut table = Table::new_array_of_tables(node.range());
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
                match Table::new_array_of_tables(node.range()).insert(
                    k,
                    Value::Table(std::mem::replace(
                        &mut table,
                        Table::new_array_of_tables(node.range()),
                    )),
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
            match Table::new(key.range() + value.range()).insert(key, value) {
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
            match Table::new_dotted_keys_table(key.range() + table.range()).insert(
                key,
                Value::Table(std::mem::replace(
                    &mut table,
                    Table::new_dotted_keys_table(node.range()),
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

impl TryFrom<ast::Key> for Key {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::Key) -> Result<Self, Self::Error> {
        let token = match node {
            ast::Key::BareKey(bare_key) => bare_key.token().unwrap(),
            ast::Key::BasicString(basic_string) => basic_string.token().unwrap(),
            ast::Key::LiteralString(literal_string) => literal_string.token().unwrap(),
        };
        Ok(Key::new(token.text(), token.text_range()))
    }
}

impl TryFrom<ast::Value> for Value {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::Value) -> Result<Self, Self::Error> {
        match node {
            ast::Value::BasicString(string) => string.try_into().map(Value::String),
            ast::Value::LiteralString(string) => string.try_into().map(Value::String),
            ast::Value::MultiLineBasicString(string) => string.try_into().map(Value::String),
            ast::Value::MultiLineLiteralString(string) => string.try_into().map(Value::String),
            ast::Value::IntegerBin(integer) => integer.try_into().map(Value::Integer),
            ast::Value::IntegerOct(integer) => integer.try_into().map(Value::Integer),
            ast::Value::IntegerDec(integer) => integer.try_into().map(Value::Integer),
            ast::Value::IntegerHex(integer) => integer.try_into().map(Value::Integer),
            ast::Value::Float(float) => float.try_into().map(Value::Float),
            ast::Value::Boolean(boolean) => boolean.try_into().map(Value::Boolean),
            ast::Value::OffsetDateTime(dt) => dt.try_into().map(Value::OffsetDateTime),
            ast::Value::LocalDateTime(dt) => dt.try_into().map(Value::LocalDateTime),
            ast::Value::LocalDate(date) => date.try_into().map(Value::LocalDate),
            ast::Value::LocalTime(time) => time.try_into().map(Value::LocalTime),
            ast::Value::Array(array) => array.try_into().map(Value::Array),
            ast::Value::InlineTable(inline_table) => inline_table.try_into().map(Value::Table),
        }
    }
}

impl TryFrom<ast::Boolean> for Boolean {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::Boolean) -> Result<Self, Self::Error> {
        let token = node.token().unwrap();
        Ok(Self::new(token.text(), token.text_range()))
    }
}

impl TryFrom<ast::IntegerBin> for Integer {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::IntegerBin) -> Result<Self, Self::Error> {
        let token = node.token().unwrap();
        Self::try_new_integer_bin(token.text(), token.text_range()).map_err(|err| {
            vec![crate::Error::ParseIntError {
                error: err,
                range: token.text_range(),
            }]
        })
    }
}

impl TryFrom<ast::IntegerOct> for Integer {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::IntegerOct) -> Result<Self, Self::Error> {
        let token = node.token().unwrap();
        Self::try_new_integer_oct(token.text(), token.text_range()).map_err(|err| {
            vec![crate::Error::ParseIntError {
                error: err,
                range: token.text_range(),
            }]
        })
    }
}

impl TryFrom<ast::IntegerDec> for Integer {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::IntegerDec) -> Result<Self, Self::Error> {
        let token = node.token().unwrap();
        Self::try_new_integer_dec(token.text(), token.text_range()).map_err(|err| {
            vec![crate::Error::ParseIntError {
                error: err,
                range: token.text_range(),
            }]
        })
    }
}

impl TryFrom<ast::IntegerHex> for Integer {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::IntegerHex) -> Result<Self, Self::Error> {
        let token = node.token().unwrap();
        Self::try_new_integer_hex(token.text(), token.text_range()).map_err(|err| {
            vec![crate::Error::ParseIntError {
                error: err,
                range: token.text_range(),
            }]
        })
    }
}

impl TryFrom<ast::Float> for Float {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::Float) -> Result<Self, Self::Error> {
        let token = node.token().unwrap();
        Self::try_new(token.text(), token.text_range()).map_err(|err| {
            vec![crate::Error::ParseFloatError {
                error: err,
                range: token.text_range(),
            }]
        })
    }
}

impl TryFrom<ast::BasicString> for String {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::BasicString) -> Result<Self, Self::Error> {
        let token = node.token().unwrap();
        Ok(Self::new_basic_string(token.text(), token.text_range()))
    }
}

impl TryFrom<ast::LiteralString> for String {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::LiteralString) -> Result<Self, Self::Error> {
        let token = node.token().unwrap();
        Ok(Self::new_literal_string(token.text(), token.text_range()))
    }
}

impl TryFrom<ast::MultiLineBasicString> for String {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::MultiLineBasicString) -> Result<Self, Self::Error> {
        let token = node.token().unwrap();
        Ok(Self::new_multi_line_basic_string(
            token.text(),
            token.text_range(),
        ))
    }
}

impl TryFrom<ast::MultiLineLiteralString> for String {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::MultiLineLiteralString) -> Result<Self, Self::Error> {
        let token = node.token().unwrap();
        Ok(Self::new_multi_line_literal_string(
            token.text(),
            token.text_range(),
        ))
    }
}

impl TryFrom<ast::OffsetDateTime> for OffsetDateTime {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::OffsetDateTime) -> Result<Self, Self::Error> {
        let token = node.token().unwrap();
        Self::try_new(token.text(), token.text_range()).map_err(|err| {
            vec![crate::Error::ParseOffsetDateTimeError {
                error: err,
                range: token.text_range(),
            }]
        })
    }
}

impl TryFrom<ast::LocalDateTime> for LocalDateTime {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::LocalDateTime) -> Result<Self, Self::Error> {
        let token = node.token().unwrap();
        Self::try_new(token.text(), token.text_range()).map_err(|err| {
            vec![crate::Error::ParseLocalDateTimeError {
                error: err,
                range: token.text_range(),
            }]
        })
    }
}

impl TryFrom<ast::LocalDate> for LocalDate {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::LocalDate) -> Result<Self, Self::Error> {
        let token = node.token().unwrap();
        Self::try_new(token.text(), token.text_range()).map_err(|err| {
            vec![crate::Error::ParseLocalDateError {
                error: err,
                range: token.text_range(),
            }]
        })
    }
}

impl TryFrom<ast::LocalTime> for LocalTime {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::LocalTime) -> Result<Self, Self::Error> {
        let token = node.token().unwrap();
        Self::try_new(token.text()).map_err(|err| {
            vec![crate::Error::ParseLocalTimeError {
                error: err,
                range: token.text_range(),
            }]
        })
    }
}

impl TryFrom<ast::Array> for Array {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::Array) -> Result<Self, Self::Error> {
        let mut array = Array::new(node.range());
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

impl TryFrom<ast::InlineTable> for Table {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::InlineTable) -> Result<Self, Self::Error> {
        let mut table = Table::new_inline_table(node.range());
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
