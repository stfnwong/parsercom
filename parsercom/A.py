"""
A
I read an article about parser combinators that described a simple parser for
the character 'a' (https://qntm.org/combinators). Since its dead simple, why not
start there?

Stefan Wong 2020
"""

from typing import List


class AParser:
    def __init__(self) -> None:
        self.target = 'a'

    def __repr__(self) -> str:
        return 'AParser'

    def __call__(self, inp:str, idx:int) -> List[int]:
        if len(inp) == 0:
            return []

        if inp[0] == self.target:
            return [idx + 1]

        return []
