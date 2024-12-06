#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum IntegerKind {
    Binary,
    Decimal,
    Octal,
    Hexadecimal,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Integer {
    kind: IntegerKind,
    value: isize,
}

impl Integer {
    pub fn try_new_integer_bin(text: &str) -> Result<Self, std::num::ParseIntError> {
        isize::from_str_radix(&text[2..], 2).map(|value| Self {
            kind: IntegerKind::Binary,
            value,
        })
    }

    pub fn try_new_integer_dec(text: &str) -> Result<Self, std::num::ParseIntError> {
        isize::from_str_radix(text, 10).map(|value| Self {
            kind: IntegerKind::Decimal,
            value,
        })
    }

    pub fn try_new_integer_oct(text: &str) -> Result<Self, std::num::ParseIntError> {
        isize::from_str_radix(&text[2..], 8).map(|value| Self {
            kind: IntegerKind::Octal,
            value,
        })
    }

    pub fn try_new_integer_hex(text: &str) -> Result<Self, std::num::ParseIntError> {
        isize::from_str_radix(&text[2..], 16).map(|value| Self {
            kind: IntegerKind::Hexadecimal,
            value,
        })
    }

    #[inline]
    pub fn kind(&self) -> IntegerKind {
        self.kind
    }

    #[inline]
    pub fn value(&self) -> isize {
        self.value
    }
}

impl TryFrom<ast::IntegerBin> for Integer {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::IntegerBin) -> Result<Self, Self::Error> {
        let token = node.token().unwrap();
        Self::try_new_integer_bin(token.text()).map_err(|err| {
            vec![crate::Error::ParseIntError {
                error: err,
                range: token.text_range(),
            }]
        })
    }
}

impl TryFrom<ast::IntegerOct> for Integer {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::IntegerOct) -> Result<Self, Self::Error> {
        let token = node.token().unwrap();
        Self::try_new_integer_oct(token.text()).map_err(|err| {
            vec![crate::Error::ParseIntError {
                error: err,
                range: token.text_range(),
            }]
        })
    }
}

impl TryFrom<ast::IntegerDec> for Integer {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::IntegerDec) -> Result<Self, Self::Error> {
        let token = node.token().unwrap();
        Self::try_new_integer_dec(token.text()).map_err(|err| {
            vec![crate::Error::ParseIntError {
                error: err,
                range: token.text_range(),
            }]
        })
    }
}

impl TryFrom<ast::IntegerHex> for Integer {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::IntegerHex) -> Result<Self, Self::Error> {
        let token = node.token().unwrap();
        Self::try_new_integer_hex(token.text()).map_err(|err| {
            vec![crate::Error::ParseIntError {
                error: err,
                range: token.text_range(),
            }]
        })
    }
}

#[cfg(feature = "serde")]
impl serde::Serialize for Integer {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: serde::Serializer,
    {
        self.value.serialize(serializer)
    }
}
