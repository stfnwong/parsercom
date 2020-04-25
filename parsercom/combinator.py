"""
COMBINATOR
Some combinators

Stefan Wong 2020
"""

from parsercom import parser

#from pudb import set_trace; set_trace()


class Combinator:
    def __init__(self, A:parser.Parser, B:parser.Parser) -> None:
        self.A = A
        self.B = B

    def __repr__(self) -> str:
        return 'Combinator %s, %s' % (repr(self.A), repr(self.B))

    def __str__(self) -> str:
        return self.__repr__()

    def parse(self) -> parser.ParseResult:
        raise NotImplementedError('Should be implemented in derived class')



class Alternation(Combinator):
    def __repr__(self) -> str:
        return 'Alternation <%s|%s>' % (repr(self.A), repr(self.B))

    def parse(self, inp:str, parse_inp:parser.ParseResult=None, idx:int=0) -> parser.ParseResult:
        a_result = self.A(inp, parse_inp=parse_inp, idx=idx)
        b_result = self.B(inp, parse_inp=parse_inp, idx=idx)

        return b_result.extend(a_result)


class Concatenation(Combinator):
    def __repr__(self) -> str:
        return 'Concatenation <%s.%s>' % (repr(self.A), repr(self.B))

    def parse(self, inp:str, parse_inp:parser.ParseResult=None, idx:int=0) -> parser.ParseResult:
        a_result = self.A(inp, parse_inp, idx=idx)
        b_result = self.B(inp, a_result)

        return b_result


class KleeneStar(Combinator):
    def __init__(self, A:parser.Parser) -> None:
        self.A = A
        self.E = parser.EmptyParser()

    def __repr__(self) -> str:
        return 'KleeneStar <%s>' % (repr(self.A))

    def parse(self, inp:str, parse_inp:parser.ParseResult=None, idx:int=0) -> parser.ParseResult:
        #from pudb import set_trace; set_trace()
        empty_result = self.E(inp, parse_inp=parse_inp, idx=idx)
        result = self.A(inp, parse_inp=empty_result)

        if len(result) == 1:
            return result

        # run this zero or more times up to unlimited bound
        while True:
            new_result = self.A(inp, result)
            if len(new_result) <= len(result):
                break
            result = new_result

        return result
