use crate::{
    format::comment::{LeadingComment, TailingComment},
    Format,
};
use ast::AstNode;
use std::fmt::Write;

use crate::format::comment::{BeginDanglingComment, EndDanglingComment};

impl Format for ast::InlineTable {
    fn fmt(&self, f: &mut crate::Formatter) -> Result<(), std::fmt::Error> {
        if self.should_be_multiline(f.toml_version()) {
            format_multiline_inline_table(self, f)
        } else {
            format_singleline_inline_table(self, f)
        }
    }
}

fn format_multiline_inline_table(
    table: &ast::InlineTable,
    f: &mut crate::Formatter,
) -> Result<(), std::fmt::Error> {
    for comment in table.leading_comments() {
        LeadingComment(comment).fmt(f)?;
    }

    f.write_indent()?;
    write!(f, "{{{}", f.line_ending())?;

    f.inc_indent();

    table
        .inner_begin_dangling_comments()
        .map(BeginDanglingComment)
        .collect::<Vec<_>>()
        .fmt(f)?;

    for (i, (key_value, comma)) in table.key_values_with_comma().enumerate() {
        // value format
        {
            if i > 0 {
                write!(f, "{}", f.line_ending())?;
            }
            key_value.fmt(f)?;
        }

        // comma format
        {
            let (comma_leading_comments, comma_tailing_comment) = match comma {
                Some(comma) => (
                    comma.leading_comments().collect::<Vec<_>>(),
                    comma.tailing_comment(),
                ),
                None => (vec![], None),
            };

            if !comma_leading_comments.is_empty() {
                write!(f, "{}", f.line_ending())?;
                for comment in comma_leading_comments {
                    LeadingComment(comment).fmt(f)?;
                }
                f.write_indent()?;
                write!(f, ",")?;
            } else if key_value.tailing_comment().is_some() {
                write!(f, "{}", f.line_ending())?;
                f.write_indent()?;
                write!(f, ",")?;
            } else {
                write!(f, ",")?;
            }

            if let Some(comment) = comma_tailing_comment {
                TailingComment(comment).fmt(f)?;
            }
        }
    }

    table
        .inner_end_dangling_comments()
        .map(EndDanglingComment)
        .collect::<Vec<_>>()
        .fmt(f)?;

    f.dec_indent();

    write!(f, "{}", f.line_ending())?;
    f.write_indent()?;
    write!(f, "}}")?;

    if let Some(comment) = table.tailing_comment() {
        TailingComment(comment).fmt(f)?;
    }

    Ok(())
}

fn format_singleline_inline_table(
    table: &ast::InlineTable,
    f: &mut crate::Formatter,
) -> Result<(), std::fmt::Error> {
    for comment in table.leading_comments() {
        LeadingComment(comment).fmt(f)?;
    }

    f.write_indent()?;
    write!(
        f,
        "{{{}",
        f.defs().singleline_inline_table_brace_inner_space()
    )?;

    for (i, key_value) in table.key_values().enumerate() {
        if i > 0 {
            write!(
                f,
                ",{}",
                f.defs().singleline_inline_table_space_after_comma()
            )?;
        }
        f.skip_indent();
        key_value.fmt(f)?;
    }

    write!(
        f,
        "{}}}",
        f.defs().singleline_inline_table_brace_inner_space()
    )?;

    if let Some(comment) = table.tailing_comment() {
        TailingComment(comment).fmt(f)?;
    }

    Ok(())
}

#[cfg(test)]
mod tests {
    use crate::test_format;

    test_format! {
        #[test]
        fn inline_table_key_value1(r#"name = { first = "Tom", last = "Preston-Werner" }"#) -> Ok(source);
    }

    test_format! {
        #[test]
        fn inline_table_key_value2(r#"point = { x = 1, y = 2 }"#) -> Ok(source);

    }

    test_format! {
        #[test]
        fn inline_table_key_value3(r#"animal = { type.name = "pug" }"#) -> Ok(source);
    }
}
