from .alien_values import WORDS, VALUES
from ..exceptions import InvalidInput


class AlienTranslator():
    words = WORDS
    values = VALUES

    @classmethod
    def get_amount_strings(cls, cleaned_string):
        try:
             return [cls.words[x] for x in cleaned_string.split()]
        except KeyError:
            raise InvalidInput('"{}" contains invalid alien words'.format(
                cleaned_string
            ))

    @classmethod
    def get_value(cls, cleaned_string):
        try:
            return cls.values[cleaned_string]
        except KeyError:
            raise InvalidInput('"{}" is not a valid alien value'.format(
                cleaned_string
            ))

    @classmethod
    def validate(cls, cleaned_string):
        valid_words = cls.words.keys() + cls.values.keys()

        for word in cleaned_string.split():
            if word not in valid_words:
                raise InvalidInput('"{}" is an invalid word to translate'.format(
                    word
                ))