<h1 align="center">
<img src="./icon.png" width="300"><br>
T-REST by <a href="https://github.com/pludi14">@pludi14</a>
</h1>

T-REST is a REST API security testing framework that contains tools and features especially for testing REST APIs.<br>
It offers the possibility to create custom test scripts and run those in this framework. 
The class `TREST_Framework()` can be used in custom scripts and offers usable methods.



## Table of contents

- [Usage](#usage)
  - [Parameters](#parameters)
- [Run Modules](#run-modules)
- [Requirements](#requirements)
- [Installation](#installation)
- [Example Module](#example-module)
- [T-REST Class](#t-rest-class)


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

### Parameters
- `-d`   OpenAPI specification file path
- `-s`   Service base URL - Example: https://server.com/api/v1/
- `-p`   Port of the target application

## Run Modules
Choose the module that needs to be run from menu by using the numbers. <br>
Run one specific `1`, more than one `0,1,2`, or all `a`.

```bash
Modules found in folder /Users/mpludra/PycharmProjects/T-REST/modules/:
0:	Example_Module.py
1:	dos.py
2:	tlscheck.py
a:	Run all modules
b:	Go back
Please select the modules you want to run: 
```

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
**Important:** The `run()` method must be available in order to run this module.

Save your custom modules in the ``./modules`` folder and execute them in the modules menu option.

## T-REST Class

#### Create object of T-REST Class
```python
# Import T-REST framework class
from main import TREST_Framework

# Create object of T-REST Framework 
trest=TREST_Framework() 
```
<br>

#### Get server base URL
```bash
  trest.get_server()
``` 

|Type     | Description     | Example                       |
|:------- |:----------------|:------------------------------|
|`string` | Server base URL | `https://server.com/api/v1/`  |

<br>

#### Get port number
```bash
  trest.get_port()
``` 

| Type  | Description | Example |
|:------|:------------|:--------|
| `int` | Server port | `443`   |

<br>

#### Get hostname from URL
```bash
trest.get_hostname()
```

|Type     | Description     | Example     |
|:------- |:----------------|:------------|
|`string` | Server hostname | `server.com` |

<br>

#### Get connection protocol
```bash
trest.get_protocol()
```
  
|Type     | Description         | Example           |
|:------- |:--------------------|:------------------|
|`string` | Connection protocol | `http` or `https` |

<br>

#### Get all paths from OpenAPI specification
```bash
trest.get_all_paths()
```

| Type   | Description                               | Example                        |
|:-------|:------------------------------------------|:-------------------------------|
| `list` | All paths from OpenAPI specification file | `['/v1/', '/v1/manufacturer/']` |

<br>

#### Get all paths + additional path information
```bash
trest.get_all_pathdata()
```

| Type   | Description                                                    |
|:-------|:---------------------------------------------------------------|
| `dict` | All paths and path information from OpenAPI specification file | 
Example:
```json
{
  "/v1/": { 
    "head": { 
      "summary": "Root",
      "operationId": "root_v1__head",
      "responses": {
        "200": {
          "description": "Successful Response",
          "content": {
            "application/json": {
              "schema": {}
            }
          }
        }
      }
    }
  }
}
```

<br>

#### Get all paths + path method and path parameters
Similar to `get_all_pathdata()` but provides only relevant path information.

```bash
trest.get_all_path_info()
```

| Type   | Description                                                     |
|:-------|:----------------------------------------------------------------|
| `dict` | All paths and specific path information (method and parameters) |

Example:
```json
{
  "/v1/manufacturer/": {
    "get": null,
    "post": {
      "Name": "string",
      "Location": "string"
    }
  }
}
```

<br>

#### Get a random integer value

```bash
trest.get_random_integer(start, end)
```

| Type  | Description          | Parameters                               |
|:------|:---------------------|:-----------------------------------------|
| `int` | Random integer value | Number between `start:int` and `end:int` |

<br>

#### Get a random string value

```bash
trest.get_random_string(lenght)
```

|Type     | Description         | Parameter                      |
|:------- |:--------------------|:-------------------------------|
|`string` | Random string value | Lenghts of string `lenght:int` |
  

[(Back to top)](#table-of-contents)


