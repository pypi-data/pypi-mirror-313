use super::handler::{
    handle_diagnostic, handle_did_change, handle_did_change_configuration, handle_did_open,
    handle_did_save, handle_document_symbol, handle_formatting, handle_hover, handle_initialize,
    handle_semantic_tokens_full, handle_shutdown,
};
use crate::{document::DocumentInfo, handler::handle_folding_range};
use ast::AstNode;
use config::{Config, TomlVersion};
use dashmap::{
    mapref::one::{Ref, RefMut},
    try_result::TryResult,
    DashMap,
};
use tower_lsp::{
    lsp_types::{
        DidChangeConfigurationParams, DidChangeTextDocumentParams, DidOpenTextDocumentParams,
        DidSaveTextDocumentParams, DocumentDiagnosticParams, DocumentDiagnosticReportResult,
        DocumentSymbolParams, DocumentSymbolResponse, FoldingRange, FoldingRangeParams, Hover,
        HoverParams, InitializeParams, InitializeResult, SemanticTokensParams,
        SemanticTokensResult, Url,
    },
    LanguageServer,
};

#[derive(Debug)]
pub struct Backend {
    #[allow(dead_code)]
    client: tower_lsp::Client,
    document_infos: DashMap<Url, DocumentInfo>,
    toml_version: Option<TomlVersion>,
    config: Config,
}

impl Backend {
    pub fn new(client: tower_lsp::Client, toml_version: Option<TomlVersion>) -> Self {
        Self {
            client,
            document_infos: Default::default(),
            toml_version,
            config: config::load(),
        }
    }

    pub fn insert_document_info(&self, uri: Url, document_info: DocumentInfo) {
        self.document_infos.insert(uri, document_info);
    }

    pub fn get_document_info(&self, uri: &Url) -> Option<Ref<Url, DocumentInfo>> {
        self.document_infos.get(uri)
    }

    pub fn get_mut_document_info(&self, uri: &Url) -> Option<RefMut<Url, DocumentInfo>> {
        self.document_infos.get_mut(uri)
    }

    pub fn try_get_mut_document_info(&self, uri: &Url) -> TryResult<RefMut<Url, DocumentInfo>> {
        self.document_infos.try_get_mut(uri)
    }

    pub fn get_ast(&self, uri: &Url) -> Option<ast::Root> {
        self.get_document_info(uri)
            .map(|document_info| {
                let p = parser::parse(&document_info.source, self.toml_version());
                if !p.errors().is_empty() {
                    return None;
                }

                ast::Root::cast(p.into_syntax_node())
            })
            .flatten()
    }

    pub fn toml_version(&self) -> TomlVersion {
        self.toml_version
            .unwrap_or(self.config.toml_version.unwrap_or_default())
    }

    pub fn format_options(&self) -> &config::FormatOptions {
        self.config
            .format
            .as_ref()
            .unwrap_or_else(|| &config::DEFAULT_FORMAT_OPTIONS)
    }

    pub fn lint_options(&self) -> &config::LintOptions {
        self.config
            .lint
            .as_ref()
            .unwrap_or_else(|| &config::DEFAULT_LINT_OPTIONS)
    }
}

#[tower_lsp::async_trait]
impl LanguageServer for Backend {
    async fn initialize(
        &self,
        params: InitializeParams,
    ) -> Result<InitializeResult, tower_lsp::jsonrpc::Error> {
        handle_initialize(params)
    }

    async fn shutdown(&self) -> Result<(), tower_lsp::jsonrpc::Error> {
        handle_shutdown()
    }

    async fn did_open(&self, params: DidOpenTextDocumentParams) {
        handle_did_open(self, params).await
    }

    async fn did_change(&self, params: DidChangeTextDocumentParams) {
        handle_did_change(self, params).await
    }

    async fn did_save(&self, params: DidSaveTextDocumentParams) {
        handle_did_save(self, params).await
    }

    async fn did_change_configuration(&self, params: DidChangeConfigurationParams) {
        handle_did_change_configuration(params).await
    }

    async fn semantic_tokens_full(
        &self,
        params: SemanticTokensParams,
    ) -> Result<Option<SemanticTokensResult>, tower_lsp::jsonrpc::Error> {
        handle_semantic_tokens_full(self, params).await
    }

    async fn document_symbol(
        &self,
        params: DocumentSymbolParams,
    ) -> Result<Option<DocumentSymbolResponse>, tower_lsp::jsonrpc::Error> {
        handle_document_symbol(self, params).await
    }

    async fn hover(&self, params: HoverParams) -> Result<Option<Hover>, tower_lsp::jsonrpc::Error> {
        handle_hover(params).await
    }

    async fn folding_range(
        &self,
        params: FoldingRangeParams,
    ) -> Result<Option<Vec<FoldingRange>>, tower_lsp::jsonrpc::Error> {
        handle_folding_range(self, params).await
    }

    async fn formatting(
        &self,
        params: tower_lsp::lsp_types::DocumentFormattingParams,
    ) -> Result<Option<Vec<tower_lsp::lsp_types::TextEdit>>, tower_lsp::jsonrpc::Error> {
        handle_formatting(self, params).await
    }

    async fn diagnostic(
        &self,
        params: DocumentDiagnosticParams,
    ) -> Result<DocumentDiagnosticReportResult, tower_lsp::jsonrpc::Error> {
        handle_diagnostic(self, params).await
    }
}
