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

        exp_outputs = [
            parser.ParseResult()
        ]
        exp_outputs[0].add(3, 'boo')
        exp_outputs[0].add(10, 'boondoggle')

        alt_combo = combinator.Alternation(
            boo_parser,
            boondoggle_parser
        )

        alt_result = alt_combo(self.inp_string_1)

        print(alt_combo)
        print(alt_result)

        assert alt_result == exp_outputs[0]



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
            results.append(ab_combo(inp))

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

        a_result = ab_combo('a', idx=0)
        assert exp_a_result == a_result

        ab_result_0 = ab_combo('ab', idx=0)
        assert exp_ab_result_0 == ab_result_0

        ab_result_1 = ab_combo('ab', idx=1)
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
        exp_outputs[2].add(2, 'aa')
        # 'aaa'
        exp_outputs[3].add(3, 'aaa')
        # 'aaaa'
        exp_outputs[4].add(4, 'aaaa')
        # 'aaabcdef'
        exp_outputs[5].add(3, 'aaa')

        # Parse the strings
        results = []
        for inp in self.inp_strings:
            results.append(ks(inp))

        print('%s results for each string :' % str(ks))
        for n, r in enumerate(results):
            print(n, r, repr(ks), self.inp_strings[n])

        assert len(results) == len(exp_outputs)

        for n, (exp, out) in enumerate(zip(exp_outputs, results)):
            print("[%d / %d] : comparing %s -> %s" % \
                  (n, len(results), str(exp), str(out))
            )
            assert exp == out


class TestHigherOrderCombinators:
    inp_strings = ['your mum', 'thisisarunonsentence']
    inp_strings_word = ['', 'the', 'quick', '0brown', '4fox']

    def test_word_one_or_more_chars(self) -> None:
        # TODO : actually, we want to be able to get an output like this
        exp_outputs = [
            parser.ParseResult(0, ''),
            parser.ParseResult(0, ''),
            parser.ParseResult(0, ''),
            parser.ParseResult(0, ''),
            parser.ParseResult(0, ''),
        ]
        exp_outputs[1].add(3, 'the')
        exp_outputs[2].add(5, 'quick')

        s_parser = parser.CharParser(' ')
        z_parser = parser.AlphaParser()
        z_star  = combinator.KleeneStar(z_parser)

        parser_output = []
        for inp in self.inp_strings_word:
            parser_output.append(z_star(inp))

        for n, r in enumerate(parser_output):
            print(n, r)

        for n, (exp, out) in enumerate(zip(exp_outputs, parser_output)):
            print("[%d / %d] : comparing %s -> %s" % \
                  (n, len(parser_output), str(exp), str(out))
            )
            assert exp == out

    def test_word_space_word(self) -> None:
        # Test ZZ* S ZZ*
        s_parser = parser.CharParser(' ')
        z_parser = parser.AlphaParser()

        # Make some combinators
        z_star  = combinator.KleeneStar(z_parser)
        zz_star = combinator.Concatenation(z_parser, z_star)
        zzss    = combinator.Concatenation(zz_star, s_parser)

        zzsszz  = combinator.Concatenation(zzss, zz_star)

        parser_output = []
        for inp in self.inp_strings:
            parser_output.append(zzsszz(inp))

        for n, r in enumerate(parser_output):
            print(n, r)

