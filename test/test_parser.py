"""
TEST_PARSER
Unit tests for parsers

Stefan Wong 2020
"""
# units under test
from parsercom.parser import (
    ParseResult,
    AlphaParser,
    CharParser,
    NumParser,
    StringParser,
    OneOrMore,
    ZeroOrMore,
)


class TestAlphaParser:
    inp_strings_single = ['', 'a', 'b', '1', '2', '{']
    #inp_strings_multi  = ['', 'a', 'b', 'ab', 'bb', 'a1', '2a']    # for combinator test...

    def test_inp_string_single(self) -> None:
        alpha_parser = AlphaParser()
        exp_outputs = [
            ParseResult(),         # ''
            ParseResult(1, 'a'),   # 'a'
            ParseResult(1, 'b'),   # 'b'
            ParseResult(),         # '1'
            ParseResult(),         # '2'
            ParseResult(),         # '{'
        ]
        parser_outputs = []
        for inp in self.inp_strings_single:
            parser_outputs.append(alpha_parser(inp))

        assert len(parser_outputs) == len(exp_outputs)
        for exp_out, test_out in zip(exp_outputs, parser_outputs):
            assert  exp_out == test_out


class TestNumParse:
    inp_strings_single = ['', '1', '2', 'a', 'b', '{']
    #inp_strings_multi  = ['', '1', '12', '123']        # TODO : this test is for combinator of NumParser

    def test_inp_string_single(self) -> None:
        num_parser = NumParser()
        exp_outputs = [
            ParseResult(),         # ''
            ParseResult(1, '1'),   # '1'
            ParseResult(1, '2'),   # '2'
            ParseResult(),         # 'a'
            ParseResult(),         # 'b'
            ParseResult(),         # '{'
        ]

        parser_outputs = []
        for inp in self.inp_strings_single:
            parser_outputs.append(num_parser(inp))

        assert len(parser_outputs) == len(exp_outputs)
        for exp_out, test_out in zip(exp_outputs, parser_outputs):
            assert  exp_out == test_out


class TestCharParser:
    inp_strings_1 = ["", "a", "ab", "acegi", "aaaa", "x"]

    def test_parse_char(self) -> None:
        exp_outputs_1 = [
            ParseResult(),
            ParseResult(1, self.inp_strings_1[1][0]),
            ParseResult(1, self.inp_strings_1[2][0]),
            ParseResult(1, self.inp_strings_1[3][0]),
            ParseResult(1, self.inp_strings_1[4][0]),
            ParseResult()
        ]

        cparser = CharParser('a')
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
            ParseResult(),
            ParseResult(),
            ParseResult(3, "ayy"),
            ParseResult(),
            ParseResult(3, "ayy"),
            ParseResult(),
            ParseResult(),
            ParseResult(3, "ayy"),
            ParseResult(3, "ayy"),
        ]

        s_parser = StringParser('ayy')

        parser_outputs = []
        for i in self.inp_strings:
            parser_outputs.append(s_parser(i, idx=0))

        # display
        for n, o in enumerate(parser_outputs):
            print('s_parser(%s) produced : %s' % (self.inp_strings[n], str(o)))

        assert  len(parser_outputs) == len(exp_outputs_2)
        for exp_out, test_out in zip(exp_outputs_2, parser_outputs):
            assert  exp_out == test_out



class TestZeroOrMoreParser:
    other_comb_inputs = [
        "",
        "at least one char",
        "0 or more",
        "1 or more"
    ]

    def test_one_or_more(self) -> None:
        one_or_more = OneOrMore()
        expected_results = [
            ParseResult(),
            ParseResult(17, "at least one char"),
            ParseResult(9, "0 or more"),
            ParseResult(9, "1 or more")
        ]

        parse_results = []
        for s in self.other_comb_inputs:
            parse_results.append(one_or_more(s))

        for n, res in enumerate(parse_results):
            print(n, res)

        assert len(parse_results) == len(expected_results)
        for res, exp_res in zip(parse_results, expected_results):
            assert res == exp_res

    def test_zero_or_more(self) -> None:
        zero_or_more = ZeroOrMore()

        expected_results = [
            ParseResult(1, ""),
            ParseResult(17, "at least one char"),
            ParseResult(9, "0 or more"),
            ParseResult(9, "1 or more")
        ]

        parse_results = []
        for s in self.other_comb_inputs:
            parse_results.append(zero_or_more(s))

        for n, res in enumerate(parse_results):
            print(n, res)

        assert len(parse_results) == len(expected_results)
        for res, exp_res in zip(parse_results, expected_results):
            assert res == exp_res

