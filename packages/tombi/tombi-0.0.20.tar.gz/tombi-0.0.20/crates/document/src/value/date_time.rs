#[derive(Debug, Clone, PartialEq, Eq)]
pub struct OffsetDateTime {
    value: chrono::DateTime<chrono::FixedOffset>,
}

impl OffsetDateTime {
    pub fn try_new(text: &str) -> Result<Self, chrono::ParseError> {
        Ok(Self {
            value: chrono::DateTime::parse_from_rfc3339(text)?,
        })
    }

    #[inline]
    pub fn value(&self) -> &chrono::DateTime<chrono::FixedOffset> {
        &self.value
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LocalDateTime {
    value: chrono::DateTime<chrono::Local>,
}

impl LocalDateTime {
    pub fn try_new(text: &str) -> Result<Self, chrono::ParseError> {
        chrono::DateTime::parse_from_rfc3339(text).map(|value| Self {
            value: value.with_timezone(&chrono::Local),
        })
    }

    #[inline]
    pub fn value(&self) -> &chrono::DateTime<chrono::Local> {
        &self.value
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LocalDate {
    value: chrono::NaiveDate,
}

impl LocalDate {
    pub fn try_new(text: &str) -> Result<Self, chrono::ParseError> {
        Ok(Self {
            value: chrono::NaiveDate::parse_from_str(text, "%Y-%m-%d")?,
        })
    }

    #[inline]
    pub fn value(&self) -> &chrono::NaiveDate {
        &self.value
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

impl TryFrom<ast::OffsetDateTime> for OffsetDateTime {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::OffsetDateTime) -> Result<Self, Self::Error> {
        let token = node.token().unwrap();
        Self::try_new(token.text()).map_err(|err| {
            vec![crate::Error::ParseOffsetDateTimeError {
                error: err,
                range: token.text_range(),
            }]
        })
    }
}

impl TryFrom<ast::LocalDateTime> for LocalDateTime {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::LocalDateTime) -> Result<Self, Self::Error> {
        let token = node.token().unwrap();
        Self::try_new(token.text()).map_err(|err| {
            vec![crate::Error::ParseLocalDateTimeError {
                error: err,
                range: token.text_range(),
            }]
        })
    }
}

impl TryFrom<ast::LocalDate> for LocalDate {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::LocalDate) -> Result<Self, Self::Error> {
        let token = node.token().unwrap();
        Self::try_new(token.text()).map_err(|err| {
            vec![crate::Error::ParseLocalDateError {
                error: err,
                range: token.text_range(),
            }]
        })
    }
}

impl TryFrom<ast::LocalTime> for LocalTime {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::LocalTime) -> Result<Self, Self::Error> {
        let token = node.token().unwrap();
        Self::try_new(token.text()).map_err(|err| {
            vec![crate::Error::ParseLocalTimeError {
                error: err,
                range: token.text_range(),
            }]
        })
    }
}

#[cfg(feature = "serde")]
impl serde::Serialize for OffsetDateTime {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: serde::Serializer,
    {
        self.value.serialize(serializer)
    }
}

#[cfg(feature = "serde")]
impl serde::Serialize for LocalDateTime {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: serde::Serializer,
    {
        self.value.serialize(serializer)
    }
}

#[cfg(feature = "serde")]
impl serde::Serialize for LocalDate {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: serde::Serializer,
    {
        self.value.serialize(serializer)
    }
}

#[cfg(feature = "serde")]
impl serde::Serialize for LocalTime {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: serde::Serializer,
    {
        self.value.serialize(serializer)
    }
}
