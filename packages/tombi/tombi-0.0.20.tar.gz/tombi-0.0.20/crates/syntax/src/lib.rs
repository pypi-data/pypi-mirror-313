mod builder;
mod error;
mod generated;
mod language;

pub use builder::SyntaxTreeBuilder;
pub use error::Error;
pub use generated::SyntaxKind;
pub use language::TomlLanguage;

pub type SyntaxNode = rg_tree::RedNode<TomlLanguage>;
pub type SyntaxToken = rg_tree::RedToken<TomlLanguage>;
pub type SyntaxElement = rg_tree::RedElement<TomlLanguage>;
pub type SyntaxNodeChildren = rg_tree::RedNodeChildren<TomlLanguage>;
pub type SyntaxElementChildren = rg_tree::RedElementChildren<TomlLanguage>;
pub type PreorderWithTokens = rg_tree::PreorderWithTokens<TomlLanguage>;
