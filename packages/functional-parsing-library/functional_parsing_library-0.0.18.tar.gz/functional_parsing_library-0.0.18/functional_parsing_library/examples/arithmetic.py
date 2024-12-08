from __future__ import annotations

from dataclasses import dataclass

from functional_parsing_library.asserts import assert_parsing_succeeds
from functional_parsing_library.integer.integer import integer
from functional_parsing_library.recursive_parser import RecursiveParser
from functional_parsing_library.strings import char


@dataclass(frozen=True)
class Plus:
    left_operand: Expression
    right_operand: Expression


Leaf = int
Expression = Leaf | Plus

leaf = integer
plus: RecursiveParser[Plus] = RecursiveParser()
operand = ((char('(') > plus.parser) < char(')')) | leaf
plus.parser = Plus * (operand < char('+')) & operand

expression = plus.parser | leaf


def test_computation() -> None:
    to_parse = '300+(200+900)'
    assert_parsing_succeeds(expression, to_parse).with_result(
        Plus(
            left_operand=300,
            right_operand=Plus(
                left_operand=200,
                right_operand=900,
            )
        )
    )
