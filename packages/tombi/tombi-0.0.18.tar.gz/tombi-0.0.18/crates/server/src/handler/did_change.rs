use dashmap::try_result::TryResult;
use tower_lsp::lsp_types::DidChangeTextDocumentParams;

use crate::backend::Backend;

#[tracing::instrument(level = "debug", skip_all)]
pub async fn handle_did_change(
    backend: &Backend,
    DidChangeTextDocumentParams {
        text_document,
        content_changes,
    }: DidChangeTextDocumentParams,
) {
    tracing::info!("handle_did_change");

    let uri = &text_document.uri;
    let mut document = match backend.documents.try_get_mut(uri) {
        TryResult::Present(document) => document,
        TryResult::Absent => {
            tracing::warn!("document not found: {}", uri);
            return;
        }
        TryResult::Locked => {
            tracing::warn!("document is locked: {}", uri);
            return;
        }
    };

    for content_change in content_changes {
        if let Some(range) = content_change.range {
            tracing::warn!("range change is not supported: {:?}", range);
        } else {
            document.source = content_change.text;
        }
    }
}
