"""
TEST_STRING_PARSER
Test string parser

Stefan Wong 2020
"""

import unittest
# units under test
from parsercom import parser

#from pudb import set_trace; set_trace()


class TestStringParser(unittest.TestCase):
    def setUp(self) -> None:
        self.inp_strings_1 = ["", "ay", "aylmao", "ay lmao", "ayy lmao", "ayayy", "ayy", "ay ayy"]
        self.inp_strings_2 = ["", "ay", "ayy", "ayayy", "ayyay"]

    def test_parse_string(self) -> None:
        exp_outputs_1 = [
            common.ParseResult(),
            common.ParseResult(2, "ay"),
            common.ParseResult(),
            common.ParseResult(2, "ay"),
            common.ParseResult(),
            common.ParseResult(),
            common.ParseResult(),
        ]

        parser = parser.StringParser('ay')

        parser_outputs = []
        for i in self.inp_strings_1:
            parser_outputs.append(parser(i, idx=0))

        # display
        for n, o in enumerate(parser_outputs):
            print('parser(%s) produced : %s' % (self.inp_strings_1[n], str(o)))

        self.assertEqual(len(parser_outputs), len(exp_outputs_1))
        for exp_out, test_out in zip(exp_outputs_1, parser_outputs):
            self.assertEqual(exp_out, test_out)


    def test_parse_combo(self) -> None:
        exp_outputs_2 = [
            common.ParseResult(),
            common.ParseResult(2, "ay"),
            common.ParseResult(3, "ayy"),
            common.ParseResult(2, "ay"),        # input is "ayayy"
            common.ParseResult(3, "ayy")
        ]
        exp_outputs_2[3].add(5, "ayy")

        parser_ay  = parser.StringParser('ay')
        parser_ayy = parser.StringParser('ayy')

        parser_outputs = []
        for i in self.inp_strings_2:
            ay_output = parser_ay(i, idx=0)
            print('parser_ay(\"%s\", idx=0) : \n\t%s' % (i, str(ay_output)))
            ayy_output = parser_ayy(i, ay_output)
            print('parser_ayy(parser_ay(\"%s\", idx=0)) : \n\t%s' % (i, str(ayy_output)))
            parser_outputs.append(ayy_output)

        # display
        for n, o in enumerate(parser_outputs):
            print('[%d] parser_ayy(parser_ay(\"%s\"))' % (n, str(self.inp_strings_2[n])))
            print('input %d [%s] produced : \n\t%s' % (n, self.inp_strings_2[n], str(o)))



    def test_two_parse_string(self) -> None:
        exp_outputs_1 = [
            common.ParseResult(),
            common.ParseResult(2, "ay"),
            common.ParseResult(),
            common.ParseResult(2, "ay"),
            common.ParseResult(3, "ayy"),
            common.ParseResult(),
            common.ParseResult(2, "ay"),
        ]

        parser_ay  = parser.StringParser('ay')
        parser_ayy = parser.StringParser('ayy')

        parser_outputs = []
        for i in self.inp_strings_1:
            ay_output = parser_ay(i, idx=0)
            print('parser_ay(\"%s\", idx=0) : %s' % (i, str(ay_output)))
            ayy_output = parser_ayy(i, ay_output)
            print('parser_ayy(parser_ay(\"%s\", idx=0)) : %s' % (i, str(ayy_output)))
            parser_outputs.append(ayy_output)

        # display
        for n, o in enumerate(parser_outputs):
            print('parser_ayy(parser_ay(\"%s\"))' % str(self.inp_strings_1[n]))
            print('input %d [%s] produced : %s' % (n, self.inp_strings_1[n], str(o)))

        self.assertEqual(len(parser_outputs), len(exp_outputs_1))
        for exp_out, test_out in zip(exp_outputs_1, parser_outputs):
            self.assertEqual(exp_out, test_out)


    def test_parse_ay_lmao(self) -> None:
        exp_outputs_1 = [
            common.ParseResult(),
            common.ParseResult(2, "ay"),
            common.ParseResult(),
            common.ParseResult(2, "ay"),
            common.ParseResult(3, "ayy"),
            common.ParseResult(),
            common.ParseResult(2, "ay"),
        ]

        parser_ay    = parser.StringParser('ay')
        parser_space = parser.StringParser(' ')
        parser_ayy   = parser.StringParser('ayy')

        parser_outputs = []
        for i in self.inp_strings_1:
            ay_output = parser_ay(i, idx=0)
            space_output = parser_space(i, ay_output)
            ayy_output = parser_ayy(i, space_output)
            parser_outputs.append(ayy_output)

        for n, o in enumerate(parser_outputs):
            print('parser_ayy(parser_space(parser_ay(\"%s\")))' % str(self.inp_strings_1[n]))
            print('input %d [%s] produced : %s' % (n, self.inp_strings_1[n], str(o)))


if __name__ == '__main__':
    unittest.main()
