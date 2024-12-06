mod format;
pub mod formatter;

pub use config::FormatOptions;
use config::TomlVersion;
use diagnostic::Diagnostic;
use format::Format;
pub use formatter::definitions::Definitions;
pub use formatter::Formatter;

pub fn format(source: &str) -> Result<String, Vec<Diagnostic>> {
    format_with(source, TomlVersion::default(), &FormatOptions::default())
}

pub fn format_with(
    source: &str,
    toml_version: TomlVersion,
    options: &FormatOptions,
) -> Result<String, Vec<Diagnostic>> {
    match parser::parse(source, toml_version).try_cast::<ast::Root>() {
        Ok(root) => {
            tracing::trace!("ast: {:#?}", root);

            let mut formatted_text = String::new();
            let line_ending = {
                let mut f = Formatter::new_with_options(toml_version, &mut formatted_text, options);
                root.fmt(&mut f).unwrap();
                f.line_ending()
            };

            Ok(formatted_text + line_ending)
        }
        Err(errors) => Err(errors
            .into_iter()
            .map(|error| Diagnostic::new_error(error.message(), error.range()))
            .collect()),
    }
}

#[cfg(test)]
#[macro_export]
macro_rules! test_format {
    (#[test] fn $name:ident($source:expr) -> Ok(source);) => {
        crate::test_format!(#[test] fn $name($source) -> Ok($source););
    };

    (#[test] fn $name:ident($source:expr, $version:expr) -> Ok(source);) => {
        crate::test_format!(#[test] fn $name($source, $version) -> Ok($source););
    };

    (#[test] fn $name:ident($source:expr) -> Ok($expected:expr);) => {
        crate::test_format!(#[test] fn $name($source, Default::default()) -> Ok($expected););
    };

    (#[test] fn $name:ident($source:expr, $version:expr) -> Ok($expected:expr);) => {
        #[test]
        fn $name() {
            match crate::format_with($source, $version, &crate::FormatOptions::default()) {
                Ok(formatted_text) => {
                    pretty_assertions::assert_eq!(formatted_text, textwrap::dedent($expected).trim().to_string() + "\n");
                }
                Err(errors) => {
                    pretty_assertions::assert_eq!(errors, vec![]);
                }
            }
        }
    };

    (#[test] fn $name:ident($source:expr) -> Err(_);) => {
        #[test]
        fn $name() {
            match crate::format($source) {
                Ok(_) => panic!("expected an error"),
                Err(errors) => {
                    pretty_assertions::assert_ne!(errors, vec![]);
                }
            }
        }
    };
}

#[cfg(test)]
mod test {
    use super::*;

    test_format! {
        #[test] fn test_key_values(r#"
            array5 = [
              1,
              {
                # inline begin dangling comment1
                # inline begin dangling comment2

                # key1 leading comment1
                # key1 leading comment2
                key1 = 1,  # key1 tailing comment
                # key2 leading comment1
                key2 = 2,  # key2 tailing comment

                # inline end dangling comment1
                # inline end dangling comment2
              },

              # comment
            ]
            "#,
            TomlVersion::V1_1_0_Preview
        ) -> Ok(source);
    }

    test_format! {
    #[test] fn test_sample_toml(
r#"
# begin dangling comment1
# begin dangling comment2

# table leading comment1
# table leading comment2
[aaaa]
# table leading comment1
# table leading comment2
[aaaa.bbb]
bool1 = true
bool2 = false
dec = 1  # dec tailing comment
bin = 0b01  # bin tailing comment
oct = 0o01  # oct tailing comment
hex = 0x01  # hex tailing comment
float1 = 0.1234  # float tailing comment
infa = inf
bs = "2"  # bs tailing comment
ls = '3'  # ls tailing comment
array1 = [
  # array begin dangling comment1
  # array begin dangling comment2

  # value1 leading comment1
  # value1 leading comment2
  # value1 leading comment3
  { key3 = 12, key4 = 2024-01-01T10:10:00 }
  # value1 comma leading comment1
  # value1 comma leading comment2
  # value1 comma leading comment3
  ,  # value1 comma tailing comment
  { key3 = 11, key4 = 2024-01-01T10:10:00 },

  # array end dangling comment1
  # array end dangling comment2
]  # array tailing comment
array2 = [1, 2, 3]
array3 = [
  1,
  2,
  3,
]
array4 = [
  [
    1,
    2,
    3,
  ],
  [1, 2, 3],
]
array5 = [
  1,
  {
    # inline begin dangling comment1
    # inline begin dangling comment2

    # key1 leading comment1
    # key1 leading comment2
    key1 = 1,  # key1 tailing comment
    # key2 leading comment1
    key2 = 2,  # key2 tailing comment

    # inline end dangling comment1
    # inline end dangling comment2
  },

  # comment
]
date = 2024-01-01  # date tailing comment
time = 10:11:00  # time tailing comment
odt1 = 1979-05-27T07:32:00Z  # odt1 tailing comment
odt2 = 1979-05-27T00:32:00-07:00  # odt2 tailing comment
odt3 = 1979-05-27T00:32:00.999999-07:00  # odt3 tailing comment
odt4 = 1979-05-27T07:32:00Z  # odt4 tailing comment
ldt1 = 1979-05-27T07:32:00  # ldt1 tailing comment
ldt2 = 1979-05-27T00:32:00.999999  # ldt2 tailing comment
ld1 = 1979-05-27  # ld1 tailing comment
lt1 = 07:32:00  # lt1 tailing comment
# lt2 leading tailing comment
lt2 = 00:32:00.999999  # lt2 tailing comment

[aaaa.ccc]
key1 = 11
key2 = "22"

[bbb]
key5 = true

[ddd.eee]  # header tailing comment
key5 = true

[[ffff.ggg]]
key6 = 1

[[ffff.ggg]]
key6 = 2

[[ffff.ggg]]  # header tailing comment
# key value leading comment1
# key value leading comment2
key6 = 3  # key value tailing comment

# end dangling comment1
# end dangling comment2
"#,
    TomlVersion::V1_1_0_Preview)
        -> Ok(source);
    }
}
