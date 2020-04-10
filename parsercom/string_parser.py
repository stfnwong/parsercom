"""
STRING_PARSER
Parse a string. After enough of this I will actually make a real parser.
Note that this isn't implemented in a pythonic way for now - I just eat one char
in the string at a time.

Stefan Wong 2020
"""

from parsercom import common



class StringParser:
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
            parse_result = parse_inp
        else:
            parse_result = common.ParseResult()

        if idx >= len(inp):
            return parse_result

        # try to match sentence, moving over sep chars?
        for n, c in enumerate(self.target_str):
            # NOTE: moving over sep chars isn't strictly what we want to do,
            # because that is really the domain of tokenization.
            if inp[idx + n] in self.sep_chars:
                continue

            if c != inp[idx + n]:
                return parse_result

        # if there are still more characters in the input then
        # don't adjust the parse output
        if len(inp) > (idx + n + 1):
            if inp[idx + n + 1] not in self.sep_chars:
                return parse_result

        # TODO : why am I adding two here?
        parse_result.add(idx + n + 1, inp[idx : idx+n+1])

        return parse_result
