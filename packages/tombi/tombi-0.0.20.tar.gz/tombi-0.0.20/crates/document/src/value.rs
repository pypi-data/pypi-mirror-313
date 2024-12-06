mod array;
mod boolean;
mod date_time;
mod float;
mod integer;
mod string;
mod table;

pub use array::{Array, ArrayKind};
pub use boolean::Boolean;
pub use date_time::{LocalDate, LocalDateTime, LocalTime, OffsetDateTime};
pub use float::Float;
pub use integer::{Integer, IntegerKind};
pub use string::String;
pub use table::{Table, TableKind};

#[derive(Debug, Clone, PartialEq)]
pub enum Value {
    Boolean(Boolean),
    Integer(Integer),
    Float(Float),
    String(String),
    OffsetDateTime(OffsetDateTime),
    LocalDateTime(LocalDateTime),
    LocalDate(LocalDate),
    LocalTime(LocalTime),
    Array(Array),
    Table(Table),
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

#[cfg(feature = "serde")]
impl serde::Serialize for Value {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: serde::Serializer,
    {
        match self {
            Value::Boolean(value) => value.serialize(serializer),
            Value::Integer(value) => value.serialize(serializer),
            Value::Float(value) => value.serialize(serializer),
            Value::String(value) => value.serialize(serializer),
            Value::OffsetDateTime(value) => value.serialize(serializer),
            Value::LocalDateTime(value) => value.serialize(serializer),
            Value::LocalDate(value) => value.serialize(serializer),
            Value::LocalTime(value) => value.serialize(serializer),
            Value::Array(value) => value.serialize(serializer),
            Value::Table(value) => value.serialize(serializer),
        }
    }
}
