from functional_parsing_library.combinators.lookahead import lookahead
from functional_parsing_library.combinators.sequence.many import many
from functional_parsing_library.parser import Parser, U, S


def many_till_exclusive(parser: Parser[U], until: Parser[S]) -> Parser[list[U]]:
    """
    Parses one or more matches for parser, followed by a match for until. Does not consume the match for until.
    For example,
    >>> from functional_parsing_library.strings import char
    >>> parser = many_till_exclusive(char('a'), char('b'))
    >>> parser('aab').result
    ['a', 'a']
    >>> parser('aab').remainder
    'b'
    """
    return lookahead(many(parser), look_for=until)
