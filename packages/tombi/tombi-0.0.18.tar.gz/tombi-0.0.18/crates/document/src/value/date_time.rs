#[derive(Debug, Clone, PartialEq, Eq)]
pub struct OffsetDateTime {
    value: chrono::DateTime<chrono::FixedOffset>,
    range: text::Range,
}

impl OffsetDateTime {
    pub fn try_new(text: &str, range: text::Range) -> Result<Self, chrono::ParseError> {
        Ok(Self {
            value: chrono::DateTime::parse_from_rfc3339(text)?,
            range,
        })
    }

    #[inline]
    pub fn value(&self) -> &chrono::DateTime<chrono::FixedOffset> {
        &self.value
    }

    #[inline]
    pub fn range(&self) -> text::Range {
        self.range
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LocalDateTime {
    value: chrono::DateTime<chrono::Local>,
    range: text::Range,
}

impl LocalDateTime {
    pub fn try_new(text: &str, range: text::Range) -> Result<Self, chrono::ParseError> {
        chrono::DateTime::parse_from_rfc3339(text).map(|value| Self {
            value: value.with_timezone(&chrono::Local),
            range,
        })
    }

    #[inline]
    pub fn value(&self) -> &chrono::DateTime<chrono::Local> {
        &self.value
    }

    #[inline]
    pub fn range(&self) -> text::Range {
        self.range
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LocalDate {
    value: chrono::NaiveDate,
    range: text::Range,
}

impl LocalDate {
    pub fn try_new(text: &str, range: text::Range) -> Result<Self, chrono::ParseError> {
        Ok(Self {
            value: chrono::NaiveDate::parse_from_str(text, "%Y-%m-%d")?,
            range,
        })
    }

    #[inline]
    pub fn value(&self) -> &chrono::NaiveDate {
        &self.value
    }

    #[inline]
    pub fn range(&self) -> text::Range {
        self.range
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LocalTime {
    value: chrono::NaiveTime,
}

impl LocalTime {
    pub fn try_new(text: &str) -> Result<Self, chrono::ParseError> {
        Ok(Self {
            value: chrono::NaiveTime::parse_from_str(text, "%H:%M:%S%.f")?,
        })
    }

    #[inline]
    pub fn value(&self) -> &chrono::NaiveTime {
        &self.value
    }

    #[inline]
    pub fn range(&self) -> text::Range {
        text::Range::default()
    }
}
