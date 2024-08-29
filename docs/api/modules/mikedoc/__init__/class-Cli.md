###### Mikedoc API Reference
[Home](/docs/api/README.md) | [Project](/README.md) | [Module](/docs/api/modules/mikedoc/__init__/README.md) | [Source](/mikedoc/__init__.py)

# Class Cli
> Module: [mikedoc.\_\_init\_\_](/docs/api/modules/mikedoc/__init__/README.md)
>
> Class: **Cli**
>
> Inheritance: `object`

Command-line interface class

## Properties table
Here are properties exposed in the class:

| Property | Methods | Description |
| --- | --- | --- |
| root\_dir | _getter_ | No docstring. |
| silent\_mode | _getter, setter_ | No docstring. |

<p align="right"><a href="#mikedoc-api-reference">Back to top</a></p>

# Methods within class
Here are methods exposed in the class:
- [\_\_init\_\_](#__init__)
- [echo](#echo)
- [run](#run)
- [\_build\_api\_reference](#_build_api_reference)
- [\_create\_config\_file](#_create_config_file)
- [\_load\_config](#_load_config)

## \_\_init\_\_
Init

```python
def __init__(self, root_dir, silent_mode=False):
    ...
```

| Parameter | Description |
| --- | --- |
| root\_dir | Path the project root directory |
| silent\_mode | Boolean to tell whether output should be printed or not |

<p align="right"><a href="#mikedoc-api-reference">Back to top</a></p>

## echo
Print text if `silent_mode` is False

```python
def echo(self, text):
    ...
```

<p align="right"><a href="#mikedoc-api-reference">Back to top</a></p>

## run
Run a command. Valid commands are `init`, `build` and `help`.

```python
def run(self, *args):
    ...
```

<p align="right"><a href="#mikedoc-api-reference">Back to top</a></p>

## \_build\_api\_reference
No docstring

```python
def _build_api_reference(self):
    ...
```

<p align="right"><a href="#mikedoc-api-reference">Back to top</a></p>

## \_create\_config\_file
No docstring

```python
def _create_config_file(self):
    ...
```

<p align="right"><a href="#mikedoc-api-reference">Back to top</a></p>

## \_load\_config
No docstring

```python
def _load_config(self):
    ...
```

<p align="right"><a href="#mikedoc-api-reference">Back to top</a></p>
