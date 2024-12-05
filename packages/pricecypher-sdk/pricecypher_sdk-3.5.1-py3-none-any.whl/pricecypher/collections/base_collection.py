from abc import ABCMeta
from collections.abc import Sequence
from typing import TypeVar

T = TypeVar('T')


class Collection(Sequence[T], metaclass=ABCMeta):
    def __init__(self, items):
        self._list = list(items)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self._list}>"

    def __len__(self) -> int:
        """List length"""
        return len(self._list)

    def __getitem__(self, ii) -> T:
        """Get a list item"""
        return self._list[ii]

    def __str__(self) -> str:
        return str(self._list)

    def pluck(self, prop):
        """
        Get a list with the values of the given prop.

        :param str prop: Property to pluck from the scope values.
        :return:
        """
        return [getattr(v, prop) for v in self._list]

    def where(self, prop, value) -> 'Collection[T]':
        filtered = [v for v in self._list if getattr(v, prop) == value]
        return type(self)(filtered)
