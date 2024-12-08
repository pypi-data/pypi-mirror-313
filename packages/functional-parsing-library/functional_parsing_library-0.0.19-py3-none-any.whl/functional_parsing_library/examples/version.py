from dataclasses import dataclass

from functional_parsing_library.asserts import assert_parsing_succeeds, assert_parsing_fails
from functional_parsing_library.integer.integer import nonnegative_integer
from functional_parsing_library.strings import char


@dataclass(frozen=True, order=True)
class Version:
    major: int
    minor: int
    patch: int


period = char('.')
version = Version * (nonnegative_integer < period) & (nonnegative_integer < period) & nonnegative_integer


def test_version() -> None:
    assert_parsing_succeeds(version, '1.2.0').with_result(Version(1, 2, 0))


def test_version_fails_on_negatives() -> None:
    assert_parsing_fails(version, '1.-2.0')
