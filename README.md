
Notes:

I've used relative imports, I know this can be a problem for larger projects and was just a
choice I used as a preference for this task, I'd be happy to conform to the existing code base
if that wasn't the case. I know importing from the root is a little clearer on larger projects
and more common.

I've set the translations and roman_numerial class functions to tbe classmethods
as they do not require the instance to hold any data so there's no reason to require
an instance to be made to use the functionality. I do still make instances of these classes
in the converter for the sake of extendability, if a more complicated process is needed
later that requires this they can use it without having to edit the converter class by subclassing
and overriding the class the converter uses.