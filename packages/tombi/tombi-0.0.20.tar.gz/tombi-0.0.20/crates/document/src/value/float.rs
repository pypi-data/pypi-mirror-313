#[derive(Debug, Clone, PartialEq)]
pub struct Float {
    value: f64,
}

impl Float {
    pub fn try_new(text: &str) -> Result<Self, std::num::ParseFloatError> {
        Ok(Self {
            value: text.parse()?,
        })
    }

    pub fn value(&self) -> f64 {
        self.value
    }
}

impl TryFrom<ast::Float> for Float {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::Float) -> Result<Self, Self::Error> {
        let token = node.token().unwrap();
        Self::try_new(token.text()).map_err(|err| {
            vec![crate::Error::ParseFloatError {
                error: err,
                range: token.text_range(),
            }]
        })
    }
}

#[cfg(feature = "serde")]
impl serde::Serialize for Float {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: serde::Serializer,
    {
        self.value.serialize(serializer)
    }
}

#[cfg(test)]
mod test {
    #[test]
    fn inf() {
        let float = crate::value::Float::try_new("inf").unwrap();
        assert_eq!(float.value(), std::f64::INFINITY);
    }

    #[test]
    fn p_inf() {
        let float = crate::value::Float::try_new("+inf").unwrap();
        assert_eq!(float.value(), std::f64::INFINITY);
    }

    #[test]
    fn m_inf() {
        let float = crate::value::Float::try_new("-inf").unwrap();
        assert_eq!(float.value(), std::f64::NEG_INFINITY);
    }

    #[test]
    fn nan() {
        let float = crate::value::Float::try_new("nan").unwrap();
        assert!(float.value().is_nan());
    }

    #[test]
    fn p_nan() {
        let float = crate::value::Float::try_new("+nan").unwrap();
        assert!(float.value().is_nan());
    }

    #[test]
    fn m_nan() {
        let float = crate::value::Float::try_new("-nan").unwrap();
        assert!(float.value().is_nan());
    }
}
