"""Misc stuff. The `parse_docstring` function is defined in this module."""
import os
import os.path
import sys
import shutil
import pathlib
import braq
from contextlib import contextmanager
from mikedoc import errors


__all__ = ["parse_docstring"]


SRC_URL_TEMPLATE = "/{pkg_dir}/{path}"
API_URL_TEMPLATE = "/{api_dir}/{path}"


def parse_docstring(docstring):
    """
    Parse a MikeDoc docstring

    [param]
    - docstring: String to parse

    [return]
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
    """
    docstring = docstring if docstring else ""
    doc = braq.decode(docstring)
    new_doc = dict()
    for key in doc.keys():
        key = key.lower()
        if key == "":
            new_doc[""] = "\n".join(doc[key]).strip()
        elif key in ("arg", "args", "argument", "arguments", 
                     "param", "params", "parameter", "parameters"):
            new_doc["params"] = "\n".join(doc[key]).strip()
        elif key in ("ret", "return", "returns"):
            new_doc["returns"] = "\n".join(doc[key]).strip()
        elif key in ("yield", "yields"):
            new_doc["yields"] = "\n".join(doc[key]).strip()
        elif key in ("exc", "except", "exception", "exceptions", "raise", "raises"):
            new_doc["raises"] = "\n".join(doc[key]).strip()
    if "params" in new_doc:
        new_doc["params"] = parse_hyphenated_list(new_doc["params"])
    if "raises" in new_doc:
        new_doc["raises"] = parse_hyphenated_list(new_doc["raises"])
    return new_doc


@contextmanager
def mount_project(root_dir, pkg_dir):
    """Context manager to temporarily add a Python project to the sys.path
    for discoverability"""
    parts = split_relative_path(pkg_dir)
    n = len(parts)
    if n == 1:
        path = root_dir
    elif n > 1:
        path = os.path.join(root_dir, *parts[0:-1])
    else:
        raise errors.Error("pkg_dir shouldn't be empty")
    sys.path.insert(0, path)
    try:
        yield
    finally:
        try:
            sys.path.remove(path)
        except ValueError as e:
            pass


def build_module_name(root_dir, pkg_dir, py_filename):
    """
    py_filename is an absolute path to python file

    Return None or the dotted name of the module
    Could have done this too:
    x = os.path.relpath(filename, root) then
    cache = pathlib.Path(x).parts
    ".".join(cache)
    """
    directory = os.path.join(root_dir, *split_relative_path(pkg_dir))
    filename, _ = os.path.splitext(py_filename)
    p = pathlib.Path(directory).parts
    f = pathlib.Path(filename).parts
    for i, item in enumerate(p):
        if item != f[i]:
            return
    return ".".join(f[len(p)-1:])


def build_absolute_path(root_dir, relative_path):
    parts = split_relative_path(relative_path)
    return os.path.join(root_dir, *parts)


def build_api_url(api_dir, module_name=None, basename="README.md"):
    if module_name:
        module_path = module_name.replace(".", "/")
        path = "modules/{module_path}/{basename}".format(module_path=module_path,
                                                         basename=basename)
    else:
        path = basename
    return API_URL_TEMPLATE.format(api_dir=api_dir.strip("./"), path=path)


def build_src_url(pkg_dir, module_name):
    module_parts = module_name.split(".")[1:]
    module_path = "/".join(module_parts)
    path = module_path + ".py"
    return SRC_URL_TEMPLATE.format(pkg_dir=pkg_dir.strip("./"), path=path)


def delete_api_dir(root_dir, api_dir):
    path = os.path.join(root_dir, *split_relative_path(api_dir))
    if not os.path.exists(path):
        return False
    n = len(os.listdir(path))
    if n == 0:
        return False
    if n != 3:
        return False
    if not os.path.isfile(os.path.join(path, "MIKEDOC")):
        return False
    if not os.path.isfile(os.path.join(path, "README.md")):
        return False
    if not os.path.isdir(os.path.join(path, "modules")):
        return False
    shutil.rmtree(path)
    return True


def escape_emphasis(text):
    """Cancel emphasis by escaping characters such as hyphen, asterisk, and backtick."""
    # escape *
    text = text.replace("*", "\\*")
    # escape _
    text = text.replace("_", "\\_")
    # escape `
    text = text.replace("`", "\\`")
    return text


def escape_unicode_string(s):
    """BEWARE ! This function will convert a line feed into: \x0a"""
    if not s:
        return s
    cache = list()
    for char in s:
        if not is_printable(char):
            char = "\\x{:02x}".format(ord(char))
        cache.append(char)
    return "".join(cache)


def is_printable(char):
    try:
        char.encode("utf-8")
    except Exception:
        return False
    else:
        return char.isprintable()


def save_api_page(text, root_dir, api_dir, module_name=None,
                  basename="README.md"):
    if not text or text.isspace():
        return False
    api_dir_parts = split_relative_path(api_dir)
    module_name_parts = module_name.split(".") if module_name else list()
    dirname = os.path.join(root_dir, *api_dir_parts, *module_name_parts)
    ensure_dir(dirname)
    filename = os.path.join(dirname, basename)
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)
    return True


def iter_py_files(location):
    for root, dirs, filenames in os.walk(location):
        dirs.sort()
        for filename in sorted(filenames):
            if filename.endswith('.py'):
                yield os.path.join(root, filename)


def split_relative_path(path):
    path = path.strip("/")
    if path.startswith("./"):
        path = path[2:]
    return path.split("/")


def ensure_dir(path):
    try:
        os.makedirs(path)
    except FileExistsError as e:
        return False
    return True


def get_class_dotted_name(klass, escape_md=False):
    module = klass.__module__
    if module == "builtins":
        cache = klass.__qualname__
    else:
        cache = ".".join((module, klass.__qualname__))
    if escape_md:
        cache = escape_emphasis(cache)
    return cache


def urlify_section_title(s, prefix="#"):
    c = list()
    if prefix:
        c.append(prefix)
    for char in s:
        if char.isspace():
            char = "-"
        else:
            char = char.lower()
        c.append(char)
    return "".join(c)


def is_namedtuple_class(cls):
    return (issubclass(cls, tuple)
            and hasattr(cls, '_fields')
            and hasattr(cls, '_asdict'))


def get_short_description(description, length):
    if not description:
        return ""
    # flatten
    s = description.split("\n\n")[0].replace("\n", " ")
    return truncate_str(s, length=length)


def truncate_str(s, length, suspension="..."):
    val = ((s[:length] + suspension)
           if len(s) > length else s)
    return val


def parse_hyphenated_list(text):
    key = ""
    data = {key: list()}
    for line in text.splitlines():
        if line.startswith("-"):
            line = line[1:]
            cache = line.split(":", maxsplit=1)
            if len(cache) == 1:
                key, value = "", cache[0].strip()
                data[key].append(value)
            elif len(cache) == 2:
                key, value = cache[0].strip(), cache[1].strip()
                if key not in data:
                    data[key] = list()
                data[key].append(value)
        else:
            if key != "":
                line = line.strip()
            data[key].append(line.strip())
    return _merge_lines_in_hyphenated_list(data)


def _merge_lines_in_hyphenated_list(data):
    cache = list()
    for key, value in data.items():
        if key == "":
            val = "\n".join(value)
        else:
            val = " ".join(value)
        val = val.strip()
        if val:
            data[key] = val
        else:
            cache.append(key)
    for key in cache:
        del data[key]
    return data
