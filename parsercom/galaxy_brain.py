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


# Match a single 'a'
class AParser:
    def __init__(self) -> None:
        self.target = 'a'

    def __repr__(self) -> str:
        return 'AParser'

    def __call__(self, pr:common.ParseResult=None, inp:str="", idx:int=0) -> common.ParseResult:
        parse_result = common.ParseResult()
        if idx < len(inp) and inp[idx] == self.target:
            parse_result.add(inp[1:], idx+1)

        return parse_result


# Match one or 2 'a's
class A2Parser:
    def __init__(self) -> None:
        self.target = 'a'

    def __repr__(self) -> str:
        return 'A2Parser'

    def __call__(self, pr:common.ParseResult=None, inp:str="", idx:int=0) -> common.ParseResult:
        parse_out = common.ParseResult()
        if idx < len(inp) and inp[idx] == self.target:
            parse_out.add(inp[1:], idx + 1)

        if idx + 1 < len(inp) and inp[idx+1] == self.target:
            parse_out.add(inp[2:], idx + 2)

        return parse_out


class BParser:
    def __init__(self) -> None:
        self.target = 'b'

    def __repr__(self) -> str:
        return 'BParser'

    def __call__(self, pr:common.ParseResult=None, inp:str="", idx:int=0) -> common.ParseResult:
        parse_result = common.ParseResult()
        if idx <= len(inp) and inp[idx] == self.target:
            parse_result.add(inp[1:], idx+1)

        return parse_result
