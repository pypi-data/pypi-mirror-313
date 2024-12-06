/// Definitions provides the definition of the format that does not have the freedom set by [`FormatOptions`][crate::FormatOptions].
///
/// NOTE: Some of the items defined in Definitions may be moved to [`FormatOptions`][crate::FormatOptions] in the future.
#[derive(Debug, Default, Clone, Copy)]
pub struct Definitions {}

impl Definitions {
    /// Returns the space before the tailing comment.
    ///
    /// ```toml
    /// key = "value"  # tailing comment
    /// #            ^^  <-this space
    /// ```
    #[inline]
    pub const fn tailing_comment_space(&self) -> &'static str {
        "  "
    }

    /// Returns the space inside the brackets of an array.
    ///
    /// ```toml
    /// key = [ 1, 2, 3 ]
    /// #      ^       ^  <- this space
    #[inline]
    pub const fn singleline_array_bracket_inner_space(&self) -> &'static str {
        ""
    }

    /// Returns the space after the comma in an array.
    ///
    /// ```toml
    /// key = [ 1, 2, 3 ]
    /// #         ^  ^    <- this space
    #[inline]
    pub const fn singleline_array_space_after_comma(&self) -> &'static str {
        " "
    }

    /// Returns the space inside the brackets of an inline table.
    ///
    /// ```toml
    /// key = { a = 1, b = 2 }
    /// #      ^            ^  <- this space
    /// ```
    #[inline]
    pub const fn singleline_inline_table_brace_inner_space(&self) -> &'static str {
        " "
    }

    /// Returns the space after the comma in an inline table.
    ///
    /// ```toml
    /// key = { a = 1, b = 2 }
    /// #             ^  <- this space
    /// ```
    #[inline]
    pub const fn singleline_inline_table_space_after_comma(&self) -> &'static str {
        " "
    }
}
