###### MikeDoc API Reference
[Home](/docs/api/README.md) | [Project](/README.md) | Module | [Source](/mikedoc/__init__.py)

# Module Overview
> Module: **mikedoc.\_\_init\_\_**

This module exposes public functions and classes useful for most cases.

## Functions
- [**All functions**](/docs/api/modules/mikedoc/__init__/funcs.md)
    - [browse](/docs/api/modules/mikedoc/__init__/funcs.md#browse): Generator to iterate over each module info and the associated members' info.
    - [build](/docs/api/modules/mikedoc/__init__/funcs.md#build): Build the API reference (Markdown files) in the api directory
    - [parse\_docstring](/docs/api/modules/mikedoc/__init__/funcs.md#parse_docstring): Parse a MikeDoc docstring

<p align="right"><a href="#mikedoc-api-reference">Back to top</a></p>

## Classes
- [**ClassMemberInfo**](/docs/api/modules/mikedoc/__init__/class-ClassMemberInfo.md): Named tuple representing a member of a class
    - name: The name of the member. This isn't a dotted name.
    - obj: The object representing the member.
    - doc: The docstring of the member, parsable with
`mikedoc.parse_docstring`. The field is set to `None` in absence of docstring.
    - signature: The signature string if it is available, otherwise, None.
    - lineage: List of bases classes where the class member
 has been overridden or defined. The list goes from the most recent change to the first definition.
    - is\_field: Boolean to tells whether the member is a field or not
    - is\_property: Boolean to tells whether the member is a property or not
    - is\_method: Boolean to tells whether the member is a method or not
- [**Cli**](/docs/api/modules/mikedoc/__init__/class-Cli.md): Command-line interface class
    - [root\_dir](/docs/api/modules/mikedoc/__init__/class-Cli.md#properties-table); _getter_
    - [silent\_mode](/docs/api/modules/mikedoc/__init__/class-Cli.md#properties-table); _getter, setter_
    - [echo](/docs/api/modules/mikedoc/__init__/class-Cli.md#echo): Print text if `silent_mode` is False
    - [run](/docs/api/modules/mikedoc/__init__/class-Cli.md#run): Run a command. Valid commands are `init`, `build` and `help`.
    - [\_build\_api\_reference](/docs/api/modules/mikedoc/__init__/class-Cli.md#_build_api_reference): No docstring.
    - [\_create\_config\_file](/docs/api/modules/mikedoc/__init__/class-Cli.md#_create_config_file): No docstring.
    - [\_load\_config](/docs/api/modules/mikedoc/__init__/class-Cli.md#_load_config): No docstring.
- [**MemberInfo**](/docs/api/modules/mikedoc/__init__/class-MemberInfo.md): Named tuple representing a member of a module
    - name: The name of the member. This isn't a dotted name.
    - obj: The object representing the member.
    - doc: The docstring of the member, parsable with
`mikedoc.parse_docstring`. The field is set to `None` in absence of docstring.
    - signature: The signature string if it is available, otherwise, None.
    - bases: List of bases class objects from which a class inherits from.
This isn't the `mro` at all. This field is set to None when the member isn't a class
    - members: The list of members of a class. 
This list contains `mikedoc.ClassMemberInfo` instances. If the member isn't a class, the list is set to None.
    - is\_field: Boolean telling whether the member is a field or not
    - is\_class: Boolean telling whether the member is a class or not
    - is\_func: Boolean telling whether the member is a func or not
- [**ModuleInfo**](/docs/api/modules/mikedoc/__init__/class-ModuleInfo.md): Named tuple yielded by the `mikedoc.browse` generator.  It contains info about one module
    - name: String representing the dotted name of the module.
Note that for a module `package/__init__.py`, the dotted name would be `package.__init__`
    - obj: Alias for field number 1
    - doc: The docstring of the module, parsable with
`mikedoc.parse_docstring`. The field is set to `None` in absence of docstring.

<p align="right"><a href="#mikedoc-api-reference">Back to top</a></p>
