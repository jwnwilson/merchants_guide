Author: Noel Wilson
Email: jwnwilson@hotmail.co.ik
Date: 09/04/2016

# Galaxy Currency Converter

This project is written in python 3 and tested on OSX but should run on any linux based terminal.

## Setting up the project

To be able to run the project and tests please run in a terminal:

$ source py_venv.sh

## Runing the project

$ python translate.py --input "how many Credits is glob prok Silver ?"

## Running tests:

$ pytest

## Coverage report:

$ py.test --cov-report html --cov=currency_converter --verbose
$ open htmlcov/index.html

# Notes:

## Structure

I have tried to separate out the responsibilities of each class and make it clear what each ones job is
to do in this project, the main converter class is the fascade that contains all other elements and passes
data from one element to another. The translater and converter classes are designed to be changed by sub classes
if need be as we should design code to be extendable without needing to edit the orginal. The translator handles
all translation logic, it did leak into the converter at one point but I tidied it back into that class. The
roman_numerals class handles the roman numeral -> number logic which is less documented as I think it's clearer
due to it's simplicity.

I've broken any functions up that start to do more than one task into multiples, the reasons for this is extendability
and maintainability and for easier testing. It's much easier to update the logic in a sub class if it's broken up, it's
easier to debug problems and we can write tests for each component to help avoid problems sooner.

I created a translations package as I though this would be the part most likely to expand first so thought it made
sense to do that pre-emptively. Roman_numerals and other converters would follow the same structure if they increased in
size although this would be discussion to be had with project managers to effectively plan ahead.

## Imports

I've used relative imports, I know this can be a problem for larger projects and was just a
choice I used as a preference for this task, I'd be happy to conform to the existing code base
if that wasn't the case. I know importing from the root is a little clearer on larger projects
and more common.

## Classmethods and extendability

I've set the translations and roman_numerial class functions to tbe classmethods
as they do not require the instance to hold any data so there's no reason to require
an instance to be made to use the functionality. I do still make instances of these classes
in the converter for the sake of extendability, if a more complicated process is needed
later that requires this they can use it without having to edit the converter class by subclassing
and overriding the class the GalaxyCurrencyConverter uses.

## Documentation

I'm trying to avoid redundant docstrings so I've deliberately chosen to not put some in some places
that I don't think they are needed. This would need a code review to tweak as I understand the
code and it's not as obvious to me what isn't as clear and needs more explaination.
