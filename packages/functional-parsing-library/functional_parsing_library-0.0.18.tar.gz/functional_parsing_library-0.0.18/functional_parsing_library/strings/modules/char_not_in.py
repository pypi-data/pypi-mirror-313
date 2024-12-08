from collections.abc import Container

from functional_parsing_library.parser import Parser
from functional_parsing_library.strings.modules.char_satisfies import char_satisfies


def char_not_in(characters: Container[str]) -> Parser[str]:
    """
    Match any character not among the given characters. For example,
    >>> char_not_in('abcd')('eddy').result
    'e'
    """
    return char_satisfies(lambda c: c not in characters)
