from codemod_json import parse_str, item


def test_parse():
    # assert parse_str("1.") == 1.0
    assert parse_str("-1.0")._root == -1.0
    assert parse_str("1.23")._root == 1.23
    assert parse_str("2.99792458e8")._root == 2.99792458e8


# def test_special_parse():
#     assert parse_str("NaN") == float("nan")
#     assert parse_str("+Infinity") == float("+inf")
#     assert parse_str("-Infinity") == float("-inf")


def test_item_methods():
    assert item(1.0).to_string() == "1.0"
