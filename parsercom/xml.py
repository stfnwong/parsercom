"""
XML
Parsers for XML

Stefan Wong 2020
"""
# TODO : note there is lots of boilerplate here...


from parsercom.parser import (
    ParseResult,
    Parser,
    AlphaSpaceParser,
    CharParser,
)
from parsercom.combinator import Combinator, KleeneStar, KleeneDot, ZeroOrMoreCombinator

# TODO : some of these are generic enough that they could be moved into the
# regular combinator implementation

# ======== PARSER ======== #
class WhiteSpace(Parser):
    """
    Zero or more whitespace characters
    """
    def __repr__(self) -> str:
        return "Whitespace()"

    def __call__(self, inp:str, parse_inp:ParseResult=None, idx:int=0) -> ParseResult:
        if parse_inp is not None:
            idx = parse_inp.last_idx()
        else:
            idx = 0

        parse_result = ParseResult()
        for target_idx, c in enumerate(inp[idx:]):
            if not c.isspace():
                break

        parse_result.add(idx + target_idx + 1, inp[idx : idx + target_idx+1])

        return parse_result


class Identifier(Parser):
    """
    Parser for an Identifier. Identifiers consist of one or more letters followed
    by any number of letters, numbers or hyphens.
    """
    def __repr__(self) -> str:
        return "Identifier()"

    def __call__(self, inp:str, parse_inp:ParseResult=None, idx:int=0) -> ParseResult:
        if parse_inp is not None:
            idx = parse_inp.last_idx()
        else:
            idx = 0

        parse_result = ParseResult()
        for target_idx, c in enumerate(inp[idx:]):
            if c.isalpha():
                continue
            elif target_idx > 0 and (c.isalnum() or c == '-'):
                continue
            else:
                break

        if target_idx == 0:
            return parse_result

        parse_result.add(idx + target_idx + 1, inp[idx : idx + target_idx+1])

        return parse_result



# ======== COMBINATORS ======== #
class Left(Combinator):
    def __repr__(self) -> str:
        return 'Left<%s|%s>' % (repr(self.A), repr(self.B))

    def __call__(self, inp:str, parse_inp:ParseResult=None, idx:int=0) -> ParseResult:
        a_result = self.A(inp, parse_inp=parse_inp, idx=idx)
        if a_result.empty():
            return a_result
        _ = self.B(inp, parse_inp=a_result, idx=idx)

        return a_result


class Right(Combinator):
    def __repr__(self) -> str:
        return 'Right<%s|%s>' % (repr(self.A), repr(self.B))

    def __call__(self, inp:str, parse_inp:ParseResult=None, idx:int=0) -> ParseResult:
        a_result = self.A(inp, parse_inp=parse_inp, idx=idx)
        if a_result.empty():
            return a_result

        b_result = self.B(inp, parse_inp=a_result, idx=idx)

        return b_result


class QuotedString(Combinator):
    def __init__(self) -> None:
        self.quote = CharParser("\"")
        self.alpha = AlphaSpaceParser()
        self.left  = Left(ZeroOrMoreCombinator(self.alpha), self.quote)
        self.quoted_str = Right(self.quote, self.left)

    def __repr__(self) -> str:
        return "QuotedString()"

    def __call__(self, inp:str, parse_inp:ParseResult=None, idx:int=0) -> ParseResult:
        #from pudb import set_trace; set_trace()
        result = self.quoted_str(inp, parse_inp=parse_inp, idx=idx)
        return result

        #a_result = self.A(inp, parse_inp=parse_inp, idx=idx)

        #if not a_result.empty():
        #    return a_result

        #b_result = self.B(inp, parse_inp=parse_inp, idx=idx)

        #return b_result
