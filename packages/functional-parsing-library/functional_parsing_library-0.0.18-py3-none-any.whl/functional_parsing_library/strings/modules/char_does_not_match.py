from typing import Any

from functional_parsing_library.check_for_empty_string import check_for_empty_string
from functional_parsing_library.parser import Parser, ParseResults, CouldNotParse
from functional_parsing_library.strings.modules.pop_one_character import pop_one_character


def char_does_not_match(parser: Parser[Any]) -> Parser[str]:
    """
    Match any character not matching the given parser. For example,
    >>> from functional_parsing_library.strings import digit
    >>> non_digit = char_does_not_match(digit)
    >>> non_digit('a').result
    'a'
    >>> isinstance(non_digit('3'), CouldNotParse)
    True
    """
    @check_for_empty_string
    def parser_(to_parse: str) -> ParseResults[str] | CouldNotParse:
        result = parser(to_parse)
        if not isinstance(result, CouldNotParse):
            return CouldNotParse()

        return pop_one_character(to_parse)

    return Parser(parser_)
