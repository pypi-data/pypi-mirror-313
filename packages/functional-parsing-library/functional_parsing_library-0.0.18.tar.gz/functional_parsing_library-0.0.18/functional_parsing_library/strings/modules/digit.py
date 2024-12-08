import string

from functional_parsing_library.fmap import to_int
from functional_parsing_library.strings.modules.char_in import char_in


digit = to_int * char_in(string.digits)
