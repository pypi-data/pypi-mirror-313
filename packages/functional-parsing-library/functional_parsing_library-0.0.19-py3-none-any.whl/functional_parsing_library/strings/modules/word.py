from functional_parsing_library.parser import Parser, ParseResults, CouldNotParse


def word(word_to_parse_for: str) -> Parser[str]:
    """
    Parse a given word. For example,
    >>> parser = word('train')
    >>> parser('training').result
    'train'
    >>> parser('training').remainder
    'ing'
    """
    def parser(to_parse: str) -> ParseResults[str] | CouldNotParse:
        if not to_parse.startswith(word_to_parse_for):
            return CouldNotParse(f'String "{to_parse}" does not start with "{word_to_parse_for}"')
        return ParseResults(word_to_parse_for, to_parse[len(word_to_parse_for):])

    return Parser(parser)
