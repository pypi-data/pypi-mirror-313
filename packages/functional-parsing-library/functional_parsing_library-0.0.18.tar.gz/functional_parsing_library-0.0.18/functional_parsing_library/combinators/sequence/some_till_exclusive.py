from functional_parsing_library.combinators.lookahead import lookahead
from functional_parsing_library.combinators.sequence.many import some
from functional_parsing_library.parser import Parser, U, S


def some_till_exclusive(parser: Parser[U], until: Parser[S]) -> Parser[list[U]]:
    """
    Parses zero or more matches for parser, followed by a match for until. Does not consume the match for until.
    For example,
    >>> from functional_parsing_library.strings import char
    >>> parser = some_till_exclusive(char('a'), char('b'))
    >>> parser('aab').result
    ['a', 'a']
    >>> parser('aab').remainder
    'b'
    >>> parser('b').result
    []
    """
    return lookahead(some(parser), look_for=until)
