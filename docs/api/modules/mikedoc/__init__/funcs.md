###### Mikedoc API Reference
[Home](/docs/api/README.md) | [Project](/README.md) | [Module](/docs/api/modules/mikedoc/__init__/README.md) | [Source](/src/mikedoc/__init__.py)

# Functions within module
> Module: [mikedoc.\_\_init\_\_](/docs/api/modules/mikedoc/__init__/README.md)

Here are functions exposed in the module:
- [browse](#browse)
- [build](#build)
- [parse\_docstring](#parse_docstring)

## browse
Generator to iterate through each module info and the associated members' info.

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

## build
Build the API reference (Markdown files) in the api directory

```python
def build(root_dir, project_name, project_url, pkg_dir, api_dir):
    ...
```

| Parameter | Description |
| --- | --- |
| root\_dir | The project root directory |
| project\_name | The public (stylized or not) name of the project. Example, a project named `MyProject` might have `my_project` as package name and `my-project` as project directory name. |
| project\_url | The url to the project, it might be the relative url to the README.md file |
| pkg\_dir | Relative path to the root_dir indicating the package directory. Slash is the only allowed separator. Example: "my_package" or "src/my_package |
| api\_dir | Relative path to the root_dir indicating the api reference directory. Slash is the only allowed separator. Example: "docs/api". |

<p align="right"><a href="#mikedoc-api-reference">Back to top</a></p>

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
