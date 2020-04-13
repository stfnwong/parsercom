# UNDERSTANDING PARSER COMBINATORS
I don't understand parser combinators, and this is something I want to fix (ideally tonight).

### Simple example
Imagine there was a simple parser `A` which only recognized the single character `a`. If we provided `A` with some example string then we would expect the output to be like the following:

- `A(eps) = {}`
- `A(a) =   {1}`
- `A(ab) = {1}`
- `A(acegi) = {1}`
- `A(aaa) = {1}`
- `A(xa) = {}`

In this case we assume that the indicies of the characters in the string begin at 0. Take note that `A` returns some set no matter what string is passed to it. If we look closer we see that the rules actually are

- `A` always returns some kind of set.
- If there is no `a` character at the start of the string then `A` returns an empty set (eg: with the string `xa`)
- If `A` can find an `a` at the start of the string, then it consumes that `a` character and includes the index 1 in the output set. This indicates that further parsing should happen starting from the index 1.
- `A` doesn't care if there is an `a` character elsewhere in the string, it simply consumes the first character and returns.




### Calling API
So far it looks like I've settled on something like

```
    def __call__(self, inp:str, parse_inp:common.ParseResult=None, idx:int=0) -> common.ParseResult:

```

as a common function signature for parsers.
