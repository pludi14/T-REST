"""
T-REST: This is an example module.
The run() method needs to be available since this method is used to run this module.
It is recommended to create custom Exceptions. Please use the base exception class as basis class.
"""

# Import T-REST Framework Methods and Attributes
from main import TREST_Framework

trest=TREST_Framework()

class Moduleexception(Exception):
    pass

def foo(error=False):
    print("You've executed the example module!")

    if error:
        raise Moduleexception("This is an example error message in example module.")


def run(): # This Method must be available in order to run this module.

    try:
        foo(error=False)
    except Moduleexception as e:
        raise Moduleexception("This is an Exception Message")

    return "This is the report of the example module."









