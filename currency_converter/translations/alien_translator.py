from .alien_values import WORDS, VALUES
from ..exceptions import InvalidInput


class AlienTranslator():
    words = WORDS
    values = VALUES

    @classmethod
    def translate(cls, cleaned_string):
        """
        Break up string into words and translate them using our stored
        dicts of word mappings.
        
        Args:
            cleaned_string: 

        Returns:

        """
        translated_data = {}
        # Handle alien numbers and keep them together
        translated_strings = cls.get_amount_strings(cleaned_string)
        translated_data['amount_strings'] = translated_strings['translated']
        remaining_strings = translated_strings['remaining']

        if len(remaining_strings) > 1:
            raise InvalidInput('Multiple remaining strings detected 1 '
                'expected: {}'.format(str(translated_strings['remaining'])))

        if remaining_strings:
            translated_data['value'] = cls.get_value(remaining_strings[0])
        else:
            translated_data['value'] = 1

        return translated_data

    @classmethod
    def get_amount_strings(cls, cleaned_string):
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
            if word in cls.words:
                translated.append(cls.words[word])
            else:
                remaining.append(word)
        return {
            'translated': translated,
            'remaining': remaining
        }

    @classmethod
    def get_value(cls, cleaned_string):
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
            return cls.values[cleaned_string]
        except KeyError:
            raise InvalidInput('"{}" is not a valid alien value'.format(
                cleaned_string
            ))

    @classmethod
    def validate(cls, cleaned_string):
        """
        Will raise an error if words in the string are not recognised from
        our word maps.
        
        Args:
            cleaned_string:
            
        Returns:
            none

        Raises:
            InvalidInput
        """
        valid_words = list(cls.words.keys()) + list(cls.values.keys())

        for word in cleaned_string.split():
            if word not in valid_words:
                raise InvalidInput('"{}" is an invalid word to '
                    'translate'.format(word))