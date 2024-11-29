###### Mikedoc API Reference
[Home](/docs/api/README.md) | [Project](/README.md) | [Module](/docs/api/modules/mikedoc/builder/__init__/README.md) | [Source](/src/mikedoc/builder/__init__.py)

# Functions within module
> Module: [mikedoc.builder.\_\_init\_\_](/docs/api/modules/mikedoc/builder/__init__/README.md)

Here are functions exposed in the module:
- [build](#build)

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
