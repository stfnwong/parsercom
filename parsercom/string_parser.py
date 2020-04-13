"""
STRING_PARSER
Parse a string. After enough of this I will actually make a real parser.
Note that this isn't implemented in a pythonic way for now - I just eat one char
in the string at a time.

Stefan Wong 2020
"""

from parsercom import common
from parsercom import parser


class StringParser(parser.Parser):
    def __init__(self, target_str:str) -> None:
        self.target_str = target_str
        self.sep_chars = (' ', ',')     # TODO : this looks like it could be generalized into a super class..

    def __repr__(self) -> str:
        return 'StringParser(%s)' % self.target_str

    def __str__(self) -> str:
        return self.__repr__()

    def __call__(self, inp:str, parse_inp:common.ParseResult=None, idx:int=0) -> common.ParseResult:

        if parse_inp is not None:
            idx = parse_inp.last_idx()
            start_idx = parse_inp.last_idx()
            parse_result = parse_inp
        else:
            parse_result = common.ParseResult()
            start_idx = 0

        if idx >= len(inp):
            return parse_result

        target_idx = 0
        while (target_idx + idx) < len(inp):
            print('target_idx : %d, idx : %d len(inp) : %d' % (target_idx, idx, len(inp)))

            # NOTE: putting a break statement here means that the parser will
            # stop eating characters as soon as it sees its input in the
            # stream. Its not clear to me yet if this is quite the behaviour I
            # want...
            if target_idx >= len(self.target_str):
                #break
                return parse_result

            if self.target_str[target_idx] != inp[target_idx + idx]:
                return parse_result

            target_idx += 1

        parse_result.add(idx + target_idx, inp[start_idx : start_idx + target_idx])

        return parse_result
