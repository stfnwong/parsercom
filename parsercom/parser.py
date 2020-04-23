"""
PARSER
Base class for parsers


Stefan Wong 2020
"""

from parsercom import common


class Parser:
    def __init__(self, target:str, **kwargs) -> None:
        self.target = target

    def __repr__(self) -> str:
        return 'Parser'

    def __str__(self) -> str:
        return self.__repr__()

    def __call__(self, inp:str, parse_inp:common.ParseResult=None, idx:int=0) -> common.ParseResult:
        raise NotImplementedError('This should be implemented in derived class')


class NullParser(Parser):
    def __repr__(self) -> str:
        return 'NullParser'

    def __call__(self, inp:str, parse_inp:common.ParseResult=None, idx:int=0) -> common.ParseResult:
        return common.ParseResult()


class EmptyParser(Parser):
    def __repr__(self) -> str:
        return 'EmptyParser'

    def __call__(self, inp:str, parse_inp:common.ParseResult=None, idx:int=0) -> common.ParseResult:
        if parse_inp is not None:
            return parse_inp

        return common.ParseResult(idx=idx, elem=None)


class CharParser(Parser):
    def __init__(self, target_char:str) -> None:
        self.target_char = target_char

    def __repr__(self) -> str:
        return 'CharParser(%s)' % self.target_char

    def __call__(self, inp:str, parse_inp:common.ParseResult=None, idx:int=0) -> common.ParseResult:
        if parse_inp is not None:
            idx = parse_inp.last_idx()

        parse_result = common.ParseResult()
        # Try to match one char
        if idx >= len(inp):
            return parse_result
        if inp[idx] == self.target_char:
            parse_result.add(idx + 1, inp[idx])

        return parse_result

    def get_target(self) -> str:
        return self.target_char




class StringParser(Parser):
    def __init__(self, target_str:str) -> None:
        self.target_str = target_str
        self.sep_chars = (' ', ',')     # TODO : this looks like it could be generalized into a super class..

    def __repr__(self) -> str:
        return 'StringParser(%s)' % self.target_str

    def __call__(self, inp:str, parse_inp:common.ParseResult=None, idx:int=0) -> common.ParseResult:
        if parse_inp is not None:
            idx = parse_inp.last_idx()
            start_idx = parse_inp.last_idx()
        else:
            start_idx = 0

        parse_result = common.ParseResult()
        if idx >= len(inp):
            return parse_result

        target_idx = 0
        while (target_idx + idx) < len(inp):
            #print('target_idx : %d, idx : %d len(inp) : %d' % (target_idx, idx, len(inp)))

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

    def get_target(self) -> str:
        return self.target_str
