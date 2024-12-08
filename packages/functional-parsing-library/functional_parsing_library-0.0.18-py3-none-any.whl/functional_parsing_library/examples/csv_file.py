from dataclasses import dataclass

from functional_parsing_library.asserts import assert_parsing_succeeds
from functional_parsing_library.combinators.sequence.many import many
from functional_parsing_library.combinators.sequence.separated_by import separated_by
from functional_parsing_library.integer.integer import integer
from functional_parsing_library.strings.modules.char import char
from functional_parsing_library.strings.modules.char_not_in import char_not_in

Value = str | int


@dataclass(frozen=True)
class CSVFile:
    header: list[str]
    records: list[list[Value]]


comma = char(',')
string_char = char_not_in(',\n')
column_name = ''.join * many(string_char)
new_line = char('\n')
header = separated_by(column_name, separator=comma) < new_line


string = ''.join * many(string_char)
value = integer | string
record = separated_by(value, separator=comma)
records = separated_by(record, separator=new_line)

csv_file = CSVFile * header & records


def test_that_stuff_parses() -> None:
    my_file = '\n'.join([
        'hi,mom',
        'orf,blorf',
        '3,dorf',
        '9,nein9'
    ])

    assert_parsing_succeeds(csv_file, my_file).with_result(
        CSVFile(
            header=['hi', 'mom'],
            records=[
                ['orf', 'blorf'],
                [3, 'dorf'],
                [9, 'nein9'],
            ]
        )
    )
