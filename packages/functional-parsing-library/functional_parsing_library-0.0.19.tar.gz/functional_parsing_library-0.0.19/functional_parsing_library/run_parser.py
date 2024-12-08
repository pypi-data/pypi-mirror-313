from functional_parsing_library.parser import Parser, S, CouldNotParse


class ParsingError(Exception):
    pass


class NotFullyParsed(Exception):
    pass


def run_parser(
    parser: Parser[S],
    to_parse: str,
    raise_on_remainder: bool = False,
) -> S:
    """
    Utility function for running parsers. On parse errors, instead of an error value CouldNotParse, this function raises
    an exception. It also unwraps the parse result:
    >>> from functional_parsing_library.strings import char
    >>> parser = char('a')
    >>> run_parser(parser, 'ab')
    'a'
    """
    parse_result = parser(to_parse)

    if isinstance(parse_result, CouldNotParse):
        raise ParsingError

    if raise_on_remainder and len(parse_result.remainder) > 0:
        raise NotFullyParsed

    return parse_result.result
