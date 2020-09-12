"""
TEST_XML
Unit tests for XML parser

Stefan Wong 2020
"""

from parsercom.parser import ParseResult
# units under test
from parsercom.xml import (
    Identifier
)


class TestIdentifier:
    iden_input = [
        "this-is-a-valid-identifier",
        "valid2",
        "0-this-is-invalid-1"
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

