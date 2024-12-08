import string
from enum import auto, Enum
from typing import Callable, Any

from functional_parsing_library.combinators.sequence.many import many
from functional_parsing_library.parser import S
from functional_parsing_library.strings.modules.char import char
from functional_parsing_library.strings.modules.char_in import char_in
from functional_parsing_library.strings.modules.word import word


class Honorific(Enum):
    MR = auto()
    MS = auto()


class Person:
    def __init__(self, honorific: Honorific, name: str, surname: str) -> None:
        self._honorific = honorific
        self._name = name
        self._surname = surname


def const(value: S) -> Callable[[Any], S]:
    return lambda x: value


alphabetic_character = char_in(string.ascii_letters)
alphabetic_word = ''.join * many(alphabetic_character)
mr = const(Honorific.MR) * (word('Mr.') | word('mr.'))
ms = const(Honorific.MS) * (word('Ms.') | word('ms.'))
honorific = (mr | ms) < char(' ')
name = alphabetic_word < char(' ')
surname = alphabetic_word
person = Person * honorific & name & surname
