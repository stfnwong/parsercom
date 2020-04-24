"""
TEST_CHAR_PARSER
Test character parser

Stefan Wong 2020
"""

import unittest
# units under test
from parsercom import parser


class TestCharParser(unittest.TestCase):
    def setUp(self) -> None:
        self.inp_strings_1 = ["", "a", "ab", "acegi", "aaaa", "x"]
        self.inp_strings_2 = []

    def test_parse_char(self) -> None:
        exp_outputs_1 = [
            parser.ParseResult(),
            parser.ParseResult(1, self.inp_strings_1[1][0]),
            parser.ParseResult(1, self.inp_strings_1[2][0]),
            parser.ParseResult(1, self.inp_strings_1[3][0]),
            parser.ParseResult(1, self.inp_strings_1[4][0]),
            parser.ParseResult()
        ]

        cparser = parser.CharParser('a')
        parser_outputs = []
        for i in self.inp_strings_1:
            parser_outputs.append(cparser(i, idx=0))

        # display
        for n, o in enumerate(parser_outputs):
            print('Input %d [%s] produced : %s' % (n, self.inp_strings_1[n], str(o)))

        self.assertEqual(len(parser_outputs), len(exp_outputs_1))
        for exp_out, test_out in zip(exp_outputs_1, parser_outputs):
            self.assertEqual(exp_out, test_out)


if __name__ == '__main__':
    unittest.main()
