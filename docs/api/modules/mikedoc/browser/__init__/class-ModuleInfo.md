###### Mikedoc API Reference
[Home](/docs/api/README.md) | [Project](/README.md) | [Module](/docs/api/modules/mikedoc/browser/__init__/README.md) | [Source](/src/mikedoc/browser/__init__.py)

# Class ModuleInfo
> Module: [mikedoc.browser.\_\_init\_\_](/docs/api/modules/mikedoc/browser/__init__/README.md)
>
> Class: **ModuleInfo**
>
> Inheritance: `tuple`

Named tuple yielded by the `mikedoc.browse` generator. 
It contains info about one module

## Fields table
Here are fields exposed in the class:

| Field | Description |
| --- | --- |
| name | String representing the dotted name of the module. Note that for a module `package/__init__.py`, the dotted name would be `package.__init__` |
| obj | Alias for field number 1 |
| doc | The docstring of the module, parsable with `mikedoc.parse_docstring`. The field is set to `None` in absence of docstring. |

<p align="right"><a href="#mikedoc-api-reference">Back to top</a></p>

# Methods within class
Here are methods exposed in the class:
- [\_asdict](#_asdict)
- [\_make](#_make)
- [\_replace](#_replace)

## \_asdict
Return a new dict which maps field names to their values.

```python
def _asdict(self):
    ...
```

<p align="right"><a href="#mikedoc-api-reference">Back to top</a></p>

## \_make
Make a new ModuleInfo object from a sequence or iterable

```python
@classmethod
def _make(iterable):
    ...
```

<p align="right"><a href="#mikedoc-api-reference">Back to top</a></p>

## \_replace
Return a new ModuleInfo object replacing specified fields with new values

```python
def _replace(self, /, **kwds):
    ...
```

<p align="right"><a href="#mikedoc-api-reference">Back to top</a></p>
