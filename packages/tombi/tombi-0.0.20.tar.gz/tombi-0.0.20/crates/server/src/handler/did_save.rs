use tower_lsp::lsp_types::DidSaveTextDocumentParams;

use crate::backend::Backend;

#[tracing::instrument(level = "debug", skip_all)]
pub async fn handle_did_save(
    backend: &Backend,
    DidSaveTextDocumentParams {
        text_document,
        text,
    }: DidSaveTextDocumentParams,
) {
    tracing::info!("handle_did_save");

    if let Some(text) = text {
        if let Some(mut document_info) = backend.get_mut_document_info(&text_document.uri) {
            document_info.source = text;
        }
    }
}
