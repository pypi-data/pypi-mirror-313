use tower_lsp::lsp_types::{
    DocumentDiagnosticParams, DocumentDiagnosticReport, DocumentDiagnosticReportResult,
    FullDocumentDiagnosticReport, RelatedFullDocumentDiagnosticReport,
};

use crate::backend::Backend;

#[tracing::instrument(level = "debug", skip_all)]
pub async fn handle_diagnostic(
    backend: &Backend,
    DocumentDiagnosticParams { text_document, .. }: DocumentDiagnosticParams,
) -> Result<DocumentDiagnosticReportResult, tower_lsp::jsonrpc::Error> {
    tracing::info!("handle_diagnostic");

    let diagnostics = match backend.documents.get(&text_document.uri).as_deref() {
        Some(document) => linter::lint_with(
            &document.source,
            backend
                .toml_version
                .unwrap_or(backend.config.toml_version.unwrap_or_default()),
            backend
                .config
                .lint
                .as_ref()
                .unwrap_or_else(|| &config::DEFAULT_LINT_OPTIONS),
        )
        .map_or_else(
            |diagnostics| {
                diagnostics
                    .into_iter()
                    .map(|diagnostic| tower_lsp::lsp_types::Diagnostic {
                        range: diagnostic.range().into(),
                        severity: Some(match diagnostic.level() {
                            diagnostic::Level::WARNING => {
                                tower_lsp::lsp_types::DiagnosticSeverity::WARNING
                            }
                            diagnostic::Level::ERROR => {
                                tower_lsp::lsp_types::DiagnosticSeverity::ERROR
                            }
                        }),
                        message: diagnostic.message().to_string(),
                        ..Default::default()
                    })
                    .collect()
            },
            |_| vec![],
        ),
        None => vec![],
    };

    Ok(DocumentDiagnosticReportResult::Report(
        DocumentDiagnosticReport::Full(RelatedFullDocumentDiagnosticReport {
            full_document_diagnostic_report: FullDocumentDiagnosticReport {
                items: diagnostics,
                ..Default::default()
            },
            ..Default::default()
        }),
    ))
}
