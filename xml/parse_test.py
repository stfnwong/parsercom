"""
PARSE_TEST
Attempt to parse some XML

"""


from parsercom import parser


class Identifier(parser.Parser):
    def __repr__(self) -> str:
        return 'Identifier(\'%s\')' % str(self.inp_str)

    def __call__(self, inp:str, parse_inp:parser.ParseResult=None, idx:int=0) -> parser.ParseResult:
        if parse_inp is not None:
            idx = parse_inp.last_idx()
        else:
            idx = 0

        #from pudb import set_trace; set_trace()
        parse_result = parser.ParseResult()
        for target_idx, c in enumerate(inp[idx:]):
            if c.isalpha():
                continue
            elif target_idx > 0 and (c.isalnum() or c == '-'):
                continue
            else:
                break

        if target_idx == 0:
            return parse_result

        parse_result.add(idx + target_idx + 1, inp[idx : idx + target_idx+1])

        return parse_result


# Mini test
if __name__ == "__main__":
    iden_parser = Identifier()

    # try and parse some identifiers
    iden1 = "this-is-a-valid-identifier"
    iden2 = "valid2"
    iden3 = "0-this-is-invalid-1"

    parse_results = []
    for iden in (iden1, iden2, iden3):
        parse_results.append(iden_parser(iden))

    for n, res in enumerate(parse_results):
        print(n, res)
