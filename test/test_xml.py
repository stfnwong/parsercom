"""
TEST_XML
Unit tests for XML parser

Stefan Wong 2020
"""

from parsercom.parser import (
    ParseResult,
    CharParser
)
from parsercom.combinator import (
    AND
)
# units under test
from parsercom.xml import (
    Identifier,
    OneOrMore,
    ZeroOrMore,
    Left,
    Right,
    QuotedString,
)


class TestParsers:
    iden_input = [
        "this-is-a-valid-identifier",
        "valid2",
        "0-this-is-invalid-1"
    ]

    other_comb_inputs = [
        "",
        "at least one char",
        "0 or more",
        "1 or more"
    ]

    def test_identifier(self) -> None:
        iden_parser = Identifier()
        expected_results = [
            ParseResult(26, "this-is-a-valid-identifier"),
            ParseResult(6, "valid2"),
            ParseResult()
        ]

        parse_results = []
        for iden in self.iden_input:
            parse_results.append(iden_parser(iden))

        # Display
        for n, res in enumerate(parse_results):
            print(n, res)

        assert len(parse_results) == len(expected_results)
        for res, exp_res in zip(parse_results, expected_results):
            assert res == exp_res

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



class TestCombinators:
    test_element = "<some-element/>"

    def test_tag_open_combinator(self) -> None:
        tag_parser = CharParser("<")
        iden_parser = Identifier()
        tag_open_combinator = AND(tag_parser, iden_parser)

        # NOTE: this is what the combinator outputs, but I am not quite happy
        # with it...
        expected_result = ParseResult(14, "<some-element/")
        parse_result = tag_open_combinator(self.test_element)

        assert parse_result == expected_result

    def test_left_combinator(self) -> None:
        tag_parser = CharParser("<")
        iden_parser = Identifier()
        left_combo = Left(tag_parser, iden_parser)

        expected_result = ParseResult(1, "<")
        parse_result = left_combo(self.test_element)
        assert parse_result == expected_result

    def test_right_combinator(self) -> None:
        tag_parser = CharParser("<")
        iden_parser = Identifier()
        right_combo = Right(tag_parser, iden_parser)

        #expected_result = ParseResult(2, "/>")
        expected_result = ParseResult(14, "some-element/")
        parse_result = right_combo(self.test_element)
        assert parse_result == expected_result



class TestQuotedString:
    valid_quoted_string = "\"this is a valid quoted string\""

    def test_quoted_string(self) -> None:
        quoted_string = QuotedString()
