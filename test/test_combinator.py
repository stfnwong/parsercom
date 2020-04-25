"""
TEST_COMBINATOR
Tests of combinator objects

Stefan Wong 2020
"""

# unit(s) under test
from parsercom import combinator
from parsercom import parser


class TestAlternation:
    inp_string_1 = "boondoggle"

    def test_alternation(self) -> None:
        boo_parser = parser.StringParser('boo')
        boondoggle_parser = parser.StringParser('boondoggle')

        alt_combo = combinator.Alternation(
            boo_parser,
            boondoggle_parser
        )

        alt_result = alt_combo.parse(self.inp_string_1)

        print(alt_combo)
        print(alt_result)


class TestConcatenation:
    inp_strings = ('', 'a', 'ab', 'aa', 'aaa', 'aba')

    def test_concatenation(self) -> None:
        a_parser = parser.CharParser('a')
        b_parser = parser.CharParser('b')
        ab_combo = combinator.Concatenation(a_parser, b_parser)
        # expected outputs
        exp_outputs = [
            parser.ParseResult(),           # ''
            parser.ParseResult(1, 'a'),     # 'a'
            parser.ParseResult(1, 'a'),     # 'ab'
            parser.ParseResult(1, 'a'),     # 'aa'
            parser.ParseResult(1, 'a'),     # 'aaa'
            parser.ParseResult(1, 'a'),     # 'aba'
        ]
        exp_outputs[2].add(2, 'b')
        exp_outputs[5].add(2, 'b')

        results = []
        for inp in self.inp_strings:
            results.append(ab_combo.parse(inp))

        print('%s results for each string :' % str(ab_combo))
        for n, r in enumerate(results):
            print(n, r)

        assert len(results) == len(exp_outputs)

        for n, (exp, out) in enumerate(zip(exp_outputs, results)):
            print("[%d / %d] : comparing %s -> %s" % \
                  (n, len(results), str(exp), str(out))
            )
            assert exp == out

    def test_ab_concat_offset(self) -> None:
        a_parser = parser.CharParser('a')
        b_parser = parser.CharParser('b')
        ab_combo = combinator.Concatenation(a_parser, b_parser)

        exp_a_only = parser.ParseResult(1, 'a')
        exp_b_only = parser.ParseResult(2, 'b')

        a_only = a_parser('ab', idx=0)
        assert exp_a_only == a_only

        b_only = b_parser('ab', idx=1)
        assert exp_b_only == b_only

        exp_a_result = parser.ParseResult(1, 'a')
        exp_ab_result_0 = parser.ParseResult(1, 'a')
        exp_ab_result_0.add(2, 'b')
        exp_ab_result_1 = parser.ParseResult()

        a_result = ab_combo.parse('a', idx=0)
        assert exp_a_result == a_result

        ab_result_0 = ab_combo.parse('ab', idx=0)
        assert exp_ab_result_0 == ab_result_0

        ab_result_1 = ab_combo.parse('ab', idx=1)
        assert exp_ab_result_1 == ab_result_1


class TestKleeneStar:
    inp_strings = ('', 'a', 'aa', 'aaa', 'aaaa', 'aaabcdefg')

    def test_kleene_star(self) -> None:
        p = parser.CharParser('a')
        ks = combinator.KleeneStar(p)
        # expected outputs
        exp_outputs = [
            parser.ParseResult(0, ''), # ''
            parser.ParseResult(0, ''), # 'a'
            parser.ParseResult(0, ''), # 'aa'
            parser.ParseResult(0, ''), # 'aaa'
            parser.ParseResult(0, ''), # 'aaaa'
            parser.ParseResult(0, ''), # 'aaabcdefg'
        ]
        # 'a'
        exp_outputs[1].add(1, 'a')
        # 'aa'
        exp_outputs[2].add(1, 'a')
        exp_outputs[2].add(2, 'a')
        # 'aaa'
        exp_outputs[3].add(1, 'a')
        exp_outputs[3].add(2, 'a')
        exp_outputs[3].add(3, 'a')
        # 'aaaa'
        exp_outputs[4].add(1, 'a')
        exp_outputs[4].add(2, 'a')
        exp_outputs[4].add(3, 'a')
        exp_outputs[4].add(4, 'a')
        # 'aaabcdef'
        exp_outputs[5].add(1, 'a')
        exp_outputs[5].add(2, 'a')
        exp_outputs[5].add(3, 'a')

        # Parse the strings
        results = []
        for inp in self.inp_strings:
            results.append(ks.parse(inp))

        print('%s results for each string :' % str(ks))
        for n, r in enumerate(results):
            print(n, r, repr(ks), self.inp_strings[n])

        assert len(results) == len(exp_outputs)

        for n, (exp, out) in enumerate(zip(exp_outputs, results)):
            print("[%d / %d] : comparing %s -> %s" % \
                  (n, len(results), str(exp), str(out))
            )
            assert exp == out


if __name__ == '__main__':
    unittest.main()
