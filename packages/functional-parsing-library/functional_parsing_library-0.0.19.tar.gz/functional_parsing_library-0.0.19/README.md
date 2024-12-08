# functional_parsing_library

A small production non-ready Python library implementing basic applicative parsers. Roughly speaking, these are functions
with signature `str -> T | CouldNotParse` transforming strings into structured data. For example, you might have a function
`integer` which will transform `"1"` and `"-1919"` to the integers `1` and `-1919`, and the string `"boink"` to `CouldNotParse()`.

What makes these functions useful is that they can be combined with so-called parser combinators. This way, complicated parsers
can be gradually built up from smaller, simpler parsers. 
For example, if we already have parsers `nonnegative_integer` and `negative_integer`, the `integer` parser from earlier 
could be written as `integer = nonnegative_integer | negative_integer`, where `|` should be read as "or". This library 
implements various such combinators, such as `many`, `some`, `ignore_left`, `many_till`, and so on.

Another piece of structure that makes these functions useful is that they're functorial: If I have a parser `p` of type 
`Parser[T]` (that is, a function which parses strings to objects of type `T`), and a function `f: T -> S`, then `f * p`
will be a parser for objects of type `S`. For example, take `len * many(word('borf'))`, and try to parse `"borfborfborf"`.
Here `word('borf')` will parse `"borf"` to the string `"borf"` (and any other string to `CouldNotParse`), so the parser
`many(word('borf')` will try and match as many `"borf"`s as possible and parse our string to the list `['borf', 'borf', 'borf']`. 
The length of this list is 3, so `len * many(word('borf'))` parses our string to the integer 3.

This works with multi-argument functions as well. If `f` is a function of type `[T, S] -> U`, and we have parsers `p`
and `q` for objects of type `T` and `S`, then `f * p & q` will first try to match `p`, and if this succeeds it will try
and match `q`, and finally it will apply `f`.

Another feature of this library is its type safety. Running mypy on

```python
from functional_parsing_library.strings import word


def add_strings(one: str, two: str, three: str) -> int:
    return len(one + two + three)


reveal_type(add_strings * word('hi'))
reveal_type(add_strings * word('hi') & word('hi'))
reveal_type(add_strings * word('hi') & word('hi') & word('di'))
```
will show that the first parser has type `MappedParser[int, str, str]`, the second `MappedParser[int, str]`, and the
third `Parser[int]`. Expressions like
```python
add_strings * word('hi') & word('hi') & integer
```
or
```python
add_strings * word('hi') & word('hi') & word('hi') & word('hi')
```
will raise a `TypeError`, and mypy will catch this.

### Documentation
To see some documentation, clone this repo, run
```bash
make serve-documentation
```
and in your browser you can peruse this library's docstrings at port 8000.

### Some operator overloading weirdness
This library overloads the operators `*`, `<`, `>`, and so on to implement parser combinators. Usually this results in more
readable parsers, but there are some quirks in order of evaluation whiich results in unexpected behavior. For example,
let's take three parsers, `a`, `b`, and `c`, which parse the strings `"a"`, `"b"`, and `"c"`, respectively. Then one would
expect `a > b < c` to parse `"abc"` to the string `"b"`. This is because `>` parses the left parser and discards the result,
and proceeds to parse the right parser. Similarly for `<`. However, `a > b < c` produces a failure on `"abc"` with the 
error message `String "abc" does not start with "b"`. The parser succeeds on `"bca"` with result `"b"` and remainder `"a"`.

### TODO list
- Backport to earlier Python versions, say 3.9 and up.
- Ambiguity in parsing, for example `char('a') | word('ab')` should parse `"ab"` as both `"a"` with remainder `"b"` and as `"ab"` with no remainder.
- Endow the parsers with a monadic structure. Probably context managers can be used to craft some makeshift Haskell-like `do` notation.


### Internal mypy error
The following snippet results in an internal mypy error:
```python
from functional_parsing_library.combinators.maybe import maybe
from functional_parsing_library.integer.integer import integer


def transform_none(integer: int, *maybe_int: int | None) -> int:
    if maybe_int[0] is None:
        return 0
    return maybe_int[0] + integer


transform_none * integer & maybe(integer) & maybe(integer)
```
