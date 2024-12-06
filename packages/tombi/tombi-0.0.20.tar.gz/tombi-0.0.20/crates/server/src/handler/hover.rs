use crate::{hover::HoverContent, toml};
use ast::{algo::ancestors_at_position, AstNode};
use config::TomlVersion;
use itertools::Itertools;
use parser::SyntaxKind::*;
use tower_lsp::lsp_types::{Hover, HoverParams, Position, TextDocumentPositionParams};

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

    if let Some(hover_content) = get_hover_content(ast, position) {
        Ok(Some(hover_content.into_hover()))
    } else {
        Ok(None)
    }
}

fn get_hover_content(ast: ast::Root, position: Position) -> Option<HoverContent> {
    // NOTE: Eventually, only KeyValue, Table, ArrayOfTable may be shown in the hover.
    //       For now, all nodes are displayed for debugging purposes.

    let mut is_key_value = false;
    for node in ancestors_at_position(ast.syntax(), position.into()) {
        if let Some(key) = ast::Key::cast(node.to_owned()) {
            let keys = key
                .syntax()
                .ancestors()
                .filter_map(|node| match node.kind() {
                    KEYS => ast::Keys::cast(node).map(|keys| {
                        keys.keys()
                            .filter(|k| {
                                k.syntax().text_range().start() <= key.syntax().text_range().start()
                            })
                            .collect::<Vec<_>>()
                    }),
                    KEY_VALUE => {
                        is_key_value = true;
                        None
                    }
                    TABLE => is_key_value
                        .then(|| {
                            ast::Table::cast(node)
                                .map(|table| {
                                    table.header().map(|keys| keys.keys().collect::<Vec<_>>())
                                })
                                .flatten()
                        })
                        .flatten(),
                    ARRAY_OF_TABLE => is_key_value
                        .then(|| {
                            ast::ArrayOfTable::cast(node)
                                .map(|array| {
                                    array.header().map(|keys| keys.keys().collect::<Vec<_>>())
                                })
                                .flatten()
                        })
                        .flatten(),
                    _ => None,
                })
                .collect::<Vec<_>>()
                .into_iter()
                .rev()
                .flatten()
                .map(|key| key.syntax().text().to_string())
                .join(".");

            return Some(HoverContent {
                keys,
                range: key.syntax().text_range(),
                ..Default::default()
            });
        }
    }
    None
}
