from codemod_json import parse_str


def test_basics():
    assert parse_str("true")._root == True
    assert parse_str("2")._root == 2
    assert parse_str("-1")._root == -1
    assert parse_str("1.2")._root == 1.2
    assert parse_str("2.99792458e8")._root == 2.99792458e8
    assert parse_str('"x"')._root == "x"
    assert parse_str("[1,2,3]")._root == [1, 2, 3]
    assert parse_str('{"x": "y"}')["x"] == "y"
