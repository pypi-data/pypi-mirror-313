import functools
from typing import Callable

from functional_parsing_library.parser import CouldNotParse, ParseResults, U


def check_for_empty_string(
    parse_function: Callable[[str], ParseResults[U] | CouldNotParse],
) -> Callable[[str], ParseResults[U] | CouldNotParse]:
    @functools.wraps(parse_function)
    def parser_(to_parse: str) -> ParseResults[U] | CouldNotParse:
        if len(to_parse) == 0:
            return CouldNotParse('String to parse is empty')
        return parse_function(to_parse)

    return parser_
