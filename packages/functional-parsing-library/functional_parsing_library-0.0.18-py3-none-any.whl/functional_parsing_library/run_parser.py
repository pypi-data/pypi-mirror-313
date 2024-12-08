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
    parse_result = parser(to_parse)

    if isinstance(parse_result, CouldNotParse):
        raise ParsingError

    if raise_on_remainder and len(parse_result.remainder) > 0:
        raise NotFullyParsed

    return parse_result.result
