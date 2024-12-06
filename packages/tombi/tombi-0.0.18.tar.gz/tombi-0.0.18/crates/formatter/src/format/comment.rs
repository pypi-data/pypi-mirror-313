use super::Format;
use std::fmt::Write;

impl Format for ast::Comment {
    #[inline]
    fn fmt(&self, f: &mut crate::Formatter) -> Result<(), std::fmt::Error> {
        let comment = self.to_string();
        let mut iter = comment.trim_ascii_end().chars();
        write!(f, "{}", iter.next().unwrap())?;

        if let Some(c) = iter.next() {
            if c != ' ' && c != '\t' {
                write!(f, " ")?;
            }
            write!(f, "{}", c)?;
        }

        write!(f, "{}", iter.as_str())
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BeginDanglingComment(pub ast::Comment);

impl Format for BeginDanglingComment {
    #[inline]
    fn fmt(&self, f: &mut crate::Formatter) -> Result<(), std::fmt::Error> {
        f.write_indent()?;
        self.0.fmt(f)?;
        write!(f, "{}", f.line_ending())
    }
}

impl Format for Vec<BeginDanglingComment> {
    #[inline]
    fn fmt(&self, f: &mut crate::Formatter) -> Result<(), std::fmt::Error> {
        if self.is_empty() {
            return Ok(());
        }

        for comment in self {
            comment.fmt(f)?;
        }
        write!(f, "{}", f.line_ending())
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct EndDanglingComment(pub ast::Comment);

impl Format for EndDanglingComment {
    #[inline]
    fn fmt(&self, f: &mut crate::Formatter) -> Result<(), std::fmt::Error> {
        write!(f, "{}", f.line_ending())?;
        f.write_indent()?;
        self.0.fmt(f)
    }
}

impl Format for Vec<EndDanglingComment> {
    #[inline]
    fn fmt(&self, f: &mut crate::Formatter) -> Result<(), std::fmt::Error> {
        if self.is_empty() {
            return Ok(());
        }

        write!(f, "{}", f.line_ending())?;

        for comment in self {
            comment.fmt(f)?;
        }

        Ok(())
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DanglingComment(pub ast::Comment);

impl Format for DanglingComment {
    #[inline]
    fn fmt(&self, f: &mut crate::Formatter) -> Result<(), std::fmt::Error> {
        f.write_indent()?;
        self.0.fmt(f)
    }
}

impl Format for Vec<DanglingComment> {
    #[inline]
    fn fmt(&self, f: &mut crate::Formatter) -> Result<(), std::fmt::Error> {
        for (i, comment) in self.iter().enumerate() {
            if i > 0 {
                write!(f, "{}", f.line_ending())?;
            }
            comment.fmt(f)?;
        }
        Ok(())
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LeadingComment(pub ast::Comment);

impl Format for LeadingComment {
    #[inline]
    fn fmt(&self, f: &mut crate::Formatter) -> Result<(), std::fmt::Error> {
        f.write_indent()?;
        self.0.fmt(f)?;
        write!(f, "{}", f.line_ending())
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TailingComment(pub ast::Comment);

impl Format for TailingComment {
    #[inline]
    fn fmt(&self, f: &mut crate::Formatter) -> Result<(), std::fmt::Error> {
        write!(f, "{}", f.defs().tailing_comment_space())?;
        self.0.fmt(f)
    }
}

#[cfg(test)]
mod tests {
    use crate::test_format;

    test_format! {
        #[test]
        fn comment_without_space(r"#comment") -> Ok("# comment");
    }

    test_format! {
        #[test]
        fn empty_comment(r"#") -> Ok(source);
    }

    test_format! {
        #[test]
        fn only_space_comment1(r"# ") -> Ok(r"#");
    }

    test_format! {
        #[test]
        fn only_space_comment2(r"#      ") -> Ok(r"#");
    }
}
