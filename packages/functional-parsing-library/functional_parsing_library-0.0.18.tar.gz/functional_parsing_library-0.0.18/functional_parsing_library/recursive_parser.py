from __future__ import annotations

from typing import Generic

from functional_parsing_library.parser import Parser, T, ParseResults, CouldNotParse


class RecursiveParser(Generic[T]):
    """
    A container for forward references to parsers so as to support parsers for recursive languages, such as the language
    of expressions of the form (), (3), ((3)), 3, ((())).
    """
    def __init__(self) -> None:
        self._parser: Parser[T] | None = None

    @property
    def parser(self) -> Parser[T]:
        return Parser(self._parse_function)

    @parser.setter
    def parser(self, parser: Parser[T]) -> None:
        self._parser = parser

    def _parse_function(self, to_parse: str) -> ParseResults[T] | CouldNotParse:
        if self._parser is None:
            raise NotImplementedError
        return self._parser(to_parse)
