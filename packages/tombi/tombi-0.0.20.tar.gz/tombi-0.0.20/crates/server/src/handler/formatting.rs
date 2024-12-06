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
    let mut document_info = match backend.try_get_mut_document_info(uri) {
        TryResult::Present(document_info) => document_info,
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
        &document_info.source,
        backend.toml_version(),
        &backend.format_options(),
    ) {
        Ok(new_text) => {
            if new_text != document_info.source {
                let range = Range::new(
                    text::Position::new(0, 0).into(),
                    text::Position::from_source(
                        &document_info.source,
                        text::Offset::new(document_info.source.len() as u32),
                    )
                    .into(),
                );
                document_info.source = new_text.clone();

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
