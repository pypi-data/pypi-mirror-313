from collections.abc import Container

from functional_parsing_library.parser import Parser
from functional_parsing_library.strings.modules.char_satisfies import char_satisfies


def char_in(string: Container[str]) -> Parser[str]:
    """
    Matches any character in the given string. For example,
    >>> parser = char_in('abcd')
    >>> parser('abdicate').result
    'a'
    >>> parser('abdicate').remainder
    'bdicate'
    """
    return Parser(char_satisfies(lambda c: c in string))
