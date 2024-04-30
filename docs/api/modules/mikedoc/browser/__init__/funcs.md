###### MikeDoc API Reference
[Home](/docs/api/README.md) | [Project](/README.md) | [Module](/docs/api/modules/mikedoc/browser/__init__/README.md) | [Source](/mikedoc/browser/__init__.py)

# Functions within module
> Module: [mikedoc.browser.\_\_init\_\_](/docs/api/modules/mikedoc/browser/__init__/README.md)

Here are functions exposed in the module:
- [browse](#browse)
- [inspect\_module](#inspect_module)
- [iter\_modules](#iter_modules)

## browse
Generator to iterate over each module info and the associated members' info.

```python
def browse(root_dir, pkg_dir):
    ...
```

| Parameter | Description |
| --- | --- |
| root\_dir | Project root directory path |
| pkg\_dir | Relative path to the root_dir indicating the package directory. Slash is the only allowed separator. Example: "my_package" or "src/my_package". |

### Value to yield
Yields a 2-tuple made of a `mikedoc.ModuleInfo` instance and an iterator representing
members of the current module. The members are `mikedoc.MemberInfo` info

<p align="right"><a href="#mikedoc-api-reference">Back to top</a></p>

## inspect\_module
Inspect a module object and returns a list of 2-tuples representing the module's members

```python
def inspect_module(module):
    ...
```

| Parameter | Description |
| --- | --- |
| module | a Python module object |

### Value to return
A list of 2-tuples. Each tuple is made of the name of a module member and the member itself.

<p align="right"><a href="#mikedoc-api-reference">Back to top</a></p>

## iter\_modules
Generator for iterating over modules

```python
def iter_modules(root_dir, pkg_dir):
    ...
```

| Parameter | Description |
| --- | --- |
| root\_dir | The project root directory |
| pkg\_dir | Relative path to the root_dir indicating the package directory. Slash is the only allowed separator. Example: "my_package" or "src/my_package". |

### Value to yield
Yields a 2-tuple made of a module and the list of 2-tuples (name and object)
representing its members.

<p align="right"><a href="#mikedoc-api-reference">Back to top</a></p>
