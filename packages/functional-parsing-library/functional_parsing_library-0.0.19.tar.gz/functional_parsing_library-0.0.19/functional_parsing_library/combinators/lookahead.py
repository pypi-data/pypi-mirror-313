from functional_parsing_library.parser import Parser, S, U, ParseResults, CouldNotParse


def lookahead(parser: Parser[S], look_for: Parser[U]) -> Parser[S]:
    """
    Matches the same as the first parser, as long as it is followed by something matching the second parser. Does not
    consume whatever the second parser matches. For example,
    >>> from functional_parsing_library.strings import char
    >>> parser = lookahead(char('a'), char('b'))
    >>> parser('abbb').result
    'a'
    >>> parser('abbb').remainder
    'bbb'
    >>> isinstance(parser('a'), CouldNotParse)
    True
    """
    def parser_(to_parse: str) -> ParseResults[S] | CouldNotParse:
        result_combined = (parser < look_for)(to_parse)
        if isinstance(result_combined, CouldNotParse):
            return result_combined
        return parser(to_parse)

    return Parser(parser_)
