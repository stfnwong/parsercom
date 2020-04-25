"""
TEST_PARSER
Unit tests for parsers

Stefan Wong 2020
"""
# units under test
from parsercom import parser


class TestCharParser:
    inp_strings_1 = ["", "a", "ab", "acegi", "aaaa", "x"]
    inp_strings_2 = []

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

        assert len(parser_outputs) == len(exp_outputs_1)
        for exp_out, test_out in zip(exp_outputs_1, parser_outputs):
            assert  exp_out == test_out


class TestStringParser:
    inp_strings = ["", "ay", "ayy", "ayayy", "ayyay", "by", "byy", "ayy lmao", "ayylmao"]

    def test_parse_strings(self) -> None:
        exp_outputs_2 = [
            parser.ParseResult(),
            parser.ParseResult(),
            parser.ParseResult(3, "ayy"),
            parser.ParseResult(),
            parser.ParseResult(3, "ayy"),
            parser.ParseResult(),
            parser.ParseResult(),
            parser.ParseResult(3, "ayy"),
            parser.ParseResult(3, "ayy"),
        ]

        s_parser = parser.StringParser('ayy')

        parser_outputs = []
        for i in self.inp_strings:
            parser_outputs.append(s_parser(i, idx=0))

        # display
        for n, o in enumerate(parser_outputs):
            print('s_parser(%s) produced : %s' % (self.inp_strings[n], str(o)))

        assert  len(parser_outputs) == len(exp_outputs_2)
        for exp_out, test_out in zip(exp_outputs_2, parser_outputs):
            assert  exp_out == test_out
