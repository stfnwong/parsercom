"""
CHAR_PARSER
Parse a single character. After enough of this I will actually make a
real parser.

Stefan Wong 2020
"""

from parsercom import common


# Match a single character
class CharParser:
    def __init__(self, target_char:str) -> None:
        self.target_char = target_char

    def __repr__(self) -> str:
        return 'CharParser(%s)' % self.target_char

    def __str__(self) -> str:
        return self.__repr__()

    def __call__(self, inp:str, parse_inp:common.ParseResult=None, idx:int=0) -> common.ParseResult:
        if parse_inp is not None:
            idx = parse_inp.last_idx()
            parse_result = parse_inp
        else:
            parse_result = common.ParseResult()

        # Try to match one char
        if idx >= len(inp):
            return parse_result
        if inp[idx] == self.target_char:
            parse_result.add(idx + 1, inp[idx])

        return parse_result

    def get_target(self) -> str:
        return self.target_char
