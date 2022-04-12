

# T-REST by [@pludi14](https://github.com/pludi14)

T-REST is a REST API security testing framework that contains tools and features especially for testing REST APIs.<br>
It offers the possibility to create custom test scripts and run those in this framework. 
The class `TREST_Framework()` can be used in custom scripts and offers usable methods and functions.

PICTURE!!!!

## Table of contents

- [Usage](#usage)
  - [Flags](#flags)
  - [Menu Options](#menu options)
- [Requirements](#requirements)
- [Installation](#installation)
- [Example Module](#example module)
- [T-REST Class](#T-REST Class)


## Usage

1. Start the framework:
  ```bash
  python main.py [-dsp]
  ```
2. Choose an option from menu:
  ```bash
  Menu: 
  m: Run modules 
  p: Show parser menu 
  r: Enable/Disable report generation. Status: True
  h: Show this menu again 
  q: Quit program
  ```

### Flags
- `-d`   OpenAPI specification file path
- `-s`   Service base URL - Example: https://server.com/api/v1/
- `-p`   Port of the target application

### Menu Options
MUSS NOCH GESTALTET WERDEN!!!!

## Requirements

Install required Python packages:
  ```bash
  pip install requests, asyncio, certifi
  ```

## Installation

Download program files from the Github repository: 
  ```bash
  git clone https://github.com/pludi14/T-REST
  ```

## Example Module


To create custom modules please use the following code snippets and customise your module: <br>
```python
# Import T-REST framework class
from main import TREST_Framework

# Create object of T-REST Framework 
trest=TREST_Framework() 

# Create own exception class
class Moduleexception(Exception): 
    pass

#Example function
def foo(error=False):
    print("You've executed the example module!")
    if error:
        raise Moduleexception("This is an example error message in example module.")

# run() method must be available in order to run this module
def run(): 
    try:
        foo(error=False) # Raise exception if error=True
    except Moduleexception as e:
        raise Moduleexception("This is an Exception Message")
    
    return "This is the report of the example module."
```

Save your custom modules in the ``./modules`` folder and choose execute them in the modules menu option.

[(Back to top)](#table-of-contents)