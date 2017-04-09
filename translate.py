import argparse
import logging

from currency_converter.translator import translate_input

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument("--input")
    args = parser.parse_args()

    if not args.input:
        logger.error('Please supply string to translate')

    print(translate_input(args.input))
