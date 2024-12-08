from functional_parsing_library.parser import Parser
from functional_parsing_library.strings.modules.char_satisfies import char_satisfies


def char(c: str) -> Parser[str]:
    """
    Creates a parser which parses a single character c. For example,
    >>> char('a')('aabcd').result
    'a'
    >>> char('a')('aabcd').remainder
    'abcd'
    >>> from functional_parsing_library.parser import CouldNotParse
    >>> isinstance(char('a')('bla'), CouldNotParse)
    True
    """

    if len(c) != 1:
        raise ValueError

    return char_satisfies(
        condition=lambda x: x == c,
        reason_factory=lambda to_parse: f'String "{to_parse}" does not start with "{c}"',
    )
