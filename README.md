[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI package version](https://img.shields.io/pypi/v/mikedoc)](https://pypi.org/project/mikedoc)
[![Downloads](https://static.pepy.tech/badge/mikedoc)](https://pepy.tech/project/mikedoc)

<!-- Cover -->
<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/assets/mikedoc/cover.jpg" alt="Cover image" width="572">
    <p align="center"> 
    <a href="https://commons.wikimedia.org/wiki/File:Tavernier_Jean_Mielot.jpg">Jean Le Tavernier</a>, Public domain, via Wikimedia Commons
    </p>
</div>

<!-- Intro Text -->
# MikeDoc
<b>Neat docstring format for building API references</b>


## Table of contents
- [Overview](#overview)
- [Usage](#usage)
- [Demo](#demo)
- [Docstring format](#docstring-format)
- [Config file](#config-file)
- [Command-line interface](#command-line-interface)
- [Application programming interface](#application-programming-interface)
- [API reference coverage](#api-reference-coverage)
- [API reference rendering and navigation](#api-reference-rendering-and-navigation)
- [Miscellaneous](#miscellaneous)
- [Testing and contributing](#testing-and-contributing)
- [Installation](#installation)


# Overview
**MikeDoc** (pronounced `/ˈmaɪkdɒk/`) is a neat [docstring](https://en.wikipedia.org/wiki/Docstring) format for building API references.

Its eponymous lightweight reference [library](#installation) exposes functions and classes for parsing docstrings as well as traversing any arbitrary [Python](https://www.python.org/) codebase, iteratively yielding the fields, classes, and functions contained within each module.

The library also offers to generate API references consisting of [Markdown](https://en.wikipedia.org/wiki/Markdown) documents from the command line or programmatically. Once generated, an API reference can be browsed offline with a Markdown reader or online with [GitHub](https://en.wikipedia.org/wiki/GitHub) or another platform.


# Usage
**MikeDoc**'s [Python package](#installation) can be used both as a tool to generate API references, or as a library to traverse an arbitrary Python codebase (for example, to create a new tool to generate API references).

## Building an API reference
From the command-line:

```bash
# cd in the project root dir
$ cd /path/to/project

# create the config file
$ mikedoc init
Config file 'mikedoc.kvf' created !

# build the api reference
$ mikedoc build
API reference built in 'docs/api' !
```

Programmatically:
```python
from mikedoc import build

# config
root_dir = "/path/to/project"
project_name = "ProjectName"
project_url = "/README.md"
pkg_dir = "src/package"
api_dir = "docs/api"

# build the API reference
build(root_dir, project_name, project_url, pkg_dir, api_dir)
```
## Traversing a codebase
The following script uses three loops to access the methods of all classes in order to print their docstrings:

```python
import mikedoc

root_dir = "/path/to/project"
pkg_dir = "src/package"

# === LOOP 1 === Accessing each module
for module_info, members in mikedoc.browse(root_dir, pkg_dir):
    # 'module_info' is a namedtuple and 'members' is an iterator
    # to iterate through fields, funcs, and classes in the module
    assert isinstance(module_info, mikedoc.ModuleInfo)

    # === LOOP 2 === Accessing each member in the module
    for member_info in members:
        # 'member_info' is a namedtuple
        assert isinstance(member_info, mikedoc.MemberInfo)
        # skip if member isn't a class
        if not member_info.is_class:
            continue
        # 'class_members' is a sequence of namedtuples
        class_members = member_info.members

        # === LOOP 3 === Accessing each member in the class
        for class_member_info in class_members:
            # class_member_info is a namedtuple
            assert isinstance(class_member_info, mikedoc.ClassMemberInfo)
            # print the parsed docstring of each method in the class
            if class_member_info.is_method:
                # get the docstring
                docstring = class_member_info.doc
                # parse the docstring
                data = mikedoc.parse_docstring(docstring)
                # print the docstring
                print(docstring)
```

## Parsing a docstring
```python
from mikedoc import parse_docstring

docstring = """
A multiline description
for a *function* that adds two numbers

[params]
- a: left-hand integer operand
- b: right-hand integer operand

[returns]
Sum of `a` and `b`"""

# returns a dictionary
data = parse_docstring(docstring)

print(data)
```
The code above would output this:
```
{'': 'A multiline description\nfor a *function* that adds two numbers',
 'param': {'a': 'left-hand integer operand',
           'b': 'right-hand integer operand'}, 
 'return': 'Sum of `a` and `b`'}
```


# Demo
**MikeDoc**'s API reference itself can serve as an explorable demo as well as those from other projects such as **Braq** and **Paradict**.

| Project | API reference |
| --- | --- |
| [MikeDoc](#readme): Neat docstring format for building API references | [mikedoc/docs/api](https://github.com/pyrustic/mikedoc/blob/master/docs/api/README.md#mikedoc-api-reference) |
| [Braq](https://github.com/pyrustic/braq): Customizable data format for config files, AI prompts, and more | [braq/docs/api](https://github.com/pyrustic/braq/blob/master/docs/api/README.md#braq-api-reference) |
| [Paradict](https://github.com/pyrustic/paradict): Streamable multi-format serialization with schema | [paradict/docs/api](https://github.com/pyrustic/paradict/blob/master/docs/api/README.md#paradict-api-reference) |

# Docstring format
The format can be summarized as follows:

```python
def arbitrary_function(a, b):
    """
    A description of the **function** that
    might span multiple lines.
    
    [params]
    Optional short text to introduce parameters.
    - a: Short or long description that might
    span multiple lines.
    - b: Short or long description that might
    span multiple lines.
    
    [returns]
    This section describes the value to return.
    
    [yields]
    This section describes the value to yield.
    
    [raises]
    Optional short text to introduce
    exceptions that might be raised.
    - Exception: Short or long description that might
    span multiple lines.
    """
    ...
```

The **MikeDoc** format uses [Braq](https://github.com/pyrustic/braq) to structure the docstring into sections. The unnamed section represents the description of the function/class/method. The `param` and `except` sections are hyphenated key-value pairs to describe parameters and exceptions (which might be raised), respectively.

> The docstring format allows reasonable use of [Markdown](https://en.wikipedia.org/wiki/Markdown) like emphasis and links. It is recommended to keep it simple.

# Config file
To be able to build a reference API for an arbitrary Python project, a `mikedoc.kvf` [config file](https://github.com/pyrustic/kvf) should be placed at the root of the codebase directory. The file can be generated with the `init` command from the CLI.

Here is the `mikedoc.kvf` config file placed at the root of **MikeDoc** itself:

```
# project name
project_name = 'MikeDoc'

# project's website or README
project_url = '/README.md'

# package directory (relative path)
pkg_dir = 'mikedoc'

# API directory (relative path)
api_dir = 'docs/api'
```

For a project named **my-project**, whose package (**my_project**) isn't placed directly at the root of the project directory but inside the `src` folder, the `pkg_dir` would contain the string `'src/my_project'`.

> Only the **slash character** is allowed as path separator in the config file.
> 
> **For most cases**, the generated config file doesn't need to be edited.

# Command-line interface
The `init` and `build` commands are all you need:

```bash
# cd in the project root dir
$ cd /path/to/project/root

# create the config file
$ mikedoc init
Config file 'mikedoc.kvf' created !

# build the api reference
$ mikedoc build
API reference built in 'docs/api' !
```

> **For most cases**, the generated config file doesn't need to be edited.

# Application programming interface
> Explore the [API Reference](/docs/api) !

# API reference coverage
An API reference generated by this tool would comprehensively cover various elements of a **Python** codebase, including:
- **Modules:** A module represents the main unit of a codebase.
  - **Fields:** Variables and constants.
  - **Functions**
  - **Classes**
    - **Regular classes**
        - **Fields:** Also referred to as `class attributes`.
        - **Properties:** `Getters`, `setters`, and `deleters`.
        - **Methods**
          - **Regular methods**
          - **Static methods**
          - **Class methods**
    - **Enumerations**
      - **Fields:** Also referred to as `enum members`.
    - **Named Tuples**
      - **Fields**

# API reference rendering and navigation
**MikeDoc** generates [Markdown](https://github.github.com/gfm/) files that can be rendered and browsed online on [GitHub](https://github.com/pyrustic/mikedoc) or explored offline with a Markdown reader. Markdown files are organized in directories that mirror the organization of the codebase.

```
project
    mikedoc.kvf
    src
        package  [1]
            module1.py
            sub_package
                module2.py
    docs
        api  [2]
            README.md  [3]
            MIKEDOC
            modules
                package
                    module1
                        README.md  [4]
                        class-MyClass1.md  [5]
                        fields.md  [6]
                        funcs.md  [7]
                    sub_package
                        module2
                            README.md
                            class-MyClass2.md
                            fields.md
                            funcs.md
```

- [1] - The package directory: `pkg_dir = 'src/package'`.
- [2] - The API directory: `api_dir = 'docs/api'`.
- [3] - Home page for the API reference.
- [4] - Overview page for the `package.module1` module.
- [5] - Page for documenting `MyClass1` exposed in `package.module1`.
- [6] - Page for documenting public fields (variables and constants) exposed in `package.module1`.
- [7] - Page for documenting public functions exposed in `package.module1`.


> **Navigation between pages** relies on **links** all **relative** to the **root directory**. These relative links are prefixed with a slash `/`.

# Miscellaneous
Miscellaneous stuff...
## Underlined links on GitHub
In **Python**, underscores are very common in identifiers. When these identifiers are rendered as underlined links, it becomes hard to notice the underscores. 

> To change the visibility of underlines on links that are adjacent to text, check the GitHub [accessibility settings](https://github.com/settings/accessibility).


# Testing and contributing
Feel free to **open an issue** to report a bug, suggest some changes, show some useful code snippets, or discuss anything related to this project. You can also directly email [me](https://pyrustic.github.io/#contact).

## Setup your development environment
Following are instructions to setup your development environment

```bash
# create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# clone the project then change into its directory
git clone https://github.com/pyrustic/mikedoc.git
cd mikedoc

# install the package locally (editable mode)
pip install -e .

# run tests
python -m unittest discover -f -s tests -t .

# deactivate the virtual environment
deactivate
```

<p align="right"><a href="#readme">Back to top</a></p>

# Installation
**MikeDoc** is **cross-platform**. It is built on [Ubuntu](https://ubuntu.com/download/desktop) and should work on **Python 3.5** or **newer**.

## Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate
```

## Install for the first time

```bash
pip install mikedoc
```

## Upgrade the package
```bash
pip install mikedoc --upgrade --upgrade-strategy eager
```

## Deactivate the virtual environment
```bash
deactivate
```

<p align="right"><a href="#readme">Back to top</a></p>

# About the author
Hello world, I'm Alex, a tech enthusiast ! Feel free to get in touch with [me](https://pyrustic.github.io/#contact) !

<br>
<br>
<br>

[Back to top](#readme)

