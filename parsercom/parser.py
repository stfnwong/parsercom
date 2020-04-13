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
