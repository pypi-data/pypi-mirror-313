mod array;
mod key;
mod table;
mod value;

use std::ops::Deref;

pub use array::Array;
pub use key::Key;
pub use table::Table;
pub use value::Value;

#[derive(Debug)]
pub struct Document(Table);

impl Deref for Document {
    type Target = Table;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl From<ast::Root> for Document {
    fn from(node: ast::Root) -> Self {
        let mut table = Table::new(node.range());

        for item in node.items() {
            match item.try_into() {
                Ok(RootItem::Table(tbl)) => table.merge(tbl),
                Ok(RootItem::ArrayOfTable(tbl)) => table.merge(tbl),
                Ok(RootItem::KeyValue(tbl)) => table.merge(tbl),
                Err(_) => {}
            }
        }
        Document(table)
    }
}

#[derive(Debug)]
enum RootItem {
    Table(Table),
    ArrayOfTable(Table),
    KeyValue(Table),
}

impl From<ast::RootItem> for RootItem {
    fn from(node: ast::RootItem) -> Self {
        match node {
            ast::RootItem::Table(tbl) => RootItem::Table(tbl.into()),
            ast::RootItem::ArrayOfTable(tbl) => RootItem::ArrayOfTable(tbl.into()),
            ast::RootItem::KeyValue(kv) => RootItem::KeyValue(kv.into()),
        }
    }
}
