use super::{Array, Table};

#[derive(Debug)]
pub enum Value {
    Boolean { range: text::Range },
    Integer { range: text::Range },
    Float { range: text::Range },
    String { range: text::Range },
    OffsetDateTime { range: text::Range },
    LocalDateTime { range: text::Range },
    LocalDate { range: text::Range },
    LocalTime { range: text::Range },
    Array(Array),
    Table(Table),
}

impl Value {
    pub fn range(&self) -> text::Range {
        match self {
            Self::Boolean { range }
            | Self::Integer { range }
            | Self::Float { range }
            | Self::String { range }
            | Self::OffsetDateTime { range }
            | Self::LocalDateTime { range }
            | Self::LocalDate { range }
            | Self::LocalTime { range } => *range,
            Self::Array(array) => array.range(),
            Self::Table(table) => table.range(),
        }
    }
}

impl From<ast::Value> for Value {
    fn from(node: ast::Value) -> Self {
        match node {
            ast::Value::Boolean(value) => Value::Boolean {
                range: value.token().unwrap().text_range(),
            },
            ast::Value::IntegerBin(value) => Value::Integer {
                range: value.token().unwrap().text_range(),
            },
            ast::Value::IntegerOct(value) => Value::Integer {
                range: value.token().unwrap().text_range(),
            },
            ast::Value::IntegerDec(value) => Value::Integer {
                range: value.token().unwrap().text_range(),
            },
            ast::Value::IntegerHex(value) => Value::Integer {
                range: value.token().unwrap().text_range(),
            },
            ast::Value::Float(value) => Value::Float {
                range: value.token().unwrap().text_range(),
            },
            ast::Value::BasicString(value) => Value::String {
                range: value.token().unwrap().text_range(),
            },
            ast::Value::LiteralString(value) => Value::String {
                range: value.token().unwrap().text_range(),
            },
            ast::Value::MultiLineBasicString(value) => Value::String {
                range: value.token().unwrap().text_range(),
            },
            ast::Value::MultiLineLiteralString(value) => Value::String {
                range: value.token().unwrap().text_range(),
            },
            ast::Value::OffsetDateTime(value) => Value::OffsetDateTime {
                range: value.token().unwrap().text_range(),
            },
            ast::Value::LocalDateTime(value) => Value::LocalDateTime {
                range: value.token().unwrap().text_range(),
            },
            ast::Value::LocalDate(value) => Value::LocalDate {
                range: value.token().unwrap().text_range(),
            },
            ast::Value::LocalTime(value) => Value::LocalTime {
                range: value.token().unwrap().text_range(),
            },
            ast::Value::Array(value) => Value::Array(value.into()),
            ast::Value::InlineTable(value) => Value::Table(value.into()),
        }
    }
}
