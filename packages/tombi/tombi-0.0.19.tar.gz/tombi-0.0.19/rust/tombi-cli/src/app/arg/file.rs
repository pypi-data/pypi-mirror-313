use std::path::PathBuf;

/// Input source for TOML files.
///
/// Standard input or file paths. Contains a list of files that match the glob pattern.
#[derive(Debug)]
pub enum FileInput {
    Stdin,
    Files(Vec<Result<PathBuf, crate::Error>>),
}

impl FileInput {
    pub fn len(&self) -> usize {
        match self {
            FileInput::Stdin => 1,
            FileInput::Files(files) => files.len(),
        }
    }
}

impl<T> From<&[T]> for FileInput
where
    T: AsRef<str>,
{
    fn from(files: &[T]) -> Self {
        match files.len() {
            0 => {
                FileInput::Files(
                    glob::glob("**/*.toml")
                        .unwrap() // No Probrem. grob pattern is const.
                        .filter_map(|x| Result::<_, crate::Error>::Ok(x.ok()).transpose())
                        .collect::<Vec<_>>(),
                )
            }
            1 if files[0].as_ref() == "-" => FileInput::Stdin,
            _ => {
                let mut results: Vec<Result<PathBuf, crate::Error>> = vec![];
                for file in files {
                    if is_glob_pattern(file.as_ref()) {
                        if let Ok(paths) = glob::glob(file.as_ref()) {
                            results.extend(
                                paths
                                    .filter_map(|x| {
                                        Result::<_, crate::Error>::Ok(x.ok()).transpose()
                                    })
                                    .collect::<Vec<_>>(),
                            );
                        } else {
                            results
                                .push(Err(crate::Error::GlobPatternInvalid(file.as_ref().into())));
                        };
                    } else {
                        let path = PathBuf::from(file.as_ref());
                        if !path.exists() {
                            results.push(Err(crate::Error::FileNotFound(file.as_ref().into())));
                        } else {
                            results.push(Ok(path));
                        }
                    }
                }
                FileInput::Files(results)
            }
        }
    }
}

fn is_glob_pattern(value: &str) -> bool {
    value.contains('*') || value.contains('?') || value.contains('[') || value.contains(']')
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn std_input() {
        let input = vec!["-"];
        let file_input = FileInput::from(input.as_ref());
        assert!(matches!(file_input, FileInput::Stdin));
    }

    #[test]
    fn single_file() {
        let input = vec!["Cargo.toml"];
        let file_input = FileInput::from(input.as_ref());
        assert!(matches!(file_input, FileInput::Files(_)));
    }

    #[test]
    fn glob_file() {
        let input = vec!["**/Cargo.toml"];
        let file_input = FileInput::from(input.as_ref());
        assert!(matches!(file_input, FileInput::Files(_)));
    }
}
