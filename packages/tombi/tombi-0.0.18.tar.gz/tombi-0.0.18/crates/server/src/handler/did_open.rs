use tower_lsp::lsp_types::DidOpenTextDocumentParams;

use crate::backend::Backend;
use crate::document::Document;

#[tracing::instrument(level = "debug", skip_all)]
pub async fn handle_did_open(backend: &Backend, params: DidOpenTextDocumentParams) {
    tracing::info!("handle_did_open");

    let uri = params.text_document.uri.clone();
    let source = params.text_document.text;

    backend.documents.insert(uri, Document::new(source));
}
