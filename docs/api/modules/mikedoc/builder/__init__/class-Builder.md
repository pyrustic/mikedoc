###### Mikedoc API Reference
[Home](/docs/api/README.md) | [Project](/README.md) | [Module](/docs/api/modules/mikedoc/builder/__init__/README.md) | [Source](/mikedoc/builder/__init__.py)

# Class Builder
> Module: [mikedoc.builder.\_\_init\_\_](/docs/api/modules/mikedoc/builder/__init__/README.md)
>
> Class: **Builder**
>
> Inheritance: `object`

Class to build the API reference

## Properties table
Here are properties exposed in the class:

| Property | Methods | Description |
| --- | --- | --- |
| api\_dir | _getter_ | No docstring. |
| pkg\_dir | _getter_ | No docstring. |
| project\_name | _getter_ | No docstring. |
| project\_url | _getter_ | No docstring. |
| root\_dir | _getter_ | No docstring. |

<p align="right"><a href="#mikedoc-api-reference">Back to top</a></p>

# Methods within class
Here are methods exposed in the class:
- [\_\_init\_\_](#__init__)
- [build](#build)
- [\_create\_class\_page](#_create_class_page)
- [\_create\_fields\_page](#_create_fields_page)
- [\_create\_funcs\_page](#_create_funcs_page)
- [\_create\_home\_page](#_create_home_page)
- [\_create\_overview\_page](#_create_overview_page)

## \_\_init\_\_
Init

```python
def __init__(self, root_dir, project_name, project_url, pkg_dir, api_dir):
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

## build
Build the API reference

```python
def build(self):
    ...
```

<p align="right"><a href="#mikedoc-api-reference">Back to top</a></p>

## \_create\_class\_page
No docstring

```python
def _create_class_page(self, module_info, class_info):
    ...
```

<p align="right"><a href="#mikedoc-api-reference">Back to top</a></p>

## \_create\_fields\_page
No docstring

```python
def _create_fields_page(self, module_info, fields):
    ...
```

<p align="right"><a href="#mikedoc-api-reference">Back to top</a></p>

## \_create\_funcs\_page
No docstring

```python
def _create_funcs_page(self, module_info, funcs):
    ...
```

<p align="right"><a href="#mikedoc-api-reference">Back to top</a></p>

## \_create\_home\_page
No docstring

```python
def _create_home_page(self, modules):
    ...
```

<p align="right"><a href="#mikedoc-api-reference">Back to top</a></p>

## \_create\_overview\_page
No docstring

```python
def _create_overview_page(self, module_info, fields, funcs, classes):
    ...
```

<p align="right"><a href="#mikedoc-api-reference">Back to top</a></p>
