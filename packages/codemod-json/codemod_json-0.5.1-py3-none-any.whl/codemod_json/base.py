from __future__ import annotations

import abc

from typing import Any, Optional

from tree_sitter import Node, Tree


class JsonStream(abc.ABC):
    _root: Item

    def __init__(self, tree: Tree, original_bytes: bytes):
        self._tree = tree
        self._original_bytes = original_bytes

    @abc.abstractmethod
    def cancel_cookie(self, cookie: int) -> None:
        pass

    @abc.abstractmethod
    def edit(self, item: Item, new_item: Optional[Item]) -> int:
        pass

    # Forwarding methods

    def __contains__(self, value: Any) -> bool:
        assert isinstance(self._root, (list, dict))
        return value in self._root

    def __getitem__(self, key: Any) -> Any:
        assert isinstance(self._root, (list, dict))
        return self._root[key]

    def __setitem__(self, key: Any, value: Any) -> None:
        assert isinstance(self._root, (list, dict))
        self._root[key] = value

    def __delitem__(self, key: Any) -> None:
        assert isinstance(self._root, (list, dict))
        del self._root[key]

    def append(self, other: Any) -> None:
        assert isinstance(self._root, list)
        self._root.append(other)


class Item(abc.ABC):
    """
    An `Item` is a dual-nature box -- it can wrap a `tree_sitter.Node` or just a python object.

    The specialized subclass should inherit from the python base type, which is why there isn't a
    `value` or so in the `__init__` here.  See `Integer` for a good example of this.  Scalars like
    keys are eagerly boxed for simplicity, but values should be done lazily where possible.
    """

    _original: Optional[Node] = None

    def __init__(
        self,
        original: Optional[Node],
        stream: Optional[JsonStream],
        annealed: bool = False,
    ):
        self._original = original
        self._stream = stream
        self._annealed = original is None

    @property
    def start_byte(self) -> int:
        assert self._original is not None
        return self._original.start_byte

    @property
    def end_byte(self) -> int:
        assert self._original is not None
        assert self._stream is not None
        t = self._original
        while t.next_sibling and t.next_sibling.type in (",", "comment"):
            t = t.next_sibling

        e = t.end_byte
        while self._stream._original_bytes[e : e + 1] in (b" ", b"\n"):
            e += 1

        return e

    @classmethod
    @abc.abstractmethod
    def from_json(cls, node: Node, stream: JsonStream) -> "Item":
        pass

    def anneal(self, initial: bool = True) -> None:
        if self._annealed:
            return

        if initial and self._original and self._stream:
            self._stream.edit(self, self)

        self._annealed = True

    @abc.abstractmethod
    def to_string(self) -> str:
        pass
