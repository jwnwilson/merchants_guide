import logging

from currency_converter.roman_numerals import RomanNumeralConverter
from .exceptions import InvalidInput
from .translations.alien_translator import AlienTranslator
from .utils import clean_string

logger = logging.getLogger(__name__)


def translate_input(input_str):
    """
    Wrapper around GalaxyTranslator() to translate an input str
    Args:
        input_str: input string in the format and with words we expect

    Returns:
        (str) output_string english translation and value from translated
        input
    """
    galaxy_translator = GalaxyCurrencyConverter()
    output_str = galaxy_translator.translate(input_str)
    return output_str


class GalaxyCurrencyConverter():
    valid_start_phrases = {
        'amount': 'how much is',
        'credits': 'how many Credits is'
    }
    responses = {
        'invalid': 'I have no idea what you are talking about',
        'amount': '{} is {}',
        'credits': '{} is {} Credits'
    }
    converter_class = RomanNumeralConverter
    translator_class = AlienTranslator

    def __init__(self):
        # Instance tools
        self.converter = self.converter_class()
        self.translator = self.translator_class()
        # Instance translation variables
        self.reset_parsed_data()

    def reset_parsed_data(self):
        self.valid_input = False
        self.original_input = None
        self.parsed_data = {}
        self.response = None

    def _translate_string(self, cleaned_string):
        """
        Use our tranlator instance to parse and translate the remaining
        string after removing expected english parts
        Args:
            cleaned_string: 

        Returns:

        """
        # Test that cleaned string only has terms we expect
        self.translator.validate(cleaned_string)

        self.parsed_data['amount_strings'] = self.translator.get_amount_strings(
            cleaned_string)
        self.parsed_data['value'] = self.translator.get_value(
            cleaned_string)

    def _validate_string(self, cleaned_string):
        """
        Look for english phase at start of input and remove it after
        checking it is acceptable input.
        Args:
            cleaned_string: 

        Returns:

        """
        for key, phrase in self.valid_start_phrases.items():
            if cleaned_string.startswith(phrase):
                self.valid_input = True
                self.response = self.responses[key]
                cleaned_string.remove(phrase)
                break

        if not self.valid_input:
            raise InvalidInput('Start of input unrecognised')

        return cleaned_string

    def _calculate_amount(self):
        self.parsed_data['amount'] = self.converter.get_amount(
            self.parsed_data['amount_strings'])

        self.parsed_data['total_amount'] = (
            self.parsed_data['amount'] * self.parsed_data['value'])

    def parse(self, input_str):
        """
        Validate input and break the string into different seconds
        to be translated.
        Args:
            input_str: (str) string value to validate and break into
                separate lists of data to translate

        Returns:
            None
        """
        self.reset_parsed_data()

        cleaned_string = clean_string(input_str)
        cleaned_string = self._validate_string(cleaned_string)

        self._translate_string(cleaned_string)

    def translate(self, input_str):
        try:
            self.parse(input_str)
            self._calculate_amount()
        except InvalidInput as e:
            logger.error('Invalid input: {}, {}'.format(
                input_str, str(e)))
            self.response = self.responses['invalid']

        return self.response.format(
            self.parsed_data['total_amount'])

