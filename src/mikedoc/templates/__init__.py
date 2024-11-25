__all__ = []

HOME_PAGE = """\
# {project_name} API Reference
Here are modules that make up [{project_name}]({project_url}):

{contents}

{back_to_top}
"""


OVERVIEW_PAGE = """\
{header_div}

# Module Overview
> Module: **{module_name}**

{description}

{members}
"""


FIELDS_PAGE = """\
{header_div}

# Fields within module
> Module: [{module_name}]({module_api_url})

Here are fields exposed in the module:

| Field | Value |
| --- | --- |
{entries}

{back_to_top}
"""


FUNCS_DOC_PAGE = """\
{header_div}

# Functions within module
> Module: [{module_name}]({module_api_url})

Here are functions exposed in the module:
{index_of_funcs}

{contents}
"""


CLASS_DOC_PAGE = """\
{header_div}

# Class {class_name}
> Module: [{module_name}]({module_api_url})
>
> Class: **{class_name}**
>
> Inheritance: {inheritance}

{description}

{contents}
"""


HEADER_DIV_1 = """\
###### {project_name} API Reference
[Home]({home_url}) | [Project]({project_url}) | Module | [Source]({src_url})"""


HEADER_DIV_2 = """\
###### {project_name} API Reference
[Home]({home_url}) | [Project]({project_url}) | [Module]({api_url}) | [Source]({src_url})"""


MODULE_LINE = """\
[{module_name}]({api_url})
<br>
{short_description}"""


ALL_FUNCTIONS_SECTION = """\
## Functions
- [**All functions**]({funcs_page_url})
{contents}

{back_to_top}"""


ALL_CLASSES_SECTION = """\
## Classes
{contents}

{back_to_top}"""


ALL_FIELDS_SECTION = """\
## Fields
- [**All fields**]({fields_page_url})
{contents}

{back_to_top}"""


FUNC_LINE = """\
    - [{name}]({doc_url}): {short_description}"""


CLASS_SECTION = """\
- [**{name}**]({doc_url}): {short_description}
{contents}"""


CLASS_MEMBER_LINE = """\
    - [{name}]({doc_url}){kv_sign} {short_description}"""


FIELD_LINE = """\
    - {name} = {value}"""


TWO_COLUMNS_TABLE_ENTRY = """\
| {col1} | {col2} |"""


THREE_COLUMNS_TABLE_ENTRY = """\
| {col1} | {col2} | {col3} |"""


METHODS_SECTION = """\
# Methods within class
Here are methods exposed in the class:
{index_of_methods}

{contents}"""


FUNC_DOC_SECTION = """\
## {func_name_1}
{description}

```python
{decorator}def {func_name_2}{signature}:
    ...
```

{contents}"""


BACK_TO_TOP = """\
<p align="right"><a href="{href}">Back to top</a></p>"""


FUNC_PARAMS_TABLE = """\
| Parameter | Description |
| --- | --- |
{contents}"""


FUNC_EXCEPTIONS_SECTION = """\
### Exceptions table
{contents}"""


FUNC_EXCEPTIONS_TABLE = """\
| Exception | Circumstance |
| --- | --- |
{contents}"""


FUNC_RETURNS_LINE = """\
### Value to return
{text}"""


FUNC_YIELDS_LINE = """\
### Value to yield
{text}"""


FIELDS_EXPOSED_IN_CLASS = """\
## Fields table
Here are fields exposed in the class:

| Field | Value |
| --- | --- |
{contents}

{back_to_top}"""


PROPERTIES_EXPOSED_IN_CLASS = """\
## Properties table
Here are properties exposed in the class:

| Property | Methods | Description |
| --- | --- | --- |
{contents}

{back_to_top}"""


FIELDS_EXPOSED_IN_NAMEDTUPLE = """\
## Fields table
Here are fields exposed in the class:

| Field | Description |
| --- | --- |
{contents}

{back_to_top}"""


FIELDS_EXPOSED_IN_ENUM = """\
## Fields table
Here are fields exposed in the class:

| Field | Value |
| --- | --- |
{contents}

{back_to_top}"""
