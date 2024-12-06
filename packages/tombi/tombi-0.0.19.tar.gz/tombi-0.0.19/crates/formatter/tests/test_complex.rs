use assert_matches::assert_matches;

#[test]
fn test_key_values() {
    let source = r#"
key = "value"
bare_key = "value"
bare-key = "value"
1234 = "value"
"#
    .trim_start()
    .to_string();

    let result = formatter::format(&source);

    assert_matches!(result, Ok(_));
    assert_eq!(result.unwrap(), source);
}
