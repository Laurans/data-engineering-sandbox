from data_engineering_sandbox.string_utils import sanitize_sql_identifier


def test_sanitize_sql_identifier_keyword():
    input_string = "INSERT"
    sanitized_string = sanitize_sql_identifier(input_string)
    assert sanitized_string == "insert_"


def test_sanitize_sql_identifier_symbol():
    input_string = "Unnamed: 0"
    sanitized_string = sanitize_sql_identifier(input_string)
    assert sanitized_string == "unnamed0"
