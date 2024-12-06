mod builder;
mod error;
mod event;
mod input;
mod lexed;
mod marker;
mod output;
mod parse;
mod parsed;
mod parser;
mod token_set;

use config::TomlVersion;
pub use error::{Error, ErrorKind};
pub use event::Event;
use lexed::lex;
pub use lexed::LexedStr;
use output::Output;
use parse::Parse;
use parsed::Parsed;
pub use syntax::{SyntaxKind, SyntaxNode, SyntaxToken};

pub fn parse(source: &str, toml_version: TomlVersion) -> Parsed<SyntaxNode> {
    parse_as::<ast::Root>(source, toml_version)
}

#[allow(private_bounds)]
pub fn parse_as<P: Parse>(source: &str, toml_version: TomlVersion) -> Parsed<SyntaxNode> {
    let lexed = lex(source);
    let input = lexed.to_input();
    let mut p = crate::parser::Parser::new(&input, toml_version);

    P::parse(&mut p);

    let events = p.finish();

    let output = crate::event::process(events);

    let (green_tree, errors) = build_green_tree(&lexed, output);

    Parsed::new(green_tree, errors)
}

pub fn build_green_tree(
    lexed: &LexedStr<'_>,
    parser_output: crate::Output,
) -> (rg_tree::GreenNode, Vec<crate::Error>) {
    let mut builder = syntax::SyntaxTreeBuilder::<crate::Error>::default();

    let _ = lexed.intersperse_trivia(&parser_output, &mut |step| match step {
        lexed::Step::AddToken { kind, text } => {
            builder.token(kind, text);
        }
        lexed::Step::StartNode { kind } => {
            builder.start_node(kind);
        }
        lexed::Step::FinishNode => builder.finish_node(),
        lexed::Step::Error { error } => builder.error(error),
    });

    builder.finish()
}

#[cfg(test)]
#[macro_export]
macro_rules! test_parser {
    {#[test] fn $name:ident($source:expr) -> Ok(_)} => {
        #[test]
        fn $name() {
            let p = crate::parse(textwrap::dedent($source).trim(), Default::default());

            assert_eq!(p.errors(), vec![])
        }
    };

    {#[test] fn $name:ident($source:expr, $toml_version:expr) -> Ok(_)} => {
        #[test]
        fn $name() {
            let p = crate::parse(textwrap::dedent($source).trim(), $toml_version);

            assert_eq!(p.errors(), vec![])
        }
    };

    {#[test] fn $name:ident($source:expr) -> Err(
        [
            $(
                SyntaxError(
                    $error_kind:ident,
                    $line1:literal:$column1:literal..$line2:literal:$column2:literal
                )
            ),*$(,)*
        ]
    )} => {
        crate::test_parser! {#[test] fn $name($source, Default::default()) -> Err([$(SyntaxError($error_kind, $line1:$column1..$line2:$column2)),*])}
    };

    {#[test] fn $name:ident($source:expr, $toml_version:expr) -> Err(
        [
            $(
                SyntaxError(
                    $error_kind:ident,
                    $line1:literal:$column1:literal..$line2:literal:$column2:literal
                )
            ),*$(,)*
        ]
    )} => {
        #[test]
        fn $name() {
            let p = crate::parse(textwrap::dedent($source).trim(), $toml_version);

            assert_eq!(p.errors(), vec![$(crate::Error::new($error_kind, (($line1, $column1), ($line2, $column2)).into())),*])
        }
    };
}
