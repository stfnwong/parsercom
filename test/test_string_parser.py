"""
TEST_STRING_PARSER
Test string parser

Stefan Wong 2020
"""

import unittest
# units under test
from parsercom import parser


class TestStringParser(unittest.TestCase):
    def setUp(self) -> None:
        self.inp_strings = ["", "ay", "ayy", "ayayy", "ayyay", "by", "byy"]

    def test_parse_strings(self) -> None:
        exp_outputs_2 = [
            parser.ParseResult(),
            parser.ParseResult(),
            parser.ParseResult(3, "ayy"),
            parser.ParseResult(),
            parser.ParseResult(3, "ayy"),
            parser.ParseResult(),
            parser.ParseResult(),
        ]

        s_parser = parser.StringParser('ayy')

        parser_outputs = []
        for i in self.inp_strings:
            parser_outputs.append(s_parser(i, idx=0))

        # display
        for n, o in enumerate(parser_outputs):
            print('s_parser(%s) produced : %s' % (self.inp_strings[n], str(o)))

        self.assertEqual(len(parser_outputs), len(exp_outputs_2))
        for exp_out, test_out in zip(exp_outputs_2, parser_outputs):
            self.assertEqual(exp_out, test_out)


if __name__ == '__main__':
    unittest.main()
