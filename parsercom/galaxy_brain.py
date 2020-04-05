"""
GALAXY BRAIN
This is a collection of patronisingly simple parsers.

I read an article about parser combinators that described a simple parser for
the character 'a' (https://qntm.org/combinators). Since its dead simple, why not
start there?

Stefan Wong 2020
"""

from typing import Set
from parsercom import common

# debug
#from pudb import set_trace; set_trace()


# Match a single 'a'
class AParser:
    def __init__(self) -> None:
        self.target = 'a'

    def __repr__(self) -> str:
        return 'AParser'

    def __call__(self, inp:str, parse_inp:common.ParseResult=None, idx:int=0) -> common.ParseResult:
        if parse_inp is not None:
            idx = parse_inp.last_idx()

        parse_result = common.ParseResult()
        if idx < len(inp) and inp[idx] == self.target:
            parse_result.add(idx+1, inp[idx])

        return parse_result


# Match one or 2 'a's
class A2Parser:
    def __init__(self) -> None:
        self.target = 'a'

    def __repr__(self) -> str:
        return 'A2Parser'

    def __call__(self, inp:str, parse_inp:common.ParseResult=None, idx:int=0) -> common.ParseResult:
        if parse_inp is not None:
            idx = parse_inp.last_idx()

        parse_out = common.ParseResult()
        if idx >= len(inp):
            return parse_out

        if inp[idx] == self.target:
            parse_out.add(idx + 1, inp[idx])

        if (idx + 1) >= len(inp):
            return parse_out

        if inp[idx] == self.target and inp[idx+1] == self.target:
            parse_out.add(idx + 2, inp[idx:idx+2])

        return parse_out


# Match a single 'b'
class BParser:
    def __init__(self) -> None:
        self.target = 'b'

    def __repr__(self) -> str:
        return 'BParser'

    def __call__(self, inp:str, parse_inp:common.ParseResult=None, idx:int=0) -> common.ParseResult:
        parse_result = common.ParseResult()
        if idx <= len(inp) and inp[idx] == self.target:
            parse_result.add(idx+1, inp[idx])

        return parse_result
