from .alien_values import WORDS, VALUES
from ..exceptions import InvalidInput


class AlienTranslator():
    def __init___(self):
        self.words = WORDS
        self.values = VALUES

    def get_amount_strings(self, cleaned_string):
        try:
             return [self.words[x] for x in cleaned_string.split()]
        except KeyError:
            raise InvalidInput('"{}" contains invalid alien words'.format(
                cleaned_string
            ))

    def get_value(self, cleaned_string):
        try:
            return self.values[cleaned_string]
        except KeyError:
            raise InvalidInput('"{}" is not a valid alien value'.format(
                cleaned_string
            ))

    def validate(self, cleaned_string):
        valid_words = self.words.keys() + self.values.keys()

        for word in cleaned_string.split():
            if word not in valid_words:
                raise InvalidInput('"{}" is an invalid word to translate'.format(
                    word
                ))