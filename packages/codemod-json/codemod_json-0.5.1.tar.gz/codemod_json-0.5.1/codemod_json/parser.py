from __future__ import annotations

from dataclasses import dataclass
from itertools import count
from logging import getLogger
from typing import Optional

from tree_sitter import Language, Parser, Tree
from tree_sitter_json import language as json_language

from .base import Item, JsonStream
from .items import item

logger = getLogger(__name__)
parser = Parser(Language(json_language()))

COOKIE_GENERATOR = count(1)

# These constants need to sort a certain way, and are applied from higher
# numbers downward.
CHANGE = 1
DELETE = 2


class ParseError(Exception):
    pass


@dataclass(order=True)
class PendingEdit:
    start: int
    end: int
    action: int
    cookie: int
    item: Optional[Item] = None


class ContainerJsonStream(JsonStream):
    def __init__(self, tree: Tree, original_bytes: bytes) -> None:
        super().__init__(tree, original_bytes)
        self._root: Item = self._get_root()
        self._edits: dict[int, PendingEdit] = {}

    def _get_root(self) -> Item:
        assert self._tree.root_node.type == "document"
        return item(node=self._tree.root_node.children[0], stream=self)

    # Private API for editing

    def cancel_cookie(self, cookie: int) -> None:
        self._edits.pop(cookie, None)

    def edit(self, item: Item, new_item: Optional[Item]) -> int:
        """
        Changes `item` (read from json) to `new_item` (a boxed python object).

        If `new_item` is None, it is a deletion.
        Otherwise, it is a swap.

        If there have been prior edits recorded in the same span, they are cancelled
        first.  This is necessary for code like:

        ```
        x["a"]["b"] = 1
        x["a"] = {}
        ```

        Edits are not actually resolved until you access `.text`.
        """
        cookie = next(COOKIE_GENERATOR)
        start = item.start_byte
        end = item.end_byte
        # print("EDIT", cookie, item, start, end, self._original_bytes[start:end])
        if new_item is None:
            self._remove_wholly_contained_edits(start, end)
            self._edits[cookie] = PendingEdit(start, end, DELETE, cookie, None)
        else:
            self._remove_wholly_contained_edits(start, end)
            self._edits[cookie] = PendingEdit(start, end, CHANGE, cookie, new_item)
        return cookie

    def _remove_wholly_contained_edits(self, start: int, end: int) -> None:
        # print(start, end, self._edits)
        overlapped_cookies: set[int] = set()
        for k, v in self._edits.items():
            if v.start >= start and v.end <= end:
                overlapped_cookies.add(k)

        for k in overlapped_cookies:
            del self._edits[k]

    @property
    def text(self) -> bytes:
        tmp = self._original_bytes

        for edit in sorted(self._edits.values(), reverse=True):
            if edit.item is not None:
                new_bytes = edit.item.to_string().encode("utf-8")
            else:
                new_bytes = b""
            logger.debug(
                "Apply edit: %r->%r @ %r",
                tmp[edit.start : edit.end],
                new_bytes,
                edit,
            )
            tmp = tmp[: edit.start] + new_bytes + tmp[edit.end :]
            # TODO restore tree-sitter edits if we can come up with the line/col values
            # self._tree.edit(edit.start, edit.end, edit.start + len(new_bytes), (0, 0), (0, 0))
        logger.debug("New text: %r", tmp)
        # TODO restore this as verification we made valid edits
        # assert parser.parse(tmp, old_tree=self._tree).root_node.text == tmp
        return tmp


def parse_str(data: str) -> JsonStream:
    original_bytes = data.encode("utf-8")
    return parse(original_bytes)


def parse(data: bytes) -> JsonStream:
    # print(type(data))
    return ContainerJsonStream(tree=parser.parse(data), original_bytes=data)
