from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar, Generic, Callable, overload, TypeVarTuple

T = TypeVar('T', covariant=True)
Ts = TypeVarTuple('Ts')
S = TypeVar('S')
U = TypeVar('U')


@dataclass(frozen=True)
class ParseResults(Generic[T]):
    result: T
    remainder: str


@dataclass(frozen=True)
class NoReasonSpecified:
    pass


FailureReason = NoReasonSpecified | str


@dataclass(frozen=True)
class CouldNotParse:
    reason: FailureReason = NoReasonSpecified()


class Parser(Generic[T]):
    """
    This class is a wrapper for functions of signature `str -> ParseResults[T] | CouldNotParse` (i.e., parsers), and
    is used to overload the operators *, |, &, <, and > to make them call various parser combinators. If you wish to
    implement a parser which cannot be implemented by combining parsers found in this library, you implement a function
    `f` of signature `str -> ParseResults[T] | CouldNotParse`, and wrap it like so: `parser = Parser(f)`. Now your
    parser is ready for use and combination with other parsers.
    """
    def __init__(self, parser_function: Callable[[str], ParseResults[T] | CouldNotParse]) -> None:
        self._parser_function = parser_function

    def __call__(self, to_parse: str) -> ParseResults[T] | CouldNotParse:
        return self._parser_function(to_parse)

    def __or__(self, other: Parser[S]) -> Parser[T | S]:
        from functional_parsing_library.combinators.parse_or import or_2
        return or_2(parser_1=self, parser_2=other)

    @overload
    def __rmul__(self, other: Callable[[T, U, *Ts], S]) -> MappedParser[S, U, *Ts]:
        pass

    @overload
    def __rmul__(self, other: Callable[[T], S]) -> Parser[S]:
        pass

    def __rmul__(self, other: Callable[[T, U, *Ts], S] | Callable[[T], S]) -> MappedParser[S, U, *Ts] | Parser[S]:
        from functional_parsing_library.fmap import fmap
        return fmap(function=other, parser=self)

    def __gt__(self, other: Parser[S]) -> Parser[S]:
        from functional_parsing_library.combinators.ignore.ignore_left import ignore_left
        return ignore_left(left=self, right=other)

    def __lt__(self, other: Parser[S]) -> Parser[T]:
        from functional_parsing_library.combinators.ignore.ignore_right import ignore_right
        return ignore_right(left=self, right=other)

    @overload
    def __rand__(self, other: MappedParser[S, T]) -> Parser[S]:
        pass

    @overload
    def __rand__(self, other: MappedParser[S, T, U, *Ts]) -> MappedParser[S, U, *Ts]:
        pass

    def __rand__(self, other: MappedParser[S, T] | MappedParser[S, T, U, *Ts]) -> Parser[S] | MappedParser[S, U, *Ts]:
        from functional_parsing_library.combinators.parse_and import parse_and
        return parse_and(left=other, right=self)


class MappedParser(Parser[Callable[[*Ts], S]], Generic[S, *Ts]):
    """
    This class exists only to make __rand__ work. In the expression
    a & b, only if a and b are of different types is __rand__ evaluated.
    If a and b are of the same type, __rand__ is implemented, and __and__ is
    not, an error is raised.
    """
    def __init__(
        self,
        parser_function: Callable[[str], ParseResults[Callable[[*Ts], S]] | CouldNotParse],
    ) -> None:
        super().__init__(parser_function)
        self.is_multi_arg = False
