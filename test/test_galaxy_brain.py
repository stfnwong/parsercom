"""
TEST_GALAXY_BRAIN
Tests for galaxy brain parsers

Stefan Wong 2020
"""

import unittest
# unit under test
from parsercom import parser
from parsercom import galaxy_brain


class TestAParser(unittest.TestCase):
    def setUp(self) -> None:
        self.inp_strings = ["", "a", "ab", "acegi", "aaaa", "x"]
        self.exp_outputs = [
            parser.ParseResult(),
            parser.ParseResult(1, self.inp_strings[1][0]),
            parser.ParseResult(1, self.inp_strings[2][0]),
            parser.ParseResult(1, self.inp_strings[3][0]),
            parser.ParseResult(1, self.inp_strings[4][0]),
            parser.ParseResult()
        ]

    def test_parse(self) -> None:
        parser = galaxy_brain.AParser()

        parser_outputs = []
        for i in self.inp_strings:
            parser_outputs.append(parser(i, idx=0))

        # display
        for n, o in enumerate(parser_outputs):
            print('Input %d [%s] produced : %s' % (n, self.inp_strings[n], str(o)))

        self.assertEqual(len(parser_outputs), len(self.exp_outputs))
        for exp_out, test_out in zip(self.exp_outputs, parser_outputs):
            self.assertEqual(exp_out, test_out)


class TestA2Parser(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_parse(self) -> None:
        inp_strings = ["", "a", "aa", "aaa", "aaaa"]
        exp_outputs = [parser.ParseResult() for _ in range(len(inp_strings))]
        exp_outputs[1].add(1, inp_strings[1][0])
        exp_outputs[2].add(1, inp_strings[2][0])
        exp_outputs[2].add(2, inp_strings[2][0:2])
        exp_outputs[3].add(1, inp_strings[3][0])
        exp_outputs[3].add(2, inp_strings[3][0:2])
        exp_outputs[4].add(1, inp_strings[4][0])
        exp_outputs[4].add(2, inp_strings[4][0:2])

        #for n, inp in enumerate(inp_strings):
        #    print('Input %d [%s] expects output \n\t%s' % (n, str(inp), str(exp_outputs[n])))

        parser = galaxy_brain.A2Parser()

        parser_outputs = []
        for i in inp_strings:
            parser_outputs.append(parser(i, idx=0))

        # display
        for n, o in enumerate(parser_outputs):
            print('Input %d [%s] produced : %s' % (n, inp_strings[n], str(o)))

        self.assertEqual(len(parser_outputs), len(exp_outputs))
        for n, (exp_out, test_out) in enumerate(zip(exp_outputs, parser_outputs)):
            print(n, exp_out, test_out)
            self.assertEqual(exp_out, test_out)

    def test_parse_offset(self) -> None:
        inp_strings = ["a", "ab", "xab", "xaab"]
        # lets see what happens as we adjust the offset
        exp_outputs = [set(), set([1]), set([1, 2]), set([1, 2]), set([1, 2])]

        parser = galaxy_brain.A2Parser()

        parser_outputs = []
        for offset in (0, 1, 2):
            out_this_offset = []
            for i in inp_strings:
                out_this_offset.append(parser(i, idx=0))
            parser_outputs.append(out_this_offset)

        # display
        for offset in (0, 1, 2):
            print('\t Offset %d' % offset)
            for n, o in enumerate(parser_outputs[offset]):
                print('parser(%s, %d) \t-> %s' %
                      (inp_strings[n], offset, str(o)))




class TestAParserCombineA2Parser(unittest.TestCase):
    def setUp(self) -> None:
        self.inp_strings = ["", "ab", "aa", "aaa", "aaaa"]
        #self.exp_outputs = [[], [1], [1], [1], [1], []]

    def test_concat(self) -> None:
        a_parser  = galaxy_brain.AParser()
        b_parser  = galaxy_brain.BParser()
        a2_parser = galaxy_brain.A2Parser()

        # There is no proper way to do this yet, so for now
        # just manually stack parsers

        a1_result = a_parser(self.inp_strings[3], idx=0)
        print('A1(%s)     : %s' % (str(self.inp_strings[3]), str(a1_result)))
        a2_result = a2_parser(self.inp_strings[3], a1_result)
        print('A2(A1(%s)) : %s' % (str(self.inp_strings[3]), str(a2_result)))


if __name__ == '__main__':
    unittest.main()
