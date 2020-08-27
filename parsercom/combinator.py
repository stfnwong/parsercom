"""
COMBINATOR
Some combinators

Stefan Wong 2020
"""

from parsercom import parser
from typing import Union

# TODO : how to implement lazy eval?

class Combinator:
    """
    Base class for Combinators
    """
    def __init__(self,
                 A:Union[parser.Parser, 'Combinator'],
                 B:Union[parser.Parser, 'Combinator']) -> None:
        self.A = A
        self.B = B

    def __repr__(self) -> str:
        return 'Combinator %s, %s' % (repr(self.A), repr(self.B))

    def __str__(self) -> str:
        return self.__repr__()

    def __call__(self, inp:str, parse_inp:parser.ParseResult=None, idx:int=0) -> parser.ParseResult:
        raise NotImplementedError('Should be implemented in derived class')


class OR(Combinator):
    """
    OR Combinator. Implements A || B, where || is
    the short-circuit OR. That is, the combinator returns the
    result of parsing A if its non-empty, otherwise it parses
    B and returns that result whether it is empty or not.
    """
    def __repr__(self) -> str:
        return 'OR<%s|%s>' % (repr(self.A), repr(self.B))

    def __call__(self, inp:str, parse_inp:parser.ParseResult=None, idx:int=0) -> parser.ParseResult:
        a_result = self.A(inp, parse_inp=parse_inp, idx=idx)

        if not a_result.empty():
            return a_result

        b_result = self.B(inp, parse_inp=parse_inp, idx=idx)

        return b_result


# So the way that I am using this parser now is like an AND operator
# Concat should be the


# TODO : maybe remove this combinator entirely...
class AND(Combinator):
    """
    AND combinator. Performs the concatenation of A and B.
    """
    def __repr__(self) -> str:
        return 'AND<%s * %s>' % (repr(self.A), repr(self.B))

    def __call__(self, inp:str, parse_inp:parser.ParseResult=None, idx:int=0) -> parser.ParseResult:
        #if parse_inp is not None:
        #    start_idx = parse_inp.last_idx()
        #else:
        #    start_idx = idx

        start_idx = parse_inp.last_idx() if parse_inp is not None else idx

        a_result = self.A(inp, parse_inp, idx=idx)
        if a_result.empty() or a_result.last_idx() == start_idx:
            return parser.ParseResult()

        b_result = self.B(inp, a_result)
        if b_result.last_idx() <= a_result.last_idx():
            return parser.ParseResult()

        parse_out = parser.ParseResult()
        parse_out.extend(a_result)
        parse_out.update(b_result.last_idx(), b_result.last_str())

        return parse_out


# TODO : call method seems a bit complicated...
class KleeneStar(Combinator):
    def __init__(self, A:parser.Parser, accept_partial=False) -> None:
        self.A = A
        self.E = parser.EmptyParser()
        self.accept_partial = accept_partial

    def __repr__(self) -> str:
        return 'KleeneStar<%s>' % (repr(self.A))

    # TODO : do we really need to return the empty result here?
    def __call__(self, inp:str, parse_inp:parser.ParseResult=None, idx:int=0) -> parser.ParseResult:
        # Handle the 'zeroth' time
        empty_result = self.E(inp, parse_inp=parse_inp, idx=idx)
        result = self.A(inp, parse_inp=empty_result)

        if len(result) == 0:
            return empty_result
        if len(result) == 1:
            return result

        # run this zero or more times up to unlimited bound
        start_idx = result.last_idx()
        while True:
            new_result = self.A(inp, idx=result.last_idx())
            if new_result.last_idx() <= result.last_idx() or new_result.empty():
                break
            result = new_result

        parser_out = parser.ParseResult()
        parser_out.extend(empty_result)

        # if we dont accept partial results and haven't consumed the
        # whole input then return an empty result
        #if not self.accept_partial and result.last_idx() < len(inp):
        #    return parser_out

        parser_out.add(result.last_idx(), inp[start_idx-1 : result.last_idx()])

        return parser_out


class KleeneDot(Combinator):
    def __init__(self, A: parser.Parser, accept_partial: bool = False) -> None:
        self.A = A
        self.accept_partial = accept_partial

    def __repr__(self) -> str:
        return 'KleeneDot<%s>' % (repr(self.A))

    def __call__(self, inp: str, parse_inp: parser.ParseResult=None, idx: int=0) -> parser.ParseResult:
        prev_result = parse_inp if parse_inp is not None else parser.ParseResult()
        start_idx = prev_result.last_idx()
        # keep parsing more tokens for as long as we can
        # NOTE: this implementation here seems much more complicated than
        # it needs to be....
        while True:
            new_result = self.A(inp, idx=prev_result.last_idx())
            if new_result.empty() or new_result.last_idx() <= prev_result.last_idx():
                break
            prev_result = new_result

        parser_out = parser.ParseResult()

        # if we dont accept partial results and haven't consumed the
        # whole input then return an empty result
        #if not self.accept_partial and result.last_idx() < len(inp):
        #    return parser_out

        parser_out.add(prev_result.last_idx(), inp[start_idx : prev_result.last_idx()])

        return parser_out
