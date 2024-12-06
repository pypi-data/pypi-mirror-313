use dashmap::try_result::TryResult;
use tower_lsp::lsp_types::{DocumentFormattingParams, Range, TextEdit};

use crate::backend::Backend;

#[tracing::instrument(level = "debug", skip_all)]
pub async fn handle_formatting(
    backend: &Backend,
    DocumentFormattingParams { text_document, .. }: DocumentFormattingParams,
) -> Result<Option<Vec<TextEdit>>, tower_lsp::jsonrpc::Error> {
    tracing::info!("handle_formatting: {}", text_document.uri);

    let uri = &text_document.uri;
    let mut document = match backend.documents.try_get_mut(uri) {
        TryResult::Present(document) => document,
        TryResult::Absent => {
            tracing::warn!("document not found: {}", uri);
            return Ok(None);
        }
        TryResult::Locked => {
            tracing::warn!("document is locked: {}", uri);
            return Ok(None);
        }
    };

    match formatter::format_with(
        &document.source,
        backend.toml_version.unwrap_or_default(),
        &Default::default(),
    ) {
        Ok(new_text) => {
            if new_text != document.source {
                let range = Range::new(
                    text::Position::new(0, 0).into(),
                    text::Position::from_source(
                        &document.source,
                        text::Offset::new(document.source.len() as u32),
                    )
                    .into(),
                );
                document.source = new_text.clone();

                return Ok(Some(vec![TextEdit { range, new_text }]));
            } else {
                tracing::info!("no change");
            }
        }
        Err(e) => {
            tracing::error!("failed to format: {:?}", e);
        }
    }

    Ok(None)
}
