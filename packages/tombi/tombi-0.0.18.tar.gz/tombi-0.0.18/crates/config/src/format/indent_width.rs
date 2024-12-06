#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
#[cfg_attr(feature = "jsonschema", derive(schemars::JsonSchema))]
pub struct IdentWidth(u8);

impl IdentWidth {
    #[inline]
    pub fn value(&self) -> u8 {
        self.0
    }
}

impl Default for IdentWidth {
    fn default() -> Self {
        Self(2)
    }
}

impl From<u8> for IdentWidth {
    fn from(value: u8) -> Self {
        Self(value)
    }
}
