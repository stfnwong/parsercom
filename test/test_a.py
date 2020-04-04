"""
TEST_A
Test the A parser

Stefan Wong 2020
"""

import unittest
# unit under test
from parsercom import A


class TestAParser(unittest.TestCase):
    def setUp(self) -> None:
        self.inp_strings = [
            "",
            "a",
            "ab",
            "acegi",
            "aaaa",
            "xa"
        ]
        self.exp_outputs = [
            [],
            [1],
            [1],
            [1],
            [1],
            []
        ]

    def test_parse(self) -> None:
        parser = A.AParser()

        parser_outputs = []
        for i in self.inp_strings:
            parser_outputs.append(parser(i, 0))

        # display
        for n, o in enumerate(parser_outputs):
            print('Input %d [%s] produced : %s' % (n, self.inp_strings[n], str(o)))

        self.assertEqual(len(parser_outputs), len(self.exp_outputs))

        for exp_out, test_out in zip(self.exp_outputs, parser_outputs):
            self.assertEqual(exp_out, test_out)



if __name__ == '__main__':
    unittest.main()
