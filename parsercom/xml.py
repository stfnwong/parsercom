"""
XML
Parsers for XML

Stefan Wong 2020
"""
# TODO : note there is lots of boilerplate here...


from parsercom.parser import ParseResult, Parser
from parsercom.combinator import Combinator


class Identifier(Parser):
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


class Left(Combinator):
    def __repr__(self) -> str:
        return 'Left<%s|%s>' % (repr(self.A), repr(self.B))

    def __call__(self, inp:str, parse_inp:ParseResult=None, idx:int=0) -> ParseResult:
        a_result = self.A(inp, parse_inp=parse_inp, idx=idx)
        _ = self.B(inp, parse_inp=a_result, idx=idx)

        return a_result


class Right(Combinator):
    def __repr__(self) -> str:
        return 'Right<%s|%s>' % (repr(self.A), repr(self.B))

    def __call__(self, inp:str, parse_inp:ParseResult=None, idx:int=0) -> ParseResult:
        a_result = self.A(inp, parse_inp=parse_inp, idx=idx)
        b_result = self.B(inp, parse_inp=a_result, idx=idx)

        return b_result


class QuotedString(Combinator):
    def __repr__(self) -> str:
        return "QuotedString()"

    def __call__(self, inp:str, parse_inp:ParseResult=None, idx:int=0) -> ParseResult:
        a_result = self.A(inp, parse_inp=parse_inp, idx=idx)

        if not a_result.empty():
            return a_result

        b_result = self.B(inp, parse_inp=parse_inp, idx=idx)

        return b_result
