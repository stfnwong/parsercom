"""
TEST_COMBINATOR
Tests of combinator objects

Stefan Wong 2020
"""

# unit(s) under test
from parsercom import combinator
from parsercom import parser


class TestOR:
    inp_string_1 = "boondoggle"

    def test_alternation(self) -> None:
        boo_parser = parser.StringParser('boo')
        boondoggle_parser = parser.StringParser('boondoggle')

        exp_outputs = [
            parser.ParseResult()
        ]
        exp_outputs[0].add(3, 'boo')

        alt_combo = combinator.OR(
            boo_parser,
            boondoggle_parser
        )

        alt_result = alt_combo(self.inp_string_1)

        print(alt_combo)
        print(alt_result)

        assert alt_result == exp_outputs[0]


class TestAND:
    inp_strings = ('', 'a', 'ab', 'aa', 'aaa', 'aba')

    def test_concatenation(self) -> None:
        a_parser = parser.CharParser('a')
        b_parser = parser.CharParser('b')
        # this combinator can recognise 'ab'
        ab_combo = combinator.AND(a_parser, b_parser)
        # expected outputs
        exp_outputs = [
            parser.ParseResult(),           # ''
            parser.ParseResult(),           # 'a'
            parser.ParseResult(2, 'ab'),    # 'ab'
            parser.ParseResult(),           # 'aa'
            parser.ParseResult(),           # 'aaa'
            parser.ParseResult(2, 'ab'),    # 'aba'
        ]

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
        ab_combo = combinator.AND(a_parser, b_parser)

        exp_a_only = parser.ParseResult(1, 'a')
        exp_b_only = parser.ParseResult(2, 'b')

        a_only = a_parser('ab', idx=0)
        assert exp_a_only == a_only

        b_only = b_parser('ab', idx=1)
        assert exp_b_only == b_only

        exp_a_result = parser.ParseResult()
        exp_ab_result_0 = parser.ParseResult(2, 'ab')
        exp_ab_result_1 = parser.ParseResult()

        a_result = ab_combo('a', idx=0)
        assert exp_a_result == a_result

        ab_result_0 = ab_combo('ab', idx=0)
        assert exp_ab_result_0 == ab_result_0

        ab_result_1 = ab_combo('ab', idx=1)
        assert exp_ab_result_1 == ab_result_1


class TestKleeneStar:
    inp_strings_alpha = ('', 'a', 'aa', 'aaa', 'aaaa', 'aaabcdefg')
    inp_strings_num = ('', '1', '2', '12', '122', '122a', 'a112', '1a2')

    def test_kleene_star_num(self) -> None:
        p = parser.NumParser()
        ks = combinator.KleeneStar(p)

        exp_outputs = [
            parser.ParseResult(0, ''), # ''
            parser.ParseResult(0, ''), # '1'
            parser.ParseResult(0, ''), # '2'
            parser.ParseResult(0, ''), # '12'
            parser.ParseResult(0, ''), # '122'
            parser.ParseResult(0, ''),
            parser.ParseResult(0, ''),
            parser.ParseResult(0, ''),
        ]
        # 'a'
        exp_outputs[1].add(1, '1')
        # 'aa'
        exp_outputs[2].add(1, '2')
        # 'aaa'
        exp_outputs[3].add(2, '12')
        # 'aaaa'
        exp_outputs[4].add(3, '122')

        # Parse the strings
        results = []
        for inp in self.inp_strings_num:
            results.append(ks(inp))

        print('%s results for each string :' % str(ks))
        for n, r in enumerate(results):
            print(n, r, repr(ks), self.inp_strings_num[n])

        assert len(results) == len(exp_outputs)

        for n, (exp, out) in enumerate(zip(exp_outputs, results)):
            print("[%d / %d] : comparing %s -> %s" % \
                  (n, len(results), str(exp), str(out))
            )
            assert exp == out

        # with partial match we should also get '122' from '122a'
        ks.accept_partial = True
        exp_outputs[5].add(3, '122')
        exp_outputs[7].add(1, '1')

        results = []
        for inp in self.inp_strings_num:
            results.append(ks(inp))
        assert len(results) == len(exp_outputs)

        for n, (exp, out) in enumerate(zip(exp_outputs, results)):
            print("[%d / %d] : comparing %s -> %s" % \
                  (n, len(results), str(exp), str(out))
            )
            assert exp == out


    def test_kleene_star_char(self) -> None:
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

        # Parse the strings
        results = []
        for inp in self.inp_strings_alpha:
            results.append(ks(inp))

        print('%s results for each string :' % str(ks))
        for n, r in enumerate(results):
            print(n, r, repr(ks), self.inp_strings_alpha[n])

        assert len(results) == len(exp_outputs)

        for n, (exp, out) in enumerate(zip(exp_outputs, results)):
            print("[%d / %d] : comparing %s -> %s" % \
                  (n, len(results), str(exp), str(out))
            )
            assert exp == out

        # if we turn on partial match then we should get 'aaa' as the
        # result for the input string 'aaabcdefg'
        exp_partial_match = parser.ParseResult(0, '')
        exp_partial_match.add(3, 'aaa')
        ks.accept_partial = True
        partial_match_result = ks(self.inp_strings_alpha[5])

        assert exp_partial_match == partial_match_result


class TestKleeneDot:
    inp_strings_alpha = ('', 'a', 'aa', 'aaa', 'aaaa', 'aaabcdefg')
    inp_strings_num = ('', '1', '2', '12', '122', '122a', 'a112', '1a2')

    def test_kleene_dot_num(self) -> None:
        p = parser.NumParser()
        ks = combinator.KleeneDot(p)

        exp_outputs = [
            parser.ParseResult(0, ''), # []
            parser.ParseResult(1, '1'), # '1'
            parser.ParseResult(1, '2'), # '2'
            parser.ParseResult(2, '12'), # '12'
            parser.ParseResult(3, '122'), # '122'
            parser.ParseResult(3, '122'), # '122a'
            parser.ParseResult(0, ''), # 'a112'
            parser.ParseResult(1, '1'), # '1a2'
        ]

        # Parse the strings
        results = []
        for inp in self.inp_strings_num:
            results.append(ks(inp))

        print('%s results for each string :' % str(ks))
        for n, r in enumerate(results):
            print(n, r, repr(ks), self.inp_strings_num[n])

        assert len(results) == len(exp_outputs)

        for n, (exp, out) in enumerate(zip(exp_outputs, results)):
            print("[%d / %d] : comparing %s -> %s" % \
                  (n, len(results), str(exp), str(out))
            )
            assert exp == out

    def test_kleene_dot_char(self) -> None:
        p = parser.CharParser('a')
        ks = combinator.KleeneDot(p)
        # expected outputs
        exp_outputs = [
            parser.ParseResult(0, ''),     # ''
            parser.ParseResult(1, 'a'),    # 'a'
            parser.ParseResult(2, 'aa'),   # 'aa'
            parser.ParseResult(3, 'aaa'),  # 'aaa'
            parser.ParseResult(4, 'aaaa'), # 'aaaa'
            parser.ParseResult(3, 'aaa'),  # 'aaabcdefg'
        ]

        # Parse the strings
        results = []
        for inp in self.inp_strings_alpha:
            results.append(ks(inp))

        print('%s results for each string :' % str(ks))
        for n, r in enumerate(results):
            print(n, r, repr(ks), self.inp_strings_alpha[n])

        assert len(results) == len(exp_outputs)

        for n, (exp, out) in enumerate(zip(exp_outputs, results)):
            print("[%d / %d] : comparing %s -> %s" % \
                  (n, len(results), str(exp), str(out))
            )
            assert exp == out


class TestHigherOrderCombinators:
    inp_strings = ['your mum', 'not your mum', 'thisisarunonsentence']
    inp_strings_word = ['', 'the', 'quick', '0brown', '4fox', 'jumped2']

    def test_word_one_or_more_chars(self) -> None:
        exp_outputs = [
            parser.ParseResult(0, ''),
            parser.ParseResult(3, 'the'),
            parser.ParseResult(5, 'quick'),
            parser.ParseResult(0, ''),
            parser.ParseResult(0, ''),
            parser.ParseResult(6, 'jumped')
        ]
        z_parser    = parser.AlphaParser()
        word_parser = combinator.KleeneDot(z_parser)

        #from pudb import set_trace; set_trace()
        parser_output = []
        for inp in self.inp_strings_word:
            parser_output.append(word_parser(inp))

        for n, r in enumerate(parser_output):
            print(n, r)

        for n, (exp, out) in enumerate(zip(exp_outputs, parser_output)):
            print("[%d / %d] : comparing %s -> %s" % \
                  (n, len(parser_output), str(exp), str(out))
            )
            assert exp == out


class TestHigherOrderConcat:
    inp_strings = ['your mum', 'not your mum', 'thisisarunonsentence']
    inp_strings_word = ['', 'the', 'quick', '0brown', '4fox', 'jumped2']

    # TODO : unify what the output looks like for the AND and OR combinator
    def test_word_with_trailing_num(self) -> None:
        exp_outputs = [
            parser.ParseResult(),
            parser.ParseResult(),
            parser.ParseResult(),
            parser.ParseResult(),
            parser.ParseResult(),
            parser.ParseResult(7, 'jumped2'),
        ]
        #exp_outputs[5].add(7, 'jumped2')

        z_parser    = parser.AlphaParser()
        n_parser    = parser.NumParser()
        word_parser = combinator.KleeneDot(z_parser)
        trailing_num_parser = combinator.AND(word_parser, n_parser)

        #parser_output = [trailing_num_parser(inp) for inp in self.inp_strings_word]
        #from pudb import set_trace; set_trace()
        parser_output = []
        for inp in self.inp_strings_word:
            parser_output.append(trailing_num_parser(inp))

        for n, r in enumerate(parser_output):
            print(n, r)

        for n, (exp, out) in enumerate(zip(exp_outputs, parser_output)):
            print("[%d / %d] : comparing %s -> %s" % \
                  (n, len(parser_output), str(exp), str(out))
            )
            assert exp == out

    def test_word_with_leading_num(self) -> None:
        exp_outputs = [
            parser.ParseResult(),
            parser.ParseResult(),
            parser.ParseResult(),
            parser.ParseResult(),
            parser.ParseResult(),
            parser.ParseResult(),
        ]
        exp_outputs[3].add(6, '0brown')
        exp_outputs[4].add(4, '4fox')

        n_parser    = parser.NumParser()
        z_parser    = parser.AlphaParser()
        word_parser = combinator.KleeneStar(z_parser)
        leading_num_parser = combinator.AND(n_parser, word_parser)

        parser_output = []
        for inp in self.inp_strings_word:
            parser_output.append(leading_num_parser(inp))

        for n, r in enumerate(parser_output):
            print(n, r)

        for n, (exp, out) in enumerate(zip(exp_outputs, parser_output)):
            print("[%d / %d] : comparing %s -> %s" % \
                  (n, len(parser_output), str(exp), str(out))
            )
            assert exp == out

#    def test_word_with_or_without_leading_num(self) -> None:
#        exp_outputs = [
#            parser.ParseResult(0, ''),
#            parser.ParseResult(0, ''),
#            parser.ParseResult(0, ''),
#            parser.ParseResult(0, ''),
#            parser.ParseResult(0, ''),
#        ]
#        exp_outputs[1].add(3, 'the')
#        exp_outputs[2].add(5, 'quick')
#        exp_outputs[3].add(5, '0brown')
#        exp_outputs[4].add(5, '4fox')
#
#        n_parser    = parser.NumParser()
#        zero_or_more_num_parser  = combinator.KleeneStar(n_parser)
#        z_parser    = parser.AlphaParser()
#        word_parser = combinator.KleeneStar(z_parser)
#        leading_num_parser = combinator.AND(
#            zero_or_more_num_parser,
#            word_parser
#        )
#
#        print(leading_num_parser)
#
#        parser_output = []
#        for inp in self.inp_strings_word:
#            parser_output.append(leading_num_parser(inp))
#
#        for n, r in enumerate(parser_output):
#            print(n, r)
#
#        for n, (exp, out) in enumerate(zip(exp_outputs, parser_output)):
#            print("[%d / %d] : comparing %s -> %s" % \
#                  (n, len(parser_output), str(exp), str(out))
#            )
#            assert exp == out
#
    #def test_word_space_word(self) -> None:
    #    # Test ZZ* S ZZ*
    #    s_parser = parser.CharParser(' ')
    #    z_parser = parser.AlphaParser()

    #    # Make some combinators
    #    word_parser            = combinator.KleeneStar(z_parser)
    #    word_parser            = combinator.AND(z_parser, word_parser)
    #    word_plus_space_parser = combinator.AND(word_parser, s_parser)

    #    word_space_word_parser  = combinator.AND(word_plus_space_parser, word_parser)

    #    parser_output = []
    #    for inp in self.inp_strings:
    #        parser_output.append(word_space_word_parser(inp))

    #    for n, r in enumerate(parser_output):
    #        print(n, r)
