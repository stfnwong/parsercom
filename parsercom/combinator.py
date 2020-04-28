"""
COMBINATOR
Some combinators

Stefan Wong 2020
"""

from parsercom import parser
from typing import Union

# TODO : how to implement lazy eval?

class Combinator:
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


class Alternation(Combinator):
    def __repr__(self) -> str:
        return 'Alternation<%s|%s>' % (repr(self.A), repr(self.B))

    def __call__(self, inp:str, parse_inp:parser.ParseResult=None, idx:int=0) -> parser.ParseResult:
        a_result = self.A(inp, parse_inp=parse_inp, idx=idx)
        b_result = self.B(inp, parse_inp=parse_inp, idx=idx)

        parse_out = parser.ParseResult()
        parse_out.extend(a_result)
        parse_out.extend(b_result)

        return parse_out


class Concatenation(Combinator):
    def __repr__(self) -> str:
        return 'Concatenation<%s * %s>' % (repr(self.A), repr(self.B))

    def __call__(self, inp:str, parse_inp:parser.ParseResult=None, idx:int=0) -> parser.ParseResult:
        if parse_inp is not None:
            start_idx = parse_inp.last_idx()
        else:
            start_idx = idx

        a_result = self.A(inp, parse_inp, idx=idx)
        print('[%s] : a_result : %s' % (repr(self), str(a_result)))
        if a_result.empty():
            return a_result

        b_result = self.B(inp, a_result)
        print('[%s] : b_result : %s' % (repr(self), str(b_result)))

        return b_result


class KleeneStar(Combinator):
    def __init__(self, A:parser.Parser, accept_partial=False) -> None:
        self.A = A
        self.accept_partial = accept_partial
        self.E = parser.EmptyParser()

    def __repr__(self) -> str:
        return 'KleeneStar<%s>' % (repr(self.A))

    def __call__(self, inp:str, parse_inp:parser.ParseResult=None, idx:int=0) -> parser.ParseResult:
        empty_result = self.E(inp, parse_inp=parse_inp, idx=idx)
        #result = self.A(inp, parse_inp=parse_inp, idx=idx)
        result = self.A(inp, parse_inp=empty_result)

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
        if not self.accept_partial and result.last_idx() < len(inp):
            return parser_out

        parser_out.add(result.last_idx(), inp[start_idx-1 : result.last_idx()])

        return parser_out
