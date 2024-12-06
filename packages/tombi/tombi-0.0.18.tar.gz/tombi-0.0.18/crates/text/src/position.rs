use std::{
    cmp::Ordering,
    ops::{Add, AddAssign},
};

use crate::{Column, Line, Offset, RelativePosition};

#[derive(Default, Debug, Copy, Clone, Eq, PartialEq, Hash)]
pub struct Position {
    line: Line,
    column: Column,
}

impl Position {
    pub const MAX: Position = Position {
        line: Line::MAX,
        column: Column::MAX,
    };
    pub const MIN: Position = Position {
        line: Line::MIN,
        column: Column::MIN,
    };

    #[inline]
    pub const fn new(line: Line, column: Column) -> Self {
        Self { line, column }
    }

    #[inline]
    pub fn add_text(&self, text: &str) -> Self {
        (*self) + RelativePosition::of(text)
    }

    /// FIXME: This method will be unnecessary because parser holds the Position of each tokens.
    pub fn from_source(source: &str, offset: Offset) -> Self {
        let offset: usize = offset.into();
        let mut line = 0;
        let mut column = 0;
        for (i, c) in source.char_indices() {
            if i == offset {
                return Self { line, column };
            }
            if c == '\n' {
                line += 1;
                column = 0;
            } else {
                column += 1;
            }
        }
        Self { line, column }
    }

    #[inline]
    pub fn line(&self) -> Line {
        self.line
    }

    #[inline]
    pub fn column(&self) -> Column {
        self.column
    }
}

impl std::fmt::Display for Position {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}:{}", self.line, self.column)
    }
}

impl Ord for Position {
    fn cmp(&self, other: &Self) -> Ordering {
        self.line
            .cmp(&other.line)
            .then_with(|| self.column.cmp(&other.column))
    }
}

impl PartialOrd for Position {
    #[inline]
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl From<(Line, Column)> for Position {
    #[inline]
    fn from((line, column): (Line, Column)) -> Self {
        Self::new(line, column)
    }
}

impl Add<RelativePosition> for Position {
    type Output = Position;

    #[inline]
    fn add(self, rhs: RelativePosition) -> Self::Output {
        let line = self.line + rhs.line();
        let column = if rhs.line() == 0 {
            self.column + rhs.column()
        } else {
            rhs.column()
        };
        Position::new(line, column)
    }
}

impl AddAssign<RelativePosition> for Position {
    #[inline]
    fn add_assign(&mut self, rhs: RelativePosition) {
        self.line += rhs.line();
        if rhs.line() == 0 {
            self.column += rhs.column();
        } else {
            self.column = rhs.column();
        }
    }
}

#[cfg(test)]
mod test {
    #[test]
    fn test_position_cmp() {
        use super::Position;

        let p1 = Position::new(1, 2);
        let p2 = Position::new(1, 3);
        let p3 = Position::new(2, 0);

        assert!(p1 < p2);
        assert!(p2 < p3);
        assert!(p1 < p3);
    }
}
