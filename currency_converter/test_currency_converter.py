import pytest

from .converter import GalaxyCurrencyConverter, translate_input
from .exceptions import InvalidInput
from .roman_numerals import RomanNumeralConverter
from .translations.alien_translator import AlienTranslator
from .utils import clean_string


class TestGalaxyConverterOutput():
    def setup_method(self, method):
        self.translator = GalaxyCurrencyConverter()

    def test_non_alpha_characters(self):
        output_str = translate_input('how much is 1 tegj glob glob?')
        assert output_str == 'tegj glob glob is 52'

    def test_amount_translation(self):
        output_str = translate_input('how much is pish tegj glob glob')
        assert output_str == 'pish tegj glob glob is 42'

    @pytest.mark.parametrize("input_str,expected_str", [
        ('how many Credits is glob prok Silver ?',
         'glob prok Silver is 68 Credits'),
        ('how many Credits is glob prok Gold ?',
         'glob prok Gold is 57800 Credits'),
        ('how many Credits is glob prok Iron ?',
         'glob prok Iron is 782 Credits')

    ])
    def test_amount_credits_translation(self, input_str, expected_str):
        output_str = translate_input(input_str)
        assert output_str == expected_str

    def test_invalid_translation(self):
        output_str = translate_input(
            'how much wood could a woodchuck chuck if a woodchuck '
            'could chuck wood ?')
        assert output_str == 'I have no idea what you are talking about'

    def test_clean_input_string(self):
        pass

    def test_validate_string_return_values(self):
        pass

    def test_parse_loads_currect_data(self):
        pass

    def test_calculate_amount_correct_total(self):
        pass



class TestRomanNumerals():
    def setup_method(self, method):
        self.r_converter = RomanNumeralConverter()

    @pytest.mark.parametrize("input_list,expected_value", [
        (['l', 'i', 'i'], 52),
        (['x', 'l', 'i'], 41),
    ])
    def test_get_amount_results(self, input_list, expected_value):
        output_val = self.r_converter.get_amount(input_list)
        assert output_val == expected_value

    @pytest.mark.parametrize("input_str_1,input_str_2,expected_bool", [
        ('i', 'v', True),
        ('i', 'x', True),
        ('v', 'x', False),
        ('x', 'l', True),
        ('i', 'l', False)
    ])
    def test_is_subtractable_result(self, input_str_1, input_str_2, expected_bool):
        test_result = self.r_converter._is_subtractable(input_str_1, input_str_2)
        assert test_result == expected_bool

    @pytest.mark.parametrize("input_str,expected_val", [
        ('i', 1),
        ('v', 5),
        ('x', 10),
        ('l', 50)
    ])
    def test_get_val_result(self, input_str, expected_val):
        test_result = self.r_converter._get_val(input_str)
        assert test_result == expected_val

    @pytest.mark.parametrize("input_str", [
        'iiii',
        'vvvv',
        'xxxx'
    ])
    def test_get_amount_results_invalid_input(self, input_str):
        with pytest.raises(InvalidInput):
            test_result = self.r_converter._get_val(input_str)


class TestAlienTranslator():
    def setup_method(self, method):
        self.translator = AlienTranslator()

    @pytest.mark.parametrize("input_str,expected_list", [
        ('tegj glob glob', ['l', 'i', 'i']),
        ('pish tegj glob', ['x', 'l', 'i'])
    ])
    def test_get_amount_strings_returned_values(self, input_str, expected_list):
        output_list = self.translator.get_amount_strings(input_str)
        assert output_list['translated'] == expected_list

    @pytest.mark.parametrize("input_str,expected_num", [
        ('gold', 14450),
        ('silver', 17),
        ('iron', 195.5)
    ])
    def test_get_value_returned_values(self, input_str, expected_num):
        output_val = self.translator.get_value(input_str)
        assert output_val == expected_num

    @pytest.mark.parametrize("input_str", [
        'gold',
        'silver',
        'iron',
        'glob',
        'prok',
        'pish',
        'tegj'
    ])
    def test_validate_valid_results(self, input_str):
        self.translator.validate(input_str)

    @pytest.mark.parametrize("input_str", [
        'test',
        'batman',
        'robin',
        'spiderman'
    ])
    def test_validate_invalid_results(self, input_str):
        with pytest.raises(InvalidInput):
            self.translator.validate(input_str)


class TestUtils():
    def test_clean_string(self):
        non_alpha_numeric = 'th!s is, a. "\' TESt?111'
        clean_str = clean_string(non_alpha_numeric)

        assert clean_str == 'th s is a test'
