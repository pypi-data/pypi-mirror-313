from typing import TypeVarTuple, Callable, overload, TypeVar, cast

from functional_parsing_library.parser import Parser, S, T, ParseResults, CouldNotParse, MappedParser

Ts = TypeVarTuple('Ts')


U = TypeVar('U')


@overload
def parse_and(left: MappedParser[S, T], right: Parser[T]) -> Parser[S]:
    pass


@overload
def parse_and(left: MappedParser[S, T, U, *Ts], right: Parser[T]) -> MappedParser[S, U, *Ts]:
    pass


def parse_and(
    left: MappedParser[S, T] | MappedParser[S, T, U, *Ts],
    right: Parser[T],
) -> Parser[S] | MappedParser[S, U, *Ts]:
    """
    Is used to combine parsers p and q to a parser which first parses using p and then the remainder using q. The `&`
    operator is overloaded to make use of this function.

    If p is of type Parser[T] and q is of type Parser[S], then it is not obvious what type p & q should have. For example,
    it could be of type Parser[tuple[T, S]], it could be of type Parser[list[T | S]], and so on. Therefore, `&` can only
    be used in combination with a callable f of type `Callable[[T, S], U]` which specifies how to combine the result of
    p with the result of q. Writing `p & q` without applying such a function will raise a TypeError.

    For example,
    >>> from functional_parsing_library.strings import char
    >>> a, b = char('a'), char('b')
    >>> plus = lambda x, y: x + ' and ' + y
    >>> parser = plus * a & b
    >>> parser('ab').result
    'a and b'

    This works with callables of more than two arguments as well:
    >>> c = char('c')
    >>> triple_plus = lambda x, y, z: x + y + z
    >>> parser = triple_plus * a & b & c
    >>> parser('abc').result
    'abc'
    """
    if left.is_multi_arg:
        multi_arg_left = cast(MappedParser[S, T, U, *Ts], left)
        return _parse_and_for_multiple_arguments(multi_arg_left, right)

    single_arg_left = cast(MappedParser[S, T], left)
    return _parse_and_for_single_argument(single_arg_left, right)


def _parse_and_for_multiple_arguments(
    left: MappedParser[S, T, U, *Ts],
    right: Parser[T],
) -> MappedParser[S, U, *Ts]:
    def parser_(to_parse: str) -> ParseResults[Callable[[U, *Ts], S]] | CouldNotParse:
        result = _parse_left_and_then_right(left, right, to_parse)
        if isinstance(result, CouldNotParse):
            return result
        right_result, parsed_function = result

        return ParseResults(
            result=lambda *ts: parsed_function(right_result.result, *ts),
            remainder=right_result.remainder
        )

    return MappedParser(parser_)


def _parse_and_for_single_argument(
    left: MappedParser[S, T],
    right: Parser[T],
) -> Parser[S]:
    def parser(to_parse: str) -> ParseResults[S] | CouldNotParse:
        result = _parse_left_and_then_right(left, right, to_parse)
        if isinstance(result, CouldNotParse):
            return result
        right_result, parsed_function = result

        return ParseResults(
            result=parsed_function(right_result.result),
            remainder=right_result.remainder
        )

    return Parser(parser)


def _parse_left_and_then_right(
    left: MappedParser[S, T, *Ts],
    right: Parser[T],
    to_parse: str
) -> tuple[ParseResults[T], Callable[[T, *Ts], S]] | CouldNotParse:
    left_result = left(to_parse)
    if isinstance(left_result, CouldNotParse):
        return left_result

    right_result = right(left_result.remainder)
    if isinstance(right_result, CouldNotParse):
        return right_result

    return right_result, left_result.result
