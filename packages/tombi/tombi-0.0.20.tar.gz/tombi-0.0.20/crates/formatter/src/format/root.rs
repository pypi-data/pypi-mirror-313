use ast::AstNode;

use super::{
    comment::{BeginDanglingComment, DanglingComment, EndDanglingComment},
    Format,
};
use std::fmt::Write;

impl Format for ast::Root {
    fn fmt(&self, f: &mut crate::Formatter) -> Result<(), std::fmt::Error> {
        f.reset();

        let items = self.items().collect::<Vec<_>>();
        if !items.is_empty() {
            self.begin_dangling_comments()
                .map(BeginDanglingComment)
                .collect::<Vec<_>>()
                .fmt(f)?;

            items
                .into_iter()
                .fold(
                    (Header::Root { key_value_size: 0 }, vec![]),
                    |(mut header, mut acc), item| match &item {
                        ast::RootItem::Table(table) => {
                            let header_text = table.header().unwrap().syntax().to_string();
                            let key_value_size = table.key_values().into_iter().count();

                            match header {
                                Header::Root { key_value_size } => {
                                    if key_value_size > 0 {
                                        acc.push(ItemOrNewLine::NewLine);
                                    }
                                }
                                Header::Table {
                                    header_text: pre_header_text,
                                    key_value_size,
                                } => {
                                    if key_value_size > 0
                                        || !header_text.starts_with(&pre_header_text)
                                    {
                                        acc.push(ItemOrNewLine::NewLine);
                                    }
                                }
                                Header::ArrayOfTable { .. } => {
                                    acc.push(ItemOrNewLine::NewLine);
                                }
                            };
                            acc.push(ItemOrNewLine::Item(item));

                            (
                                Header::Table {
                                    header_text,
                                    key_value_size,
                                },
                                acc,
                            )
                        }
                        ast::RootItem::ArrayOfTable(_) => {
                            match header {
                                Header::Root { key_value_size } => {
                                    if key_value_size > 0 {
                                        acc.push(ItemOrNewLine::NewLine);
                                    }
                                }
                                Header::Table { key_value_size, .. } => {
                                    if key_value_size > 0 {
                                        acc.push(ItemOrNewLine::NewLine);
                                    }
                                }
                                Header::ArrayOfTable { .. } => {
                                    acc.push(ItemOrNewLine::NewLine);
                                }
                            };
                            acc.push(ItemOrNewLine::Item(item));

                            (Header::ArrayOfTable {}, acc)
                        }
                        ast::RootItem::KeyValue(_) => {
                            header = if let Header::Root { key_value_size } = header {
                                Header::Root {
                                    key_value_size: key_value_size + 1,
                                }
                            } else {
                                header
                            };
                            acc.push(ItemOrNewLine::Item(item));
                            (header, acc)
                        }
                    },
                )
                .1
                .into_iter()
                .enumerate()
                .try_for_each(|(i, item)| {
                    if i > 0 && matches!(item, ItemOrNewLine::Item(_)) {
                        ItemOrNewLine::NewLine.fmt(f)?;
                    }
                    item.fmt(f)
                })?;

            self.end_dangling_comments()
                .map(EndDanglingComment)
                .collect::<Vec<_>>()
                .fmt(f)?;
        } else {
            self.dangling_comments()
                .map(DanglingComment)
                .collect::<Vec<_>>()
                .fmt(f)?;
        }

        Ok(())
    }
}

impl Format for ast::RootItem {
    fn fmt(&self, f: &mut crate::Formatter) -> Result<(), std::fmt::Error> {
        match self {
            ast::RootItem::Table(it) => it.fmt(f),
            ast::RootItem::ArrayOfTable(it) => it.fmt(f),
            ast::RootItem::KeyValue(it) => it.fmt(f),
        }
    }
}

enum ItemOrNewLine {
    Item(ast::RootItem),
    NewLine,
}

impl Format for ItemOrNewLine {
    fn fmt(&self, f: &mut crate::Formatter) -> Result<(), std::fmt::Error> {
        match self {
            Self::Item(it) => it.fmt(f),
            Self::NewLine => write!(f, "{}", f.line_ending()),
        }
    }
}

#[derive(Debug)]
enum Header {
    Root {
        key_value_size: usize,
    },

    Table {
        header_text: String,
        key_value_size: usize,
    },

    ArrayOfTable {},
}
