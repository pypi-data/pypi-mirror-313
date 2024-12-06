use tower_lsp::lsp_types::Url;

pub fn try_load(url: &Url) -> Result<String, tower_lsp::jsonrpc::Error> {
    let path = url
        .to_file_path()
        .map_err(|_| tower_lsp::jsonrpc::Error::invalid_params(format!("{url} not found!")))?;
    let content = std::fs::read_to_string(path)
        .map_err(|_| tower_lsp::jsonrpc::Error::invalid_params(format!("{url} cannot load!")))?;
    Ok(content)
}
