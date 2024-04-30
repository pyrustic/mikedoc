###### MikeDoc API Reference
[Home](/docs/api/README.md) | [Project](/README.md) | [Module](/docs/api/modules/mikedoc/__init__/README.md) | [Source](/mikedoc/__init__.py)

# Class ClassMemberInfo
> Module: [mikedoc.\_\_init\_\_](/docs/api/modules/mikedoc/__init__/README.md)
>
> Class: **ClassMemberInfo**
>
> Inheritance: `tuple`

Named tuple representing a member of a class

## Fields table
Here are fields exposed in the class:

| Field | Description |
| --- | --- |
| name | The name of the member. This isn't a dotted name. |
| obj | The object representing the member. |
| doc | The docstring of the member, parsable with `mikedoc.parse_docstring`. The field is set to `None` in absence of docstring. |
| signature | The signature string if it is available, otherwise, None. |
| lineage | List of bases classes where the class member  has been overridden or defined. The list goes from the most recent change to the first definition. |
| is\_field | Boolean to tells whether the member is a field or not |
| is\_property | Boolean to tells whether the member is a property or not |
| is\_method | Boolean to tells whether the member is a method or not |

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
Make a new ClassMemberInfo object from a sequence or iterable

```python
@classmethod
def _make(iterable):
    ...
```

<p align="right"><a href="#mikedoc-api-reference">Back to top</a></p>

## \_replace
Return a new ClassMemberInfo object replacing specified fields with new values

```python
def _replace(self, /, **kwds):
    ...
```

<p align="right"><a href="#mikedoc-api-reference">Back to top</a></p>
