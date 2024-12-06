pub mod algo;
mod generated;

use config::TomlVersion;
pub use generated::*;
use itertools::Itertools;
use std::{fmt::Debug, marker::PhantomData};
use syntax::{SyntaxElement, SyntaxKind::*, T};

pub trait AstNode
where
    Self: Debug,
{
    fn leading_comments(&self) -> impl Iterator<Item = crate::Comment> {
        support::leading_comments(self.syntax().children_with_tokens())
    }

    fn tailing_comment(&self) -> Option<crate::Comment> {
        self.syntax().last_token().and_then(crate::Comment::cast)
    }

    fn can_cast(kind: syntax::SyntaxKind) -> bool
    where
        Self: Sized;

    fn cast(syntax: syntax::SyntaxNode) -> Option<Self>
    where
        Self: Sized;

    fn syntax(&self) -> &syntax::SyntaxNode;
}

/// Like `AstNode`, but wraps tokens rather than interior nodes.
pub trait AstToken {
    fn can_cast(token: syntax::SyntaxKind) -> bool
    where
        Self: Sized;

    fn cast(syntax: syntax::SyntaxToken) -> Option<Self>
    where
        Self: Sized;

    fn syntax(&self) -> &syntax::SyntaxToken;

    fn text(&self) -> &str {
        self.syntax().text()
    }
}

#[allow(dead_code)]
#[derive(Debug, Clone)]
pub struct AstChildren<N> {
    inner: syntax::SyntaxNodeChildren,
    ph: PhantomData<N>,
}

impl<N> AstChildren<N> {
    fn new(parent: &syntax::SyntaxNode) -> Self {
        AstChildren {
            inner: parent.children(),
            ph: PhantomData,
        }
    }
}

impl<N: AstNode> Iterator for AstChildren<N> {
    type Item = N;
    fn next(&mut self) -> Option<N> {
        self.inner.find_map(N::cast)
    }
}

#[derive(Debug, Clone)]
pub enum TableOrArrayOfTable {
    Table(Table),
    ArrayOfTable(ArrayOfTable),
}

impl TableOrArrayOfTable {
    pub fn header(&self) -> Option<Keys> {
        match self {
            TableOrArrayOfTable::Table(table) => table.header(),
            TableOrArrayOfTable::ArrayOfTable(array_of_table) => array_of_table.header(),
        }
    }

    pub fn range(&self) -> text::Range {
        match self {
            TableOrArrayOfTable::Table(table) => table.range(),
            TableOrArrayOfTable::ArrayOfTable(array_of_table) => array_of_table.range(),
        }
    }
}

impl AstNode for TableOrArrayOfTable {
    #[inline]
    fn can_cast(kind: syntax::SyntaxKind) -> bool {
        Table::can_cast(kind) || ArrayOfTable::can_cast(kind)
    }

    #[inline]
    fn cast(syntax: syntax::SyntaxNode) -> Option<Self> {
        if Table::can_cast(syntax.kind()) {
            Table::cast(syntax).map(TableOrArrayOfTable::Table)
        } else if ArrayOfTable::can_cast(syntax.kind()) {
            ArrayOfTable::cast(syntax).map(TableOrArrayOfTable::ArrayOfTable)
        } else {
            None
        }
    }

    #[inline]
    fn syntax(&self) -> &syntax::SyntaxNode {
        match self {
            TableOrArrayOfTable::Table(table) => table.syntax(),
            TableOrArrayOfTable::ArrayOfTable(array_of_table) => array_of_table.syntax(),
        }
    }
}

#[allow(dead_code)]
mod support {
    use syntax::SyntaxKind;

    use super::*;

    #[inline]
    pub(super) fn child<N: AstNode>(parent: &syntax::SyntaxNode) -> Option<N> {
        parent.children().find_map(N::cast)
    }

    #[inline]
    pub(super) fn children<N: AstNode>(parent: &syntax::SyntaxNode) -> AstChildren<N> {
        AstChildren::new(parent)
    }

    #[inline]
    pub(super) fn token(
        parent: &syntax::SyntaxNode,
        kind: syntax::SyntaxKind,
    ) -> Option<syntax::SyntaxToken> {
        parent
            .children_with_tokens()
            .filter_map(|it| it.into_token())
            .find(|it| it.kind() == kind)
    }

    #[inline]
    pub(super) fn leading_comments<I: Iterator<Item = syntax::SyntaxElement>>(
        iter: I,
    ) -> impl Iterator<Item = crate::Comment> {
        iter.take_while(|node| matches!(node.kind(), COMMENT | LINE_BREAK | WHITESPACE))
            .filter_map(|node_or_token| match node_or_token {
                SyntaxElement::Token(token) => crate::Comment::cast(token),
                SyntaxElement::Node(_) => None,
            })
    }

    #[inline]
    pub(super) fn tailing_comment<I: Iterator<Item = syntax::SyntaxElement>>(
        iter: I,
        end: syntax::SyntaxKind,
    ) -> Option<crate::Comment> {
        let mut iter = iter
            .skip_while(|item| item.kind() != end && item.kind() != EOF)
            .skip(1);

        match iter.next()? {
            SyntaxElement::Token(token) if token.kind() == COMMENT => crate::Comment::cast(token),
            SyntaxElement::Token(token) if token.kind() == WHITESPACE => {
                iter.next().and_then(|node_or_token| match node_or_token {
                    SyntaxElement::Token(token) if token.kind() == COMMENT => {
                        crate::Comment::cast(token)
                    }
                    _ => None,
                })
            }
            _ => None,
        }
    }

    #[inline]
    pub(super) fn dangling_comments<I: Iterator<Item = syntax::SyntaxElement>>(
        iter: I,
    ) -> impl Iterator<Item = crate::Comment> {
        iter.filter_map(|node_or_token| match node_or_token {
            SyntaxElement::Token(token) => crate::Comment::cast(token),
            SyntaxElement::Node(_) => None,
        })
    }

    #[inline]
    pub(super) fn begin_dangling_comments<I: Iterator<Item = syntax::SyntaxElement>>(
        iter: I,
    ) -> impl Iterator<Item = crate::Comment> {
        iter.take_while(|node| matches!(node.kind(), COMMENT | WHITESPACE | LINE_BREAK))
            .filter_map(|node_or_token| match node_or_token {
                SyntaxElement::Token(token) => crate::Comment::cast(token),
                SyntaxElement::Node(_) => None,
            })
    }

    #[inline]
    pub(super) fn end_dangling_comments<I: Iterator<Item = syntax::SyntaxElement>>(
        iter: I,
    ) -> impl Iterator<Item = crate::Comment> {
        iter.collect::<Vec<_>>()
            .into_iter()
            .rev()
            .take_while(|node| matches!(node.kind(), COMMENT | WHITESPACE | LINE_BREAK))
            .filter_map(|node_or_token| match node_or_token {
                SyntaxElement::Token(token) => crate::Comment::cast(token),
                SyntaxElement::Node(_) => None,
            })
            .collect::<Vec<_>>()
            .into_iter()
            .rev()
    }

    #[inline]
    pub(super) fn has_inner_comments<I: Iterator<Item = syntax::SyntaxElement>>(
        iter: I,
        start: SyntaxKind,
        end: SyntaxKind,
    ) -> bool {
        iter.skip_while(|node| node.kind() != start)
            .skip(1)
            .take_while(|node| node.kind() != end)
            .any(|node| {
                node.kind() == COMMENT
                    || match node {
                        syntax::SyntaxElement::Node(node) => node
                            .children_with_tokens()
                            .any(|node| node.kind() == COMMENT),
                        _ => false,
                    }
            })
    }

    pub fn leading_table_or_inline_tables<N: AstNode>(
        node: &N,
    ) -> impl Iterator<Item = TableOrArrayOfTable> {
        support::children::<TableOrArrayOfTable>(&node.syntax().parent().unwrap())
            .into_iter()
            .take_while(|n| n.range() < node.syntax().text_range())
            .collect::<Vec<_>>()
            .into_iter()
            .rev()
    }

    pub fn tailing_table_or_inline_tables<'a, N: AstNode>(
        node: &'a N,
    ) -> impl Iterator<Item = TableOrArrayOfTable> + 'a {
        support::children::<TableOrArrayOfTable>(&node.syntax().parent().unwrap())
            .into_iter()
            .skip_while(|n| n.range() <= node.syntax().text_range())
    }
}

impl Root {
    pub fn begin_dangling_comments(&self) -> impl Iterator<Item = crate::Comment> {
        support::begin_dangling_comments(self.syntax().children_with_tokens())
    }

    pub fn end_dangling_comments(&self) -> impl Iterator<Item = crate::Comment> {
        support::end_dangling_comments(self.syntax().children_with_tokens())
    }

    pub fn dangling_comments(&self) -> impl Iterator<Item = crate::Comment> {
        support::dangling_comments(self.syntax().children_with_tokens())
    }
}

impl Table {
    pub fn header_leading_comments(&self) -> impl Iterator<Item = crate::Comment> {
        support::leading_comments(self.syntax().children_with_tokens())
    }

    pub fn header_tailing_comment(&self) -> Option<crate::Comment> {
        support::tailing_comment(self.syntax().children_with_tokens(), T!(']'))
    }

    pub fn leading_table_or_inline_tables(&self) -> impl Iterator<Item = TableOrArrayOfTable> {
        support::leading_table_or_inline_tables(self)
    }

    pub fn tailing_table_or_inline_tables<'a>(
        &'a self,
    ) -> impl Iterator<Item = TableOrArrayOfTable> + 'a {
        support::tailing_table_or_inline_tables(self)
    }
}

impl ArrayOfTable {
    pub fn header_leading_comments(&self) -> impl Iterator<Item = crate::Comment> {
        support::leading_comments(self.syntax().children_with_tokens())
    }

    pub fn header_tailing_comment(&self) -> Option<crate::Comment> {
        support::tailing_comment(self.syntax().children_with_tokens(), T!("]]"))
    }

    pub fn leading_table_or_inline_tables(&self) -> impl Iterator<Item = TableOrArrayOfTable> {
        support::leading_table_or_inline_tables(self)
    }

    pub fn tailing_table_or_inline_tables<'a>(
        &'a self,
    ) -> impl Iterator<Item = TableOrArrayOfTable> + 'a {
        support::tailing_table_or_inline_tables(self)
    }
}

impl Array {
    #[inline]
    pub fn inner_begin_dangling_comments(&self) -> impl Iterator<Item = crate::Comment> {
        support::begin_dangling_comments(
            self.syntax()
                .children_with_tokens()
                .skip_while(|node| node.kind() != T!('['))
                .skip(1),
        )
    }

    #[inline]
    pub fn inner_end_dangling_comments(&self) -> impl Iterator<Item = crate::Comment> {
        support::end_dangling_comments(
            self.syntax()
                .children_with_tokens()
                .take_while(|node| node.kind() != T!(']')),
        )
    }

    #[inline]
    pub fn dangling_comments(&self) -> impl Iterator<Item = crate::Comment> {
        support::dangling_comments(self.syntax().children_with_tokens())
    }

    #[inline]
    pub fn values_with_comma(&self) -> impl Iterator<Item = (crate::Value, Option<crate::Comma>)> {
        self.values()
            .zip_longest(support::children::<crate::Comma>(self.syntax()))
            .map(|value_with_comma| match value_with_comma {
                itertools::EitherOrBoth::Both(value, comma) => (value, Some(comma)),
                itertools::EitherOrBoth::Left(value) => (value, None),
                itertools::EitherOrBoth::Right(_) => unreachable!(),
            })
    }

    pub fn should_be_multiline(&self, toml_version: TomlVersion) -> bool {
        self.has_tailing_comma_after_last_value()
            || self.has_multiline_values(toml_version)
            || self.has_inner_comments()
    }

    pub fn has_tailing_comma_after_last_value(&self) -> bool {
        self.syntax()
            .children_with_tokens()
            .collect::<Vec<_>>()
            .into_iter()
            .rev()
            .skip_while(|item| item.kind() != T!(']'))
            .skip(1)
            .find(|item| !matches!(item.kind(), WHITESPACE | COMMENT | LINE_BREAK))
            .map_or(false, |it| it.kind() == T!(,))
    }

    pub fn has_multiline_values(&self, toml_version: TomlVersion) -> bool {
        self.values().any(|value| match value {
            crate::Value::Array(array) => array.should_be_multiline(toml_version),
            crate::Value::InlineTable(inline_table) => {
                inline_table.should_be_multiline(toml_version)
            }
            crate::Value::MultiLineBasicString(string) => {
                string.token().unwrap().text().contains('\n')
            }
            crate::Value::MultiLineLiteralString(string) => {
                string.token().unwrap().text().contains('\n')
            }
            _ => false,
        })
    }

    pub fn has_inner_comments(&self) -> bool {
        support::has_inner_comments(self.syntax().children_with_tokens(), T!('['), T!(']'))
    }
}

impl InlineTable {
    pub fn inner_begin_dangling_comments(&self) -> impl Iterator<Item = crate::Comment> {
        support::begin_dangling_comments(
            self.syntax()
                .children_with_tokens()
                .skip_while(|node| node.kind() != T!('{'))
                .skip(1),
        )
    }

    pub fn inner_end_dangling_comments(&self) -> impl Iterator<Item = crate::Comment> {
        support::end_dangling_comments(
            self.syntax()
                .children_with_tokens()
                .take_while(|node| node.kind() != T!('}')),
        )
    }

    pub fn key_values_with_comma(
        &self,
    ) -> impl Iterator<Item = (crate::KeyValue, Option<crate::Comma>)> {
        self.key_values()
            .zip_longest(support::children::<crate::Comma>(self.syntax()))
            .map(|value_with_comma| match value_with_comma {
                itertools::EitherOrBoth::Both(value, comma) => (value, Some(comma)),
                itertools::EitherOrBoth::Left(value) => (value, None),
                itertools::EitherOrBoth::Right(_) => unreachable!(),
            })
    }

    pub fn should_be_multiline(&self, toml_version: TomlVersion) -> bool {
        match toml_version {
            TomlVersion::V1_0_0 => false,
            TomlVersion::V1_1_0_Preview => {
                self.has_tailing_comma_after_last_value()
                    || self.has_multiline_values(toml_version)
                    || self.has_inner_comments()
            }
        }
    }

    pub fn has_tailing_comma_after_last_value(&self) -> bool {
        self.syntax()
            .children_with_tokens()
            .collect::<Vec<_>>()
            .into_iter()
            .rev()
            .skip_while(|item| item.kind() != T!('}'))
            .skip(1)
            .find(|item| !matches!(item.kind(), WHITESPACE | COMMENT | LINE_BREAK))
            .map_or(false, |it| it.kind() == T!(,))
    }

    pub fn has_multiline_values(&self, toml_version: TomlVersion) -> bool {
        self.key_values().any(|key_value| {
            key_value.value().map_or(false, |value| match value {
                crate::Value::Array(array) => array.should_be_multiline(toml_version),
                crate::Value::InlineTable(inline_table) => {
                    inline_table.should_be_multiline(toml_version)
                }
                crate::Value::MultiLineBasicString(string) => {
                    string.token().unwrap().text().contains('\n')
                }
                crate::Value::MultiLineLiteralString(string) => {
                    string.token().unwrap().text().contains('\n')
                }
                _ => false,
            })
        })
    }

    pub fn has_inner_comments(&self) -> bool {
        support::has_inner_comments(self.syntax().children_with_tokens(), T!('{'), T!('}'))
    }
}

impl Key {
    pub fn token(&self) -> Option<syntax::SyntaxToken> {
        match self {
            Key::BareKey(key) => key.token(),
            Key::BasicString(key) => key.token(),
            Key::LiteralString(key) => key.token(),
        }
    }
}
