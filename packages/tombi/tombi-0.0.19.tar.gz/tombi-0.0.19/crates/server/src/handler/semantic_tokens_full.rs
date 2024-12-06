use crate::backend::Backend;
use crate::toml;
use ast::{AstNode, AstToken};
use config::TomlVersion;
use parser::{SyntaxNode, SyntaxToken};
use text::Span;
use tower_lsp::lsp_types::{
    Position, Range, SemanticToken, SemanticTokenType, SemanticTokens, SemanticTokensParams,
    SemanticTokensResult,
};

macro_rules! token_types {
    (
        standard {
            $($standard:ident),*$(,)?
        }
        custom {
            $(($custom:ident, $string:literal)),*$(,)?
        }
    ) => {
        pub mod token_type {
            use super::SemanticTokenType;

            $(pub(crate) const $custom: SemanticTokenType = SemanticTokenType::new($string);)*
        }

        pub enum TokenType {
            $($standard,)*
            $($custom),*
        }

        pub const SUPPORTED_TOKEN_TYPES: &[SemanticTokenType] = &[
            $(SemanticTokenType::$standard,)*
            $(self::token_type::$custom),*
        ];
    }
}

token_types! {
    standard {
        STRUCT,
        STRING,
        NUMBER,
        VARIABLE,
        OPERATOR,
        COMMENT,
    }
    custom {
        (BOOLEAN, "boolean"),
        // NOTE: "datetime" does not exist, so we will use "regexp" instead.
        (DATETIME, "regexp"),
    }
}

#[tracing::instrument(level = "debug", skip_all)]
pub async fn handle_semantic_tokens_full(
    _backend: &Backend,
    SemanticTokensParams { text_document, .. }: SemanticTokensParams,
) -> Result<Option<SemanticTokensResult>, tower_lsp::jsonrpc::Error> {
    tracing::info!("semantic_tokens_full");

    let source = toml::try_load(&text_document.uri)?;

    let p = parser::parse(&source, TomlVersion::default());
    let Some(ast) = ast::Root::cast(p.into_syntax_node()) else {
        return Ok(None);
    };

    let mut tokens_builder = SemanticTokensBuilder::new(&source);
    ast.append_semantic_tokens(&mut tokens_builder);
    let tokens = tokens_builder.build();

    tracing::debug!("SemanticTokens: {tokens:#?}");

    Ok(Some(SemanticTokensResult::Tokens(SemanticTokens {
        result_id: None,
        data: tokens,
    })))
}

trait AppendSemanticTokens {
    fn append_semantic_tokens(&self, builder: &mut SemanticTokensBuilder);
}

impl AppendSemanticTokens for ast::Root {
    fn append_semantic_tokens(&self, builder: &mut SemanticTokensBuilder) {
        for comment in self.begin_dangling_comments() {
            builder.add_token(TokenType::COMMENT, comment.syntax().into());
        }

        for item in self.items() {
            item.append_semantic_tokens(builder);
        }

        for comment in self.end_dangling_comments() {
            builder.add_token(TokenType::COMMENT, comment.syntax().into());
        }
    }
}

impl AppendSemanticTokens for ast::RootItem {
    fn append_semantic_tokens(&self, builder: &mut SemanticTokensBuilder) {
        match self {
            Self::Table(table) => table.append_semantic_tokens(builder),
            Self::ArrayOfTable(array) => array.append_semantic_tokens(builder),
            Self::KeyValue(key_value) => key_value.append_semantic_tokens(builder),
        }
    }
}

impl AppendSemanticTokens for ast::Table {
    fn append_semantic_tokens(&self, builder: &mut SemanticTokensBuilder) {
        for comment in self.header_leading_comments() {
            builder.add_token(TokenType::COMMENT, comment.syntax().into());
        }

        if let Some(token) = self.bracket_start() {
            builder.add_token(TokenType::OPERATOR, (&token).into())
        }

        if let Some(header) = self.header() {
            for key in header.keys() {
                builder.add_token(TokenType::STRUCT, key.syntax().into());
            }
        }

        if let Some(token) = self.bracket_end() {
            builder.add_token(TokenType::OPERATOR, (&token).into())
        }

        if let Some(comment) = self.header_tailing_comment() {
            builder.add_token(TokenType::COMMENT, comment.syntax().into())
        }

        for key_value in self.key_values() {
            key_value.append_semantic_tokens(builder);
        }
    }
}

impl AppendSemanticTokens for ast::ArrayOfTable {
    fn append_semantic_tokens(&self, builder: &mut SemanticTokensBuilder) {
        for comment in self.header_leading_comments() {
            builder.add_token(TokenType::COMMENT, comment.syntax().into());
        }

        if let Some(token) = self.double_bracket_start() {
            builder.add_token(TokenType::OPERATOR, (&token).into());
        }

        if let Some(header) = self.header() {
            for key in header.keys() {
                builder.add_token(TokenType::STRUCT, key.syntax().into());
            }
        }

        if let Some(token) = self.double_bracket_end() {
            builder.add_token(TokenType::OPERATOR, (&token).into());
        }

        if let Some(comment) = self.header_tailing_comment() {
            builder.add_token(TokenType::COMMENT, comment.syntax().into())
        }

        for key_value in self.key_values() {
            key_value.append_semantic_tokens(builder);
        }
    }
}

impl AppendSemanticTokens for ast::KeyValue {
    fn append_semantic_tokens(&self, builder: &mut SemanticTokensBuilder) {
        for comment in self.leading_comments() {
            builder.add_token(TokenType::COMMENT, comment.syntax().into());
        }

        if let Some(key) = self.keys() {
            key.append_semantic_tokens(builder)
        }

        if let Some(value) = self.value() {
            value.append_semantic_tokens(builder)
        }
    }
}

impl AppendSemanticTokens for ast::Keys {
    fn append_semantic_tokens(&self, builder: &mut SemanticTokensBuilder) {
        for key in self.keys() {
            key.append_semantic_tokens(builder);
        }
    }
}

impl AppendSemanticTokens for ast::Key {
    fn append_semantic_tokens(&self, builder: &mut SemanticTokensBuilder) {
        builder.add_token(TokenType::VARIABLE, self.syntax().into());
    }
}

impl AppendSemanticTokens for ast::Value {
    fn append_semantic_tokens(&self, builder: &mut SemanticTokensBuilder) {
        for comment in self.leading_comments() {
            builder.add_token(TokenType::COMMENT, comment.syntax().into());
        }

        match self {
            Self::BasicString(n) => {
                builder.add_token(TokenType::STRING, (&n.token().unwrap()).into())
            }
            Self::LiteralString(n) => {
                builder.add_token(TokenType::STRING, (&n.token().unwrap()).into())
            }
            Self::MultiLineBasicString(n) => {
                builder.add_token(TokenType::STRING, (&n.token().unwrap()).into())
            }
            Self::MultiLineLiteralString(n) => {
                builder.add_token(TokenType::STRING, (&n.token().unwrap()).into())
            }
            Self::IntegerBin(n) => {
                builder.add_token(TokenType::NUMBER, (&n.token().unwrap()).into())
            }
            Self::IntegerOct(n) => {
                builder.add_token(TokenType::NUMBER, (&n.token().unwrap()).into())
            }
            Self::IntegerDec(n) => {
                builder.add_token(TokenType::NUMBER, (&n.token().unwrap()).into())
            }
            Self::IntegerHex(n) => {
                builder.add_token(TokenType::NUMBER, (&n.token().unwrap()).into())
            }
            Self::Float(n) => builder.add_token(TokenType::NUMBER, (&n.token().unwrap()).into()),
            Self::Boolean(n) => builder.add_token(TokenType::BOOLEAN, (&n.token().unwrap()).into()),
            Self::OffsetDateTime(n) => {
                builder.add_token(TokenType::DATETIME, (&n.token().unwrap()).into())
            }
            Self::LocalDateTime(n) => {
                builder.add_token(TokenType::DATETIME, (&n.token().unwrap()).into())
            }
            Self::LocalDate(n) => {
                builder.add_token(TokenType::DATETIME, (&n.token().unwrap()).into())
            }
            Self::LocalTime(n) => {
                builder.add_token(TokenType::DATETIME, (&n.token().unwrap()).into())
            }
            Self::Array(array) => array.append_semantic_tokens(builder),
            Self::InlineTable(inline_table) => inline_table.append_semantic_tokens(builder),
        }

        if let Some(comment) = self.tailing_comment() {
            builder.add_token(TokenType::COMMENT, comment.syntax().into())
        }
    }
}

impl AppendSemanticTokens for ast::Array {
    fn append_semantic_tokens(&self, builder: &mut SemanticTokensBuilder) {
        for comment in self.inner_begin_dangling_comments() {
            builder.add_token(TokenType::COMMENT, comment.syntax().into());
        }

        for (value, comma) in self.values_with_comma() {
            value.append_semantic_tokens(builder);
            if let Some(comma) = comma {
                for comment in comma.leading_comments() {
                    builder.add_token(TokenType::COMMENT, comment.syntax().into());
                }

                if let Some(comment) = comma.tailing_comment() {
                    builder.add_token(TokenType::COMMENT, comment.syntax().into())
                }
            }
        }

        for comment in self.inner_end_dangling_comments() {
            builder.add_token(TokenType::COMMENT, comment.syntax().into());
        }
    }
}

impl AppendSemanticTokens for ast::InlineTable {
    fn append_semantic_tokens(&self, builder: &mut SemanticTokensBuilder) {
        for comment in self.inner_begin_dangling_comments() {
            builder.add_token(TokenType::COMMENT, comment.syntax().into());
        }

        for (key_value, comma) in self.key_values_with_comma() {
            key_value.append_semantic_tokens(builder);
            if let Some(comma) = comma {
                for comment in comma.leading_comments() {
                    builder.add_token(TokenType::COMMENT, comment.syntax().into());
                }

                if let Some(comment) = comma.tailing_comment() {
                    builder.add_token(TokenType::COMMENT, comment.syntax().into())
                }
            }
        }

        for comment in self.inner_end_dangling_comments() {
            builder.add_token(TokenType::COMMENT, comment.syntax().into());
        }
    }
}

struct SemanticTokensBuilder<'a> {
    tokens: Vec<SemanticToken>,
    last_range: Range,
    source: &'a str,
}

impl<'a> SemanticTokensBuilder<'a> {
    fn new(source: &'a str) -> Self {
        Self {
            tokens: Vec::new(),
            last_range: Range::default(),
            source,
        }
    }

    fn add_token(&mut self, token_type: TokenType, node: TokenOrNode) {
        let range = Range::new(
            text::Position::from_source(self.source, node.text_span().start()).into(),
            text::Position::from_source(self.source, node.text_span().end()).into(),
        );

        let relative = relative_range(range, self.last_range);

        #[allow(clippy::cast_possible_truncation)]
        self.tokens.push(SemanticToken {
            delta_line: relative.start.line as u32,
            delta_start: relative.start.character as u32,
            length: (relative.end.character - relative.start.character) as u32,
            token_type: token_type as u32,
            token_modifiers_bitset: 0,
        });

        self.last_range = range;
    }

    fn build(self) -> Vec<SemanticToken> {
        self.tokens
    }
}

enum TokenOrNode<'a> {
    Token(&'a SyntaxToken),
    Node(&'a SyntaxNode),
}

impl<'a> TokenOrNode<'a> {
    fn text_span(&self) -> Span {
        match self {
            Self::Token(token) => token.text_span(),
            Self::Node(node) => node.text_span(),
        }
    }
}

impl<'a> From<&'a SyntaxToken> for TokenOrNode<'a> {
    fn from(token: &'a SyntaxToken) -> Self {
        Self::Token(token)
    }
}

impl<'a> From<&'a SyntaxNode> for TokenOrNode<'a> {
    fn from(node: &'a SyntaxNode) -> Self {
        Self::Node(node)
    }
}

fn relative_position(position: Position, to: Position) -> Position {
    if position.line == to.line {
        Position {
            line: 0,
            character: position.character - to.character,
        }
    } else {
        Position {
            line: position.line - to.line,
            character: position.character,
        }
    }
}

fn relative_range(from: Range, to: Range) -> Range {
    let line_diff = from.end.line - from.start.line;
    let start = relative_position(from.start, to.start);

    let end = if line_diff == 0 {
        Position {
            line: start.line,
            character: start.character + from.end.character - from.start.character,
        }
    } else {
        Position {
            line: start.line + line_diff,
            character: from.end.character,
        }
    };

    Range { start, end }
}
