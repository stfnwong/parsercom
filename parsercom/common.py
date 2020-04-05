"""
COMMON
Grab bag of recurring things. To be refactored.

Stefan Wong 2020
"""

from typing import Any
from typing import Tuple


class ParseResult:
    def __init__(self, elem:Any=None, idx:int=0) -> None:
        self.data:Tuple[int, Any] = list()

        if elem is not None:
            self.add(elem, idx)

    def __repr__(self) -> str:
        return 'ParseResult'

    def __str__(self) -> str:
        return '%s %s' % (repr(self), str(self.data))

    def __eq__(self, other:'ParseResult') -> bool:
        if isinstance(other, ParseResult):
            if len(self.data) != len(other.data):
                return False

            # check that all the other combinations are in
            # the set
            # TODO : should really be a set and not a list...
            for ours, theirs in zip(self.data, other.data):
                if ours != theirs:
                    return False

            return True
        else:        # comparison with any other type makes no sense
            return False

    def add(self, elem:Any=None, idx:int=0) -> None:
        new_elem = (idx, elem)
        self.data.append(new_elem)
