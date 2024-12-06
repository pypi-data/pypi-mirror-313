use crate::format::{DateTimeDelimiter, IdentStyle, IdentWidth, LineEnding};

#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
#[cfg_attr(feature = "serde", serde(rename_all = "kebab-case"))]
#[cfg_attr(feature = "jsonschema", derive(schemars::JsonSchema))]
#[derive(Debug, Default, Clone)]
pub struct FormatOptions {
    /// # The style of indentation.
    ///
    /// Whether to use spaces or tabs for indentation.
    #[cfg_attr(feature = "jsonschema", schemars(default = "IdentStyle::default"))]
    pub indent_style: Option<IdentStyle>,

    /// # The number of spaces per indentation level.
    #[cfg_attr(feature = "jsonschema", schemars(default = "IdentWidth::default"))]
    pub indent_width: Option<IdentWidth>,

    /// # The type of line ending.
    ///
    /// In TOML, the line ending must be either `LF` or `CRLF`.
    ///
    /// - `lf`: Line Feed only (`\n`), common on Linux and macOS as well as inside git repos.
    /// - `crlf`: Carriage Return Line Feed (`\r\n`), common on Windows.
    pub line_ending: Option<LineEnding>,

    /// # The delimiter between date and time.
    ///
    /// In accordance with [RFC 3339](https://datatracker.ietf.org/doc/html/rfc3339), you can use `T` or space character between date and time.
    ///
    /// - `T`: Example: `2001-01-01T00:00:00`
    /// - `space`: Example: `2001-01-01 00:00:00`
    /// - `preserve`: Preserve the original delimiter.
    #[cfg_attr(
        feature = "jsonschema",
        schemars(default = "DateTimeDelimiter::default")
    )]
    pub date_time_delimiter: Option<DateTimeDelimiter>,
}

impl FormatOptions {
    pub fn merge(&mut self, other: &FormatOptions) -> &mut Self {
        if let Some(line_ending) = other.line_ending {
            self.line_ending = Some(line_ending);
        }
        if let Some(date_time_delimiter) = other.date_time_delimiter {
            self.date_time_delimiter = Some(date_time_delimiter);
        }

        self
    }

    #[inline]
    pub fn date_time_delimiter(&self) -> DateTimeDelimiter {
        self.date_time_delimiter.unwrap_or_default()
    }

    #[inline]
    pub fn ident(&self, depth: u8) -> String {
        match self.indent_style.unwrap_or_default() {
            IdentStyle::Space => {
                " ".repeat((self.indent_width.unwrap_or_default().value() * depth) as usize)
            }
            IdentStyle::Tab => "\t".repeat(depth as usize),
        }
    }
}
