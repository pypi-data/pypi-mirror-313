from functional_parsing_library.parser import ParseResults


def pop_one_character(string: str) -> ParseResults[str]:
    return ParseResults(
        result=string[0],
        remainder=string[1:],
    )
