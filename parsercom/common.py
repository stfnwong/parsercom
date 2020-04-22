"""
COMMON
Grab bag of recurring things. To be refactored.

Stefan Wong 2020
"""

from typing import List
from typing import Set
from typing import Tuple


"""
NOTES:
    rather than return some tuple like (status, chars_left) we should
    replace chars_left with an index to where in the stream to find the
    next set of chars. The ParseResult is just the result of parsing.
    That is to say we don't want to keep making copies of the string all
    the time in order to make the ParseResult self contained.

    We want to be able to give ParseResults from previous parsers/steps
    to subsequent parsers/steps and have them continue on in some way.
"""
class ParseResult:
    def __init__(self, idx:int=0, elem:str=None) -> None:
        self.data:List[Tuple[str, int]] = list()
        if elem is not None:
            self.add(idx, elem)

    def __repr__(self) -> str:
        return 'ParseResult %s' % str(self.data)

    def __str__(self) -> str:
        return self.__repr__()

    def __eq__(self, other:object) -> bool:
        if isinstance(other, ParseResult):
            if len(self.data) != len(other.data):
                return False

            for ours, theirs in zip(self.data, other.data):
                if ours != theirs:
                    return False

            return True
        else:        # comparison with any other type makes no sense
            return False

    def add(self, idx:int=0, elem:str=None) -> None:
        if elem is None:
            new_elem = (idx, '')
        else:
            new_elem = (idx, elem)
        self.data.append(new_elem)

    def extend(self, result:'ParseResult') -> None:
        self.data.extend(result.data)

    def last_idx(self) -> int:
        try:
            return self.data[-1][0]
        except:
            return 0
