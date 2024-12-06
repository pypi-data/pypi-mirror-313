#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Boolean {
    value: bool,
}

impl Boolean {
    pub(crate) fn new(text: &str) -> Self {
        Self {
            value: match text {
                "true" => true,
                "false" => false,
                _ => unreachable!(),
            },
        }
    }

    #[inline]
    pub fn value(&self) -> bool {
        self.value
    }
}

impl TryFrom<ast::Boolean> for Boolean {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::Boolean) -> Result<Self, Self::Error> {
        let token = node.token().unwrap();
        Ok(Self::new(token.text()))
    }
}

#[cfg(feature = "serde")]
impl serde::Serialize for Boolean {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: serde::Serializer,
    {
        self.value.serialize(serializer)
    }
}
