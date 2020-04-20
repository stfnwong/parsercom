"""
TEST_COMBO
Trying out combinations of parsers

Stefan Wong 2020
"""

import unittest
from parsercom import parser


class TestCombo(unittest.TestCase):
    def setUp(self) -> None:
        self.inp_string_1 ="test nottest"
        self.inp_string_list = ['test', ' ', 'nottest']

    def test_string_space_string(self) -> None:
        string_parser_a = parser.StringParser('test')
        string_parser_b = parser.StringParser('nottest')
        space_parser    = parser.CharParser(' ')


        # If we do a-> space -> b then we should get the whole input
        sa = string_parser_a(self.inp_string_1, idx=0)
        sp = space_parser(self.inp_string_1, sa)
        sb = string_parser_b(self.inp_string_1, sp)


        for n, result in enumerate((sa, sp, sb)):
            print(n, result)


    def test_parse_string_list(self) -> None:
        sa = parser.StringParser('test')
        sp = parser.StringParser('nottest')
        sb = parser.CharParser(' ')

        parsers = [sa, sp, sb]

        for n, par in enumerate(parsers):
            if n == 0:
                result = par(self.inp_string_list[n], idx=0)
            else:
                result = par(self.inp_string_list[n], result)

            print(n, result)



if __name__ == '__main__':
    unittest.main()
