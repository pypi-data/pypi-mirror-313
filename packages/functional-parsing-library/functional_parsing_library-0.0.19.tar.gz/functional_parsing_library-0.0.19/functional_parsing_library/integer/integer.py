import string

from functional_parsing_library.fmap import to_int
from functional_parsing_library.strings.modules.char import char
from functional_parsing_library.strings.modules.char_in import char_in
from functional_parsing_library.combinators.sequence.many import many


digit = char_in(string.digits)
digits = ''.join * many(digit)
nonnegative_integer = to_int * digits


def negate(x: int) -> int:
    return -x


negative_integer = negate * (char('-') > nonnegative_integer)
integer = nonnegative_integer | negative_integer
