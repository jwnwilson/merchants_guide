import logging

from .alien_translator import AlienTranslator
from .exceptions import InvalidInput
from .roman_numerials import RomanNumeralConverter
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
    galaxy_translator = GalaxyTranslator()
    output_str = galaxy_translator.translate(input_str)
    return output_str


class GalaxyTranslator():
    valid_start_phrases = {
        'amount': 'how much is',
        'credits': 'how many Credits is'
    }
    responses = {
        'invalid': 'I have no idea what you are talking about',
        'amount': '{} is {}',
        'credits': '{} is {} Credits'
    }

    def __init__(self):
        # Instance tools
        self.converter = RomanNumeralConverter()
        self.translator = AlienTranslator()
        # Instance translation variables
        self.reset_parsed_data()

    def reset_parsed_data(self):
        self.valid_input = False
        self.cleaned_string = None
        self.original_input = None
        self.parsed_data = {}
        self.response = None

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
        self.cleaned_string = clean_string(input_str)

        # Look for valid start to input
        for key, phrase in self.valid_start_phrases.items():
            if self.cleaned_string.startswith(phrase):
                self.valid_input = True
                self.response = self.responses[key]
                self.cleaned_string.remove(phrase)

        if not self.valid_input:
            raise InvalidInput('Start of input unrecognised')

        self.parsed_data['amount_strings'] = self.translator.get_amount(
            self.cleaned_string)
        self.parsed_data['value_strings'] = self.translator.get_value(
            self.cleaned_string)

    def translate(self, input_str):
        try:
            self.parse(input_str)
        except InvalidInput as e:
            logger.error('Invalid input: {}, {}'.format_map(
                input_str, str(e)))
            self.response = self.responses['invalid']

        if self.valid_input:

