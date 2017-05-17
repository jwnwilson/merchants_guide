Author: Noel Wilson
Email: jwnwilson@hotmail.co.uk
Date: 09/04/2016

# Galaxy Currency Converter

This project is written in python 3 and tested on OSX but should run on any linux based terminal.

## Setting up the project

To be able to run the project and tests please run in a terminal:

$ source py_venv.sh

## Runing the project

(optional input for setting variables)

$ python translate.py --input "glob is I"

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


# Challenge notes

You decided to give up on earth after the latest financial collapse left 99.99% of the earth's population with 0.01% of the wealth. Luckily, with the scant sum of money that is left in your account, you are able to afford to rent a spaceship, leave earth, and fly all over the galaxy to sell common metals and dirt (which apparently is worth a lot).

Buying and selling over the galaxy requires you to convert numbers and units, and you decided to write a program to help you.

The numbers used for intergalactic transactions follows similar convention to the roman numerals and you have painstakingly collected the appropriate translation between them.

Roman numerals are based on seven symbols:

Symbol

Value

I   1

V   5

X   10

L   50

C   100

D   500

M   1,000


Numbers are formed by combining symbols together and adding the values. For example, MMVI is 1000 + 1000 + 5 + 1 = 2006. Generally, symbols are placed in order of value, starting with the largest values. When smaller values precede larger values, the smaller values are subtracted from the larger values, and the result is added to the total. For example MCMXLIV = 1000 + (1000 - 100) + (50 - 10) + (5 - 1) = 1944.

The symbols "I", "X", "C", and "M" can be repeated three times in succession, but no more. (They may appear four times if the third and fourth are separated by a smaller value, such as XXXIX.) "D", "L", and "V" can never be repeated.
"I" can be subtracted from "V" and "X" only. "X" can be subtracted from "L" and "C" only. "C" can be subtracted from "D" and "M" only. "V", "L", and "D" can never be subtracted.
Only one small-value symbol may be subtracted from any large-value symbol.
A number written in Arabic numerals can be broken into digits. For example, 1903 is composed of 1, 9, 0, and 3. To write the Roman numeral, each of the non-zero digits should be treated separately. In the above example, 1,000 = M, 900 = CM, and 3 = III. Therefore, 1903 = MCMIII.
(Source: Wikipedia http://en.wikipedia.org/wiki/Roman_numerals)

Input to your program consists of lines of text detailing your notes on the conversion between intergalactic units and roman numerals.

You are expected to handle invalid queries appropriately.

## Updated spec:

Parse input and calculate value of alien words, use translated words to calculate credit value of ores.

Test input:

<pre>
glob is I
prok is V
pish is X
tegj is L
glob glob Silver is 34 Credits
glob prok Gold is 57800 Credits
pish pish Iron is 3910 Credits
how much is pish tegj glob glob ?
how many Credits is glob prok Silver ?
how many Credits is glob prok Gold ?
how many Credits is glob prok Iron ?
how much wood could a woodchuck chuck if a woodchuck could chuck wood ?
</pre>

Test Output:
<pre>
pish tegj glob glob is 42
glob prok Silver is 68 Credits
glob prok Gold is 57800 Credits
glob prok Iron is 782 Credits
I have no idea what you are talking about
</pre>
