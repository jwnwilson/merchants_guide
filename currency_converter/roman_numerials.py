from copy import deepcopy

from currency_converter.exceptions import InvalidInput


class RomanNumeralConverter():
    # If this gets too big we should move it to another module
    # like we did for translations.
    roman_value_map = {
        'i': 1,
        'v': 5,
        'x': 10,
        'l': 50
    }
    valid_subtraction_map ={
        'v': ['i'],
        'x': ['i'],
        'l': ['x']
    }

    def _get_val(self, char):
        try:
            return self.roman_value_map[char]
        except KeyError:
            raise InvalidInput('"{}" is an invalid roman numeral'.format(
                char
            ))

    def _valid_subtraction(self, char1, char2):
        return char1 in self.valid_subtraction_map[char2]

    def _is_subtractable(self, char1, char2):
        val1 = self._get_val(char1)
        val2 = self._get_val(char2)
        return val2 > val1 and self._valid_subtraction(char1, char2)

    def get_amount(self, numeral_list):
        remaining_chars = deepcopy(numeral_list)
        total = 0
        same_char_count = 0
        while remaining_chars:
            char_1 = remaining_chars.pop(0)
            char_2 = remaining_chars[0] if remaining_chars else None

            # sanity checking for bad roman numeral syntax
            if char_1 == char_2:
                same_char_count += 1
                if same_char_count > 2:
                    raise InvalidInput(
                        'Invalid numeral, more than 3 of same type: {} '
                        'in a row.'.format(char_1))
            else:
                same_char_count = 0

            if char_2 and self._is_subtractable(char_1, char_2):
                total += self._get_val(char_2) - self._get_val(char_1)
                remaining_chars.pop(0)
            else:
                total += self._get_val(char_1)

