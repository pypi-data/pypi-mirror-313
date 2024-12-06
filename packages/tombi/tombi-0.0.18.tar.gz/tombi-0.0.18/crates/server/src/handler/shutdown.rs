#[tracing::instrument(level = "debug", skip_all)]
pub fn handle_shutdown() -> Result<(), tower_lsp::jsonrpc::Error> {
    tracing::info!("Server shutting down");

    Ok(())
}
