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
    That is, we don't want to keep making copies of the string all
    the time in order to make the ParseResult self contained.

    We want to be able to give ParseResults from previous parsers/steps
    to subsequent parsers/steps and have them continue on in some way.
"""
class ParseResult:
    """
    Holds the result of a parse operation.
    """
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

    def update(self, idx:int=0, elem:str=None) -> None:
        if elem is None:
            self.data[-1] = (idx, '')
        else:
            self.data[-1] = (idx, self.data[-1][1] + elem)

    def extend(self, result:'ParseResult') -> None:
        self.data.extend(result.data)

    def last_idx(self) -> int:
        try:
            return self.data[-1][0]
        except:
            return 0

    def last_str(self) -> str:
        try:
            return self.data[-1][1]
        except:
            return ''

    def empty(self) -> bool:
        return True if len(self.data) == 0 else False


class Parser:
    """
    Base class for parsers. Provides __call__ signature.
    """
    def __repr__(self) -> str:
        return 'Parser'

    def __str__(self) -> str:
        return self.__repr__()

    def __call__(self, inp:str, parse_inp:ParseResult=None, idx:int=0) -> ParseResult:
        raise NotImplementedError('This should be implemented in derived class')


class NullParser(Parser):
    def __repr__(self) -> str:
        return 'NullParser'

    def __call__(self, inp:str, parse_inp:ParseResult=None, idx:int=0) -> ParseResult:
        return ParseResult()


class EmptyParser(Parser):
    def __repr__(self) -> str:
        return 'EmptyParser'

    def __call__(self, inp:str, parse_inp:ParseResult=None, idx:int=0) -> ParseResult:
        if parse_inp is not None:
            parse_out = copy.deepcopy(parse_inp)
            parse_out.add(parse_inp.last_idx(), '')
            return parse_out

        return ParseResult(idx=idx, elem='')



class AlphaParser(Parser):
    """
    AlphaParser
    Parses any ASCII character
    """
    def __repr__(self) -> str:
        return 'AlphaParser'

    def __call__(self, inp:str, parse_inp:ParseResult=None, idx:int=0) -> ParseResult:
        if parse_inp is not None:
            idx = parse_inp.last_idx()

        if idx < len(inp):
            if inp[idx].isalpha():
                if parse_inp is not None:
                    parse_out = copy.deepcopy(parse_inp)
                else:
                    parse_out = ParseResult()
                parse_out.add(idx+1, inp[idx])

                return parse_out

        return ParseResult()


class AlphaSpaceParser(Parser):
    """
    AlphaSpaceParser
    Parses any ASCII character or space
    """
    def __repr__(self) -> str:
        return 'AlphaSpaceParser'

    def __call__(self, inp:str, parse_inp:ParseResult=None, idx:int=0) -> ParseResult:
        if parse_inp is not None:
            idx = parse_inp.last_idx()

        if idx < len(inp):
            if inp[idx].isalpha() or inp[idx].isspace():
                if parse_inp is not None:
                    parse_out = copy.deepcopy(parse_inp)
                else:
                    parse_out = ParseResult()
                parse_out.add(idx+1, inp[idx])

                return parse_out

        return ParseResult()


class NumParser(Parser):
    """
    NumParser
    Parses any number
    """
    def __repr__(self) -> str:
        return 'NumParser'

    def __call__(self, inp:str, parse_inp:ParseResult=None, idx:int=0) -> ParseResult:
        if parse_inp is not None:
            idx = parse_inp.last_idx()

        if idx < len(inp):
            if inp[idx].isdigit():
                if parse_inp is not None:
                    parse_out = copy.deepcopy(parse_inp)
                else:
                    parse_out = ParseResult()
                parse_out.add(idx+1, inp[idx])

                return parse_out

        #if parse_inp is not None:
        #    return copy.deepcopy(parse_inp)

        return ParseResult()


class CharParser(Parser):
    """
    CharParser
    Parses any single character
    """
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
        else:
            parse_out = ParseResult()

        parse_out.extend(parse_result)
        return parse_out

    def get_target(self) -> str:
        return self.target_char


class StringParser(Parser):
    """
    StringParser
    Parses a given string"
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



# KleeneDot for characters
class OneOrMore(Parser):
    def __repr__(self) -> str:
        return "OneOrMore()"

    def __call__(self, inp:str, parse_inp:ParseResult=None, idx:int=0) -> ParseResult:
        if parse_inp is not None:
            idx = parse_inp.last_idx()
        else:
            idx = 0

        parse_result = ParseResult()
        target_idx = 0
        for target_idx, c in enumerate(inp[idx:]):
            if not c.isalnum() and not c.isspace():
                break

        if target_idx == 0:
            return parse_result

        parse_result.add(idx + target_idx + 1, inp[idx : idx + target_idx+1])

        return parse_result


# KleeneStar for characters
class ZeroOrMore(Parser):
    def __repr__(self) -> str:
        return "ZeroOrMore()"

    def __call__(self, inp:str, parse_inp:ParseResult=None, idx:int=0) -> ParseResult:
        if parse_inp is not None:
            idx = parse_inp.last_idx()
        else:
            idx = 0

        parse_result = ParseResult()
        target_idx = 0
        for target_idx, c in enumerate(inp[idx:]):
            if not c.isalnum() and not c.isspace():
                break

        parse_result.add(idx + target_idx + 1, inp[idx : idx + target_idx+1])

        return parse_result
