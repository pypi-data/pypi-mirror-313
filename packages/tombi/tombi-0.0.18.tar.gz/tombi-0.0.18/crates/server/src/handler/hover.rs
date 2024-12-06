use crate::toml;
use ast::{algo::ancestors_at_offset, AstNode};
use config::TomlVersion;
use parser::SyntaxKind;
use text::{Offset, Span};
use tower_lsp::lsp_types::{
    Hover, HoverContents, HoverParams, MarkupContent, MarkupKind, Position, Range,
    TextDocumentPositionParams,
};

#[tracing::instrument(level = "debug", skip_all)]
pub async fn handle_hover(
    HoverParams {
        text_document_position_params:
            TextDocumentPositionParams {
                text_document,
                position,
            },
        ..
    }: HoverParams,
) -> Result<Option<Hover>, tower_lsp::jsonrpc::Error> {
    tracing::info!("handle_hover");

    let source = toml::try_load(&text_document.uri)?;

    let Some(ast) =
        ast::Root::cast(parser::parse(&source, TomlVersion::default()).into_syntax_node())
    else {
        return Ok(None);
    };

    if let Some((value, range)) = get_hover(ast, &source, position) {
        let range = Some(Range::new(
            text::Position::from_source(&source, range.start()).into(),
            text::Position::from_source(&source, range.end()).into(),
        ));

        Ok(Some(Hover {
            contents: HoverContents::Markup(MarkupContent {
                kind: MarkupKind::Markdown,
                value,
            }),
            range,
        }))
    } else {
        Ok(None)
    }
}

fn get_hover(ast: ast::Root, source: &str, position: Position) -> Option<(String, Span)> {
    let offset = Offset::from_source(source, position);

    // NOTE: Eventually, only KeyValue, Table, ArrayOfTable may be shown in the hover.
    //       For now, all nodes are displayed for debugging purposes.

    for node in ancestors_at_offset(ast.syntax(), offset) {
        if let Some(node) = ast::IntegerDec::cast(node.to_owned()) {
            return Some(("IntegerDec".to_owned(), node.syntax().text_span()));
        } else if let Some(node) = ast::IntegerBin::cast(node.to_owned()) {
            return Some(("IntegerBin".to_owned(), node.syntax().text_span()));
        } else if let Some(node) = ast::IntegerOct::cast(node.to_owned()) {
            return Some(("IntegerOct".to_owned(), node.syntax().text_span()));
        } else if let Some(node) = ast::IntegerHex::cast(node.to_owned()) {
            return Some(("IntegerHex".to_owned(), node.syntax().text_span()));
        } else if let Some(node) = ast::BasicString::cast(node.to_owned()) {
            return Some(("BasicString".to_owned(), node.syntax().text_span()));
        } else if let Some(node) = ast::LiteralString::cast(node.to_owned()) {
            return Some(("LiteralString".to_owned(), node.syntax().text_span()));
        } else if let Some(node) = ast::MultiLineBasicString::cast(node.to_owned()) {
            return Some(("MultiLineBasicString".to_owned(), node.syntax().text_span()));
        } else if let Some(node) = ast::MultiLineLiteralString::cast(node.to_owned()) {
            return Some((
                "MultiLineLiteralString".to_owned(),
                node.syntax().text_span(),
            ));
        } else if let Some(node) = ast::Float::cast(node.to_owned()) {
            return Some(("Float".to_owned(), node.syntax().text_span()));
        } else if let Some(node) = ast::Boolean::cast(node.to_owned()) {
            return Some(("Boolean".to_owned(), node.syntax().text_span()));
        } else if let Some(node) = ast::OffsetDateTime::cast(node.to_owned()) {
            return Some(("OffsetDateTime".to_owned(), node.syntax().text_span()));
        } else if let Some(node) = ast::LocalDateTime::cast(node.to_owned()) {
            return Some(("LocalDateTime".to_owned(), node.syntax().text_span()));
        } else if let Some(node) = ast::LocalDate::cast(node.to_owned()) {
            return Some(("LocalDate".to_owned(), node.syntax().text_span()));
        } else if let Some(node) = ast::LocalTime::cast(node.to_owned()) {
            return Some(("LocalTime".to_owned(), node.syntax().text_span()));
        } else if let Some(node) = ast::Array::cast(node.to_owned()) {
            return Some(("Array".to_owned(), node.syntax().text_span()));
        } else if let Some(node) = ast::InlineTable::cast(node.to_owned()) {
            return Some(("InlineTable".to_owned(), node.syntax().text_span()));
        } else if let Some(node) = ast::Keys::cast(node.to_owned()) {
            return Some(("Keys".to_owned(), node.syntax().text_span()));
        } else if let Some(node) = ast::KeyValue::cast(node.to_owned()) {
            return Some(("KeyValue".to_owned(), node.syntax().text_span()));
        } else if let Some(node) = ast::Table::cast(node.to_owned()) {
            return Some(("Table".to_owned(), node.syntax().text_span()));
        } else if let Some(node) = ast::ArrayOfTable::cast(node.to_owned()) {
            return Some(("ArrayOfTable".to_owned(), node.syntax().text_span()));
        } else if node.kind() == SyntaxKind::INVALID_TOKEN {
            return Some(("INVALID_TOKEN".to_owned(), node.text_span()));
        }
    }
    None
}
