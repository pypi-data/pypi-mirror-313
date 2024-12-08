import string
from typing import Any

from functional_parsing_library.combinators.sequence.many import many
from functional_parsing_library.combinators.sequence.separated_by import some_separated_by
from functional_parsing_library.integer.integer import integer
from functional_parsing_library.recursive_parser import RecursiveParser
from functional_parsing_library.strings.modules.char import char
from functional_parsing_library.strings.modules.char_in import char_in
from functional_parsing_library.strings.modules.word import word


valid_json_string_chars = string.ascii_letters + 'idk'
json_string = ''.join * ((char('"') > many(char_in(valid_json_string_chars))) < char('"'))

_json: RecursiveParser[Any] = RecursiveParser()
array = (char('[') > some_separated_by(_json.parser, word(', '))) < char(']')
key_value_pair = (lambda t, s: (t, s)) * (json_string < word(': ')) & _json.parser
json_object = dict * (
    (char('{') > some_separated_by(key_value_pair, word(', '))) < char('}')
)
_json.parser = integer | array | json_string | json_object
json = _json.parser
