import logging

from currency_converter.alien_translator import AlienTranslator
from .exceptions import InvalidInput
from .roman_numerals import RomanNumeralConverter
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
    """
    Main interface for translating and converting strings words to 
    english values
    """
    valid_output_phrases = {
        'amount': 'how much is',
        'credits': 'how many Credits is',

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
        self._reset_parsed_data()

    def _reset_parsed_data(self):
        self.valid_output = False
        self.original_input = None
        self.parsed_data = {}
        self.response = None

    def _translate_string(self, cleaned_string, output_value):
        """
        Use our translator instance to parse and translate the remaining
        string after removing expected english parts
        Args:
            cleaned_string: 

        Returns:
            None
        """
        # Pick out translated words and store them separately
        translated_data = self.translator.translate(
            cleaned_string, output_value=output_value)

        if translated_data.get('output'):
            self.parsed_data['amount_strings'] = translated_data['amount_strings']
            self.parsed_data['value'] = translated_data['value']

    def _get_translate_string(self, cleaned_string):
        """
        Look for english phase at start of input and remove it after
        checking it is acceptable input then return cleaned string.
        Args:
            cleaned_string: 

        Returns:
            (str) cleaned string
        """
        for key, phrase in self.valid_output_phrases.items():
            phrase = phrase.lower()
            if cleaned_string.startswith(phrase):
                self.valid_output = True
                self.response = self.responses[key]
                # Remove our expected non alien words
                cleaned_string = cleaned_string.replace(
                    phrase, '', 1).strip()
                break

        self.original_input = cleaned_string
        # Value words are capitalized
        for word in self.translator.values:
            self.original_input = self.original_input.replace(
                word, word.title())

        return cleaned_string

    def _calculate_amount(self):
        """
        Calculate the total value to return in the response from parsed data, 
        stores in instance parsed data.
        
        Returns:
            None
        """
        # TODO: Move me to translator, should not need to access converter
        # data
        self.parsed_data['amount'] = self.converter.get_amount(
            self.parsed_data['amount_strings'])

        self.parsed_data['total_amount'] = int(
            self.parsed_data['amount'] * self.parsed_data['value'])

    def _parse(self, input_str):
        """
        Validate input and break the string into sub-strings to be translated
        by the translator instance, stores translated data in instance
        parsed_data attr
        
        Args:
            input_str: (str) string value to validate and break into
                separate lists of data to translate

        Returns:
            None
        """
        self._reset_parsed_data()
        cleaned_string = clean_string(input_str)
        to_translate = self._get_translate_string(cleaned_string)
        self._translate_string(to_translate, self.valid_output)

    def translate(self, input_str):
        """
        Main entry point for this class accepts input string and will return
        translated and converted string
        Args:
            input_str: (str) string value to validate and break into
                separate lists of data to translate

        Returns:
            (str) final translated and converted string
        """
        response = ''
        try:
            self._parse(input_str)
            if self.parsed_data:
                self._calculate_amount()
                response = self.response.format(
                    self.original_input, self.parsed_data['total_amount'])
            else:
                response = 'Input parsed.'
        except InvalidInput as e:
            logger.error('Invalid input: "{}", {}'.format(
                input_str, str(e)))
            response = self.responses['invalid']
        finally:
            self._reset_parsed_data()

        return response
