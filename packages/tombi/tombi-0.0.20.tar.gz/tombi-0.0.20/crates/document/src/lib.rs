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
    fn new() -> Self {
        Self(Table::new_root())
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

#[cfg(feature = "serde")]
impl serde::Serialize for Document {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: serde::Serializer,
    {
        self.0.serialize(serializer)
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
        let mut document = Document::new();
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

#[cfg(test)]
#[macro_export]
macro_rules! test_serialize {
    {#[test] fn $name:ident($source:expr) -> Ok($json:expr)} => {
        #[cfg(feature = "serde")]
        #[test]
        fn $name() {
            use ast::AstNode;

            let p = parser::parse($source, config::TomlVersion::V1_0_0);
            let ast = ast::Root::cast(p.into_syntax_node()).unwrap();
            let document = crate::Document::try_from(ast).unwrap();
            let serialized = serde_json::to_string(&document).unwrap();
            assert_eq!(serialized, $json.to_string());
        }
    };
}

#[cfg(test)]
mod test {
    use serde_json::json;

    test_serialize! {
        #[test]
        fn empty("") -> Ok(json!({}))
    }

    test_serialize! {
        #[test]
        fn key_values(
            r#"
            key = "value"
            flag = true
            "#
        ) -> Ok(json!({"key": "value", "flag": true}))
    }
}
