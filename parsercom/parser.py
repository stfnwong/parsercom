"""
PARSER
Base class for parsers


Stefan Wong 2020
"""
import copy
from typing import List
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
        self.data:List[Tuple[int, str]] = list()
        if elem is not None:
            self.add(idx, elem)

    def __repr__(self) -> str:
        return 'ParseResult %s' % str(self.data)

    def __str__(self) -> str:
        return self.__repr__()

    def __len__(self) -> int:
        return len(self.data)

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

    def empty(self) -> bool:
        return True if len(self.data) == 0 else False


class Parser:
    """
    Base class for parsers. Provides __call__ signature.
    """
    def __init__(self, target:str, **kwargs) -> None:
        self.target = target

    def __repr__(self) -> str:
        return 'Parser'

    def __str__(self) -> str:
        return self.__repr__()

    def __call__(self, inp:str, parse_inp:ParseResult=None, idx:int=0) -> ParseResult:
        raise NotImplementedError('This should be implemented in derived class')


class NullParser(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return 'NullParser'

    def __call__(self, inp:str, parse_inp:ParseResult=None, idx:int=0) -> ParseResult:
        return ParseResult()


class EmptyParser(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return 'EmptyParser'

    def __call__(self, inp:str, parse_inp:ParseResult=None, idx:int=0) -> ParseResult:
        if parse_inp is not None:
            parse_out = copy.deepcopy(parse_inp)
            parse_out.add(idx, '')
            return parse_out

        return ParseResult(idx=idx, elem='')


class CharParser(Parser):
    def __init__(self, target_char:str) -> None:
        self.target_char = target_char

    def __repr__(self) -> str:
        return 'CharParser(\'%s\')' % self.target_char

    def __call__(self, inp:str, parse_inp:ParseResult=None, idx:int=0) -> ParseResult:
        if parse_inp is not None:
            idx = parse_inp.last_idx()

        parse_result = ParseResult()
        # Try to match one char
        if idx >= len(inp):
            return parse_inp if parse_inp is not None else parse_result

        if inp[idx] == self.target_char:
            parse_result.add(idx + 1, inp[idx])

        if parse_inp is not None:
            parse_out = copy.deepcopy(parse_inp)
            parse_out.extend(parse_result)
            return parse_out

        return parse_result

    def get_target(self) -> str:
        return self.target_char


class StringParser(Parser):
    """
    StringParser
    """
    def __init__(self, target_str:str) -> None:
        self.target_str = target_str

    def __repr__(self) -> str:
        return 'StringParser(\'%s\')' % self.target_str

    def __call__(self, inp:str, parse_inp:ParseResult=None, idx:int=0) -> ParseResult:
        if parse_inp is not None:
            idx = parse_inp.last_idx()
            start_idx = parse_inp.last_idx()
        else:
            start_idx = 0

        parse_result = ParseResult()
        if idx >= len(inp):
            return parse_result

        for target_idx, c in enumerate(inp[idx:]):
            if target_idx >= len(self.target_str):
                return parse_result
            if self.target_str[target_idx] != c:
                return parse_result
            # dont eval the rest of the string if we have partial match
            if target_idx == len(self.target_str)-1:
                break

        if target_idx < len(self.target_str)-1:
            return parse_result     # didnt match enough chars

        parse_result.add(idx + target_idx+1, inp[start_idx : start_idx + target_idx+1])

        return parse_result

    def get_target(self) -> str:
        return self.target_str
