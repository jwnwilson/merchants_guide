import json
from json.decoder import JSONDecodeError
import logging
import re

from currency_converter.exceptions import InvalidInput
from currency_converter.roman_numerals import RomanNumeralConverter

logger = logging.getLogger(__name__)


class TranslateEngine:
    """
    This class is responsible for storing word / translation mappings and 
    for returning translations of words and values
    """
    converter_class = RomanNumeralConverter
    json_file = 'currency_converter/translations.json'

    def __init__(self):
        self.words = {}
        self.values = {}
        self.input_regex = {
            'words': [
                '([^0-9]+) is ([^0-9]+)',
            ],
            'values': [
                '([^0-9]+) ([^0-9]+) is (\d+) credits',
            ]
        }
        self.output_regex = [
            '([^0-9]+)'
        ]
        self.converter = self.converter_class()
        self.read_translation_file()

    def read_translation_file(self):
        with open(self.json_file, 'rb') as in_file:
            try:
                data = json.loads(in_file.read())
            except JSONDecodeError:
                logger.error(
                    "Unable to load json file, starting with empty dict")
                data = {}
            self.words = data.get('words', {})
            self.values = data.get('values', {})

    def write_translation_file(self):
        with open(self.json_file, 'wb') as out_file:
            data = {
                'words': self.words,
                'values': self.values
            }
            data_str = json.dumps(data, indent=4)
            out_file.write(data_str.encode('utf-8'))

    def add_word(self, word):
        self.words.update(word)

    def add_value(self, value):
        self.values.update(value)

    def output_from_string(self, cleaned_string):
        """
        Return output to stdout based on input given from user.
        Args:
            cleaned_string: cleaned input str without invalid chars

        Returns:
            (dict): contain translated words and translated values
        """
        translated_data = {
            'output': True
        }
        # Handle alien numbers and keep them together
        translated_strings = self.get_amount_strings(cleaned_string)
        translated_data['amount_strings'] = translated_strings['translated']
        remaining_strings = translated_strings['remaining']

        if len(remaining_strings) > 1:
            raise InvalidInput('Multiple remaining strings detected 1 '
                               'expected: {}'.format(
                str(translated_strings['remaining'])))

        if remaining_strings:
            translated_data['value'] = self.get_value(remaining_strings[0])
        else:
            translated_data['value'] = 1
        return translated_data

    def _get_regex_results(self, cleaned_string):
        """
        Use regex to get the expected values we are after from the string
        Args:
            cleaned_string: 

        Returns:
            (tuple): (regex key, regex results) or (None, None)
        """
        for key in self.input_regex:
            for reg in self.input_regex[key]:
                values = re.search(reg, cleaned_string)
                reg_key = key
                if values:
                    return reg_key, values
        return None, None

    def input_from_string(self, cleaned_string):
        """
        Store inputted values from strings parsed from input.
        Args:
            cleaned_string: string without invalid characters

        Returns:
            (dict) contains meta data
        """
        translated_data = {
            'output': False
        }
        reg_key, values = self._get_regex_results(cleaned_string)

        if reg_key == 'words':
            values = {values[1]: values[2]}
            self.add_word(values)
        elif reg_key == 'values':
            alien_words = self.output_from_string(values[1])
            amount = self.converter.get_amount(alien_words['amount_strings'])
            values = {values[2]: (float(values[3]) / amount)}
            self.add_value(values)

        self.write_translation_file()

        return translated_data

    def translate(self, cleaned_string, output_value=False):
        """
        Break up string into words and translate them using our stored
        dicts of word mappings.
        
        Args:
            cleaned_string: 

        Returns:
            (dict): dict containing metadata and translation data
        """
        # Test that cleaned string only has terms we expect
        self.validate(cleaned_string, output_value=output_value)

        if output_value:
            translated_data = self.output_from_string(cleaned_string)
        else:
            translated_data = self.input_from_string(cleaned_string)

        return translated_data

    def get_amount_strings(self, cleaned_string):
        """
        Amount strings are the strings we expect to translate to roman
        numerals.
        
        Args:
            cleaned_string: 

        Returns:

        """
        translated = []
        remaining = []
        for word in cleaned_string.split():
            if word in self.words:
                translated.append(self.words[word])
            else:
                remaining.append(word)
        return {
            'translated': translated,
            'remaining': remaining
        }

    def get_value(self, cleaned_string):
        """
        The Value string is the object with value after the
        roman numeral characters this function returns its value.
        
        Args:
            cleaned_string: 

        Returns:
            (int) integer value from string value map
            
        Raises:
            InvalidInput if cleaned_string is not found in values word map
        """
        try:
            return self.values[cleaned_string]
        except KeyError:
            raise InvalidInput('"{}" is not a valid alien value'.format(
                cleaned_string
            ))

    def validate(self, cleaned_string, output_value):
        """
        Will raise an error if words in the string are not recognised from
        our word maps and will identify if string is input string or if string
        if requesting output
        
        Args:
            cleaned_string:
            
        Returns:
            (bool): return input regex matches

        Raises:
            InvalidInput
        """
        if output_value:
            # Valid output strings will be in word banks
            valid = True
            valid_values = list(self.words.keys()) + list(self.values.keys())

            for word in cleaned_string.split():
                if word not in valid_values:
                    valid = False
        else:
            # Valid input strings will be identified by regex
            valid = False
            reg_lists = [
                item for sublist in self.input_regex.values() for item in
                sublist]

            for reg in reg_lists:
                if re.search(reg, cleaned_string):
                    valid = True
                    break

        if not valid:
            raise InvalidInput(
                '"{}" is an unknown phase to translate'.format(cleaned_string))
