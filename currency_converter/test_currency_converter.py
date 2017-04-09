import pytest

from .converter import GalaxyTranslator, translate_input


class TestGalaxyTranslatorOutput():
    def setup_method(self, method):
        self.translator = GalaxyTranslator()

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
