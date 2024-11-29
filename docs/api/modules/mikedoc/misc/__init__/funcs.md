###### Mikedoc API Reference
[Home](/docs/api/README.md) | [Project](/README.md) | [Module](/docs/api/modules/mikedoc/misc/__init__/README.md) | [Source](/src/mikedoc/misc/__init__.py)

# Functions within module
> Module: [mikedoc.misc.\_\_init\_\_](/docs/api/modules/mikedoc/misc/__init__/README.md)

Here are functions exposed in the module:
- [parse\_docstring](#parse_docstring)

## parse\_docstring
Parse a MikeDoc docstring

```python
def parse_docstring(docstring):
    ...
```

| Parameter | Description |
| --- | --- |
| docstring | String to parse |

### Value to return
A dictionary containing:
- the Description section (whose key is an empty string),
- the Parameters section (whose key is "param"),
- the Return section (whose key is "return"),
- the Yield section (whose key is "yield"),
- and the Exceptions section (whose key is "except").

Note that Parameters and the Exceptions sections are hyphenated list sections.
Therefore, the value of the dictionary key "param" or "except" is not a string
but a dictionary whose keys represent the parameters/exception classes and whose
values are description/circumstance strings. The empty key represents the intro.

<p align="right"><a href="#mikedoc-api-reference">Back to top</a></p>
