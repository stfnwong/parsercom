"""
TEST_STRING_PARSER
Test string parser

Stefan Wong 2020
"""

import unittest
# units under test
from parsercom import common
from parsercom import string_parser

from pudb import set_trace; set_trace()


class TestStringParser(unittest.TestCase):
    def setUp(self) -> None:
        self.inp_strings_1 = ["", "ay ayy", "ay lmao", "ayy lmao", "ayanami rei", "ay"]

    def test_parse_string(self) -> None:
        exp_outputs_1 = [
            common.ParseResult(),
            common.ParseResult(2, "ay"),
            common.ParseResult(2, "ay"),
            common.ParseResult(),
            common.ParseResult(),
            common.ParseResult(2, "ay"),
        ]

        parser = string_parser.StringParser('ay')

        parser_outputs = []
        for i in self.inp_strings_1:
            parser_outputs.append(parser(i, idx=0))

        # display
        for n, o in enumerate(parser_outputs):
            print('Input %d [%s] produced : %s' % (n, self.inp_strings_1[n], str(o)))

        self.assertEqual(len(parser_outputs), len(exp_outputs_1))
        for exp_out, test_out in zip(exp_outputs_1, parser_outputs):
            self.assertEqual(exp_out, test_out)


    def test_two_parse_string(self) -> None:
        exp_outputs_1 = [
            common.ParseResult(),
            common.ParseResult(2, "ay"),
            common.ParseResult(2, "ay"),
            common.ParseResult(),
            common.ParseResult(),
            common.ParseResult(2, "ay"),
        ]
        exp_outputs_1[1].add(6, "ayy")

        parser_ay  = string_parser.StringParser('ay')
        parser_ayy = string_parser.StringParser('ayy')

        parser_outputs = []
        for i in self.inp_strings_1:
            ay_output = parser_ay(i, idx=0)
            ayy_output = parser_ayy(i, ay_output)
            parser_outputs.append(ayy_output)

        # display
        for n, o in enumerate(parser_outputs):
            print('parser_ayy(parser_ay(\"%s\"))' % str(self.inp_strings_1[n]))
            print('Input %d [%s] produced : %s' % (n, self.inp_strings_1[n], str(o)))

        self.assertEqual(len(parser_outputs), len(exp_outputs_1))
        for exp_out, test_out in zip(exp_outputs_1, parser_outputs):
            self.assertEqual(exp_out, test_out)


if __name__ == '__main__':
    unittest.main()
