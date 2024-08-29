###### Mikedoc API Reference
[Home](/docs/api/README.md) | [Project](/README.md) | [Module](/docs/api/modules/mikedoc/__init__/README.md) | [Source](/mikedoc/__init__.py)

# Class MemberInfo
> Module: [mikedoc.\_\_init\_\_](/docs/api/modules/mikedoc/__init__/README.md)
>
> Class: **MemberInfo**
>
> Inheritance: `tuple`

Named tuple representing a member of a module

## Fields table
Here are fields exposed in the class:

| Field | Description |
| --- | --- |
| name | The name of the member. This isn't a dotted name. |
| obj | The object representing the member. |
| doc | The docstring of the member, parsable with `mikedoc.parse_docstring`. The field is set to `None` in absence of docstring. |
| signature | The signature string if it is available, otherwise, None. |
| bases | List of bases class objects from which a class inherits from. This isn't the `mro` at all. This field is set to None when the member isn't a class |
| members | The list of members of a class.  This list contains `mikedoc.ClassMemberInfo` instances. If the member isn't a class, the list is set to None. |
| is\_field | Boolean telling whether the member is a field or not |
| is\_class | Boolean telling whether the member is a class or not |
| is\_func | Boolean telling whether the member is a func or not |

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
Make a new MemberInfo object from a sequence or iterable

```python
@classmethod
def _make(iterable):
    ...
```

<p align="right"><a href="#mikedoc-api-reference">Back to top</a></p>

## \_replace
Return a new MemberInfo object replacing specified fields with new values

```python
def _replace(self, /, **kwds):
    ...
```

<p align="right"><a href="#mikedoc-api-reference">Back to top</a></p>
