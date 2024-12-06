use std::io::Read;

use config::{LintOptions, TomlVersion};
use diagnostic::{printer::Pretty, Diagnostic, Print};

use crate::app::arg;

/// Lint TOML files.
#[derive(clap::Args, Debug)]
pub struct Args {
    /// Paths or glob patterns to TOML documents.
    ///
    /// If the only argument is "-", the standard input is used.
    files: Vec<String>,

    /// TOML version.
    #[arg(long, value_enum, default_value = None)]
    toml_version: Option<TomlVersion>,
}

#[tracing::instrument(level = "debug", skip_all)]
pub fn run(args: Args) -> Result<(), crate::Error> {
    let (success_num, error_num) = inner_run(args, Pretty);

    match success_num {
        0 => eprintln!("No files linted"),
        1 => eprintln!("1 file linted"),
        _ => eprintln!("{} files linted", success_num),
    }

    if error_num > 0 {
        std::process::exit(1);
    }

    Ok(())
}

fn inner_run<P>(args: Args, printer: P) -> (usize, usize)
where
    Diagnostic: Print<P>,
    crate::Error: Print<P>,
    P: Copy,
{
    let input = arg::FileInput::from(args.files.as_ref());

    let total_num = input.len();
    let mut success_num = 0;
    let mut error_num = 0;

    let config = config::load();
    let toml_version = args
        .toml_version
        .unwrap_or(config.toml_version.unwrap_or_default());
    let options = config.lint.unwrap_or_default();

    match input {
        arg::FileInput::Stdin => {
            tracing::debug!("stdin input linting...");
            if lint_file(std::io::stdin(), printer, toml_version, &options) {
                success_num += 1;
            } else {
                error_num += 1;
            }
        }
        arg::FileInput::Files(files) => {
            for file in files {
                match file {
                    Ok(path) => {
                        tracing::debug!("{:?} linting...", path);
                        match std::fs::File::open(&path) {
                            Ok(file) => {
                                if lint_file(file, printer, toml_version, &options) {
                                    success_num += 1;
                                    continue;
                                }
                            }
                            Err(err) => {
                                if err.kind() == std::io::ErrorKind::NotFound {
                                    crate::Error::FileNotFound(path).print(printer);
                                } else {
                                    crate::Error::Io(err).print(printer);
                                }
                            }
                        }
                    }
                    Err(err) => err.print(printer),
                }
                error_num += 1;
            }
        }
    };

    assert_eq!(success_num + error_num, total_num);

    (success_num, error_num)
}

fn lint_file<R: Read, P>(
    mut reader: R,
    printer: P,
    toml_version: TomlVersion,
    options: &LintOptions,
) -> bool
where
    Diagnostic: Print<P>,
    crate::Error: Print<P>,
    P: Copy,
{
    let mut source = String::new();
    if reader.read_to_string(&mut source).is_ok() {
        match linter::lint_with(&source, toml_version, &options) {
            Ok(()) => {
                return true;
            }
            Err(diagnostics) => diagnostics.print(printer),
        }
    }
    false
}
