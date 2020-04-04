"""
GALAXY BRAIN
This is a collection of patronisingly simple parsers.

I read an article about parser combinators that described a simple parser for
the character 'a' (https://qntm.org/combinators). Since its dead simple, why not
start there?

Stefan Wong 2020
"""

from typing import List

# Match a single 'a'
class AParser:
    def __init__(self) -> None:
        self.target = 'a'

    def __repr__(self) -> str:
        return 'AParser'

    def __call__(self, inp:str, idx:int) -> List[int]:
        if len(inp) == 0:
            return []

        if idx <= len(inp) and inp[idx] == self.target:
            return [idx + 1]

        return []


# Match one or 2 'a's
class A2Parser:
    def __init__(self) -> None:
        self.target = 'a'

    def __repr__(self) -> str:
        return 'A2Parser'

    def __call__(self, inp:str, idx:int) -> List[int]:
        if len(inp) == 0:
            return []

        # TODO : this looks awkward
        parse_out = list()
        if idx < len(inp) and inp[idx] == self.target:
            parse_out.append(idx + 1)

        if idx + 1 < len(inp) and inp[idx+1] == self.target:
            parse_out.append(idx + 2)

        return parse_out

