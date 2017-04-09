from .alien_values import WORDS, VALUES
from ..exceptions import InvalidInput


class AlienTranslator():
    words = WORDS
    values = VALUES

    @classmethod
    def get_amount_strings(cls, cleaned_string):
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
        try:
            return cls.values[cleaned_string]
        except KeyError:
            raise InvalidInput('"{}" is not a valid alien value'.format(
                cleaned_string
            ))

    @classmethod
    def validate(cls, cleaned_string):
        valid_words = list(cls.words.keys()) + list(cls.values.keys())

        for word in cleaned_string.split():
            if word not in valid_words:
                raise InvalidInput('"{}" is an invalid word to '
                    'translate'.format(word))