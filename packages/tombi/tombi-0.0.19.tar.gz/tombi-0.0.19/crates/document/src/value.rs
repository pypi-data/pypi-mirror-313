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

impl Value {
    #[inline]
    pub fn range(&self) -> text::Range {
        match self {
            Self::Boolean(value) => value.range(),
            Self::Integer(value) => value.range(),
            Self::Float(value) => value.range(),
            Self::String(value) => value.range(),
            Self::OffsetDateTime(value) => value.range(),
            Self::LocalDateTime(value) => value.range(),
            Self::LocalDate(value) => value.range(),
            Self::LocalTime(value) => value.range(),
            Self::Array(value) => value.range(),
            Self::Table(value) => value.range(),
        }
    }
}
