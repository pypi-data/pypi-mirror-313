from codemod_json import parse_str, item


def test_parse():
    assert parse_str("null")._root == None


def test_item_methods():
    assert item(None).to_string() == "null"
    assert hash(item(None)) == hash(item(None))
    assert item(None) == item(None)
