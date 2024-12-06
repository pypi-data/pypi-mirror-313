from codemod_json import parse_str, item


def test_parse():
    assert parse_str("true")._root == True
    assert parse_str("false")._root == False


def test_item_methods():
    assert item(True).to_string() == "true"
    assert item(False).to_string() == "false"
    assert hash(item(True)) == hash(item(True))
    assert item(True) == item(True)
    assert item(True)
    assert not item(False)
    assert int(item(True)) == 1
    assert item(True) == 1
    assert item(True) != 2
    assert item(False) == 0
