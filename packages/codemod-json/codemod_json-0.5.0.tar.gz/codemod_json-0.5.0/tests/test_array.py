from codemod_json import parse_str


def test_addition():
    doc = parse_str("[1,2,3]")
    doc._root.append(4)
    assert doc.text.decode("utf-8") == "[1, 2, 3, 4]"


def test_addition_discards_comments():
    doc = parse_str("[1,2,\n//foo\n3] // bar")
    doc._root.append(4)
    assert doc.text.decode("utf-8") == "[1, 2, 3, 4]"


def test_array_assignment():
    doc = parse_str("[1]//foo")
    doc[0] = 99
    assert doc.text.decode("utf-8") == "[99]//foo"


def test_array_nesting():
    doc = parse_str("[1//foo\n//bar\n]")
    doc[0] = [1, 2, 3]
    assert doc.text.decode("utf-8") == "[[1, 2, 3]]"


def test_array_delete():
    doc = parse_str("[1,2,3]")
    del doc[1]
    assert doc.text.decode("utf-8") == "[1, 3]"


def test_array_delete_last():
    doc = parse_str("[1,2,3]")
    del doc[2]
    assert doc.text.decode("utf-8") == "[1, 2]"


def test_array_slice_assign():
    doc = parse_str("[1,2,3]")
    doc[:] = ["a"]
    assert doc.text.decode("utf-8") == '["a"]'


def test_array_del_one_at_a_time():
    doc = parse_str("[1,2,3]")
    while doc._root:
        del doc._root[0]
    assert doc.text.decode("utf-8") == "[]"
