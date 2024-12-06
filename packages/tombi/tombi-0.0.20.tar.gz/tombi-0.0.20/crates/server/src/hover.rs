use std::fmt::Debug;

use itertools::Itertools;

#[derive(Debug, Default)]
pub struct HoverContent {
    pub title: Option<String>,
    pub description: Option<String>,
    pub keys: String,
    pub enumerated_values: Vec<String>,
    pub schema_url: Option<tower_lsp::lsp_types::Url>,
    pub range: text::Range,
}

impl std::fmt::Display for HoverContent {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        if let Some(title) = &self.title {
            writeln!(f, "## {}\n", title)?;
        }

        if let Some(description) = &self.description {
            writeln!(f, "{}\n", description.split("\n").join("\n\n"))?;
        }

        writeln!(f, "Keys: `{}`\n", self.keys)?;

        if !self.enumerated_values.is_empty() {
            writeln!(f, "Allowed Values:\n")?;
            for value in &self.enumerated_values {
                writeln!(f, "- `{}`", value)?;
            }
            writeln!(f)?;
        }

        if let Some(schema_url) = &self.schema_url {
            if let Some(schema_filename) = get_schema_name(schema_url) {
                writeln!(f, "Source: [{schema_filename}]({schema_url})\n",)?;
            }
        }
        Ok(())
    }
}

impl HoverContent {
    pub fn into_hover(self) -> tower_lsp::lsp_types::Hover {
        tower_lsp::lsp_types::Hover {
            contents: tower_lsp::lsp_types::HoverContents::Markup(
                tower_lsp::lsp_types::MarkupContent {
                    kind: tower_lsp::lsp_types::MarkupKind::Markdown,
                    value: self.to_string(),
                },
            ),
            range: Some(self.range.into()),
        }
    }
}

fn get_schema_name(schema_url: &tower_lsp::lsp_types::Url) -> Option<&str> {
    if let Some(path) = schema_url.path().split('/').last() {
        if !path.is_empty() {
            return Some(path);
        }
    }
    schema_url.host_str()
}

#[cfg(test)]
mod test {
    use super::*;
    use rstest::rstest;
    use tower_lsp::lsp_types::Url;

    #[rstest]
    #[case("https://json.schemastore.org/tombi.schema.json")]
    #[case("file://./folder/tombi.schema.json")]
    #[case("file://./tombi.schema.json")]
    #[case("file://tombi.schema.json")]
    fn url_content(#[case] url: &str) {
        let url = Url::parse(url).unwrap();
        assert_eq!(get_schema_name(&url).unwrap(), "tombi.schema.json");
    }
}
