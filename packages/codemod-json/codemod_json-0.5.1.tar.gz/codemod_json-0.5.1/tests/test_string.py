from codemod_json import parse_str, item


def test_parse():
    assert parse_str('"abc"')._root == "abc"
    assert parse_str('"abc\\u0001"')._root == "abc\x01"


def test_to_string():
    assert item("abc\u0001").to_string() == '"abc\\u0001"'
