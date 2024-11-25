"""This module exposes function for browsing the codebase, and iterating/inspecting modules"""
import inspect
import importlib
import importlib.util
from collections import namedtuple
from mikedoc import misc


__all__ = ["browse", "iter_modules", "inspect_module", "ModuleInfo",
           "MemberInfo", "ClassMemberInfo"]

ModuleInfo = namedtuple("ModuleInfo", ["name", "obj", "doc"])
MemberInfo = namedtuple("MemberInfo", ["name", "obj",  "doc", "signature", "bases", "members",
                                       "is_field", "is_class", "is_func"])
ClassMemberInfo = namedtuple("ClassMemberInfo", ["name", "obj", "doc", "signature", "lineage",
                                                 "is_field", "is_property", "is_method"])

# === Doc for module_info
ModuleInfo.__doc__ = """Named tuple yielded by the `mikedoc.browse` generator. 
It contains info about one module"""
ModuleInfo.name.__doc__ = """String representing the dotted name of the module.
Note that for a module `package/__init__.py`, the dotted name would be `package.__init__`"""
ModuleInfo.doc.__doc__ = """The docstring of the module, parsable with
`mikedoc.parse_docstring`. The field is set to `None` in absence of docstring."""


# === Doc for member_info
MemberInfo.__doc__ = """Named tuple representing a member of a module"""
MemberInfo.name.__doc__ = """The name of the member. This isn't a dotted name."""
MemberInfo.obj.__doc__ = """The object representing the member."""
MemberInfo.doc.__doc__ = """The docstring of the member, parsable with
`mikedoc.parse_docstring`. The field is set to `None` in absence of docstring."""
MemberInfo.signature.__doc__ = """The signature string if it is available, otherwise, None."""
MemberInfo.bases.__doc__ = """List of bases class objects from which a class inherits from.
This isn't the `mro` at all. This field is set to None when the member isn't a class"""
MemberInfo.members.__doc__ = """The list of members of a class. 
This list contains `mikedoc.ClassMemberInfo` instances. If the member isn't a class, the list is set to None."""
MemberInfo.is_field.__doc__ = """Boolean telling whether the member is a field or not"""
MemberInfo.is_class.__doc__ = """Boolean telling whether the member is a class or not"""
MemberInfo.is_func.__doc__ = """Boolean telling whether the member is a func or not"""


# === Doc for class_member_info
ClassMemberInfo.__doc__ = """Named tuple representing a member of a class"""
ClassMemberInfo.name.__doc__ = """The name of the member. This isn't a dotted name."""
ClassMemberInfo.obj.__doc__ = """The object representing the member."""
ClassMemberInfo.doc.__doc__ = """The docstring of the member, parsable with
`mikedoc.parse_docstring`. The field is set to `None` in absence of docstring."""
ClassMemberInfo.signature.__doc__ = """The signature string if it is available, otherwise, None."""
ClassMemberInfo.lineage.__doc__ = """List of bases classes where the class member
 has been overridden or defined. The list goes from the most recent change to the first definition."""
ClassMemberInfo.is_field.__doc__ = """Boolean to tells whether the member is a field or not"""
ClassMemberInfo.is_property.__doc__ = """Boolean to tells whether the member is a property or not"""
ClassMemberInfo.is_method.__doc__ = """Boolean to tells whether the member is a method or not"""


def browse(root_dir, pkg_dir):
    """Generator to iterate through each module info and the associated members' info.

    [param]
    - root_dir: Project root directory path
    - pkg_dir: Relative path to the root_dir indicating the package directory.
    Slash is the only allowed separator. Example: "my_package" or "src/my_package".

    [yield]
    Yields a 2-tuple made of a `mikedoc.ModuleInfo` instance and an iterator representing
    members of the current module. The members are `mikedoc.MemberInfo` info
    """
    for module_obj, members in iter_modules(root_dir, pkg_dir):
        module_name = module_obj.__name__
        module_doc = get_printable_doc(module_obj)
        module_info = ModuleInfo(module_name, module_obj, module_doc)
        members = [create_member_info(member) for member in members]
        yield module_info, members


def iter_modules(root_dir, pkg_dir):
    """Generator for iterating over modules

    [param]
    - root_dir: The project root directory
    - pkg_dir: Relative path to the root_dir indicating the package directory.
    Slash is the only allowed separator. Example: "my_package" or "src/my_package".

    [yield]
    Yields a 2-tuple made of a module and the list of 2-tuples (name and object)
    representing its members.
    """
    with misc.mount_project(root_dir, pkg_dir):
        yield from _iter_modules(root_dir, pkg_dir)


def inspect_module(module):
    """Inspect a module object and returns a list of 2-tuples representing the module's members

    [param]
    - module: a Python module object

    [return]
    A list of 2-tuples. Each tuple is made of the name of a module member and the member itself."""
    module_name = module.__name__
    data = []
    members = inspect.getmembers(module)
    members = {name: obj for name, obj in members} if members else dict()
    if "__all__" in members:
        return restrict_members(members, members["__all__"])
    for name in sorted(members):
        if name.startswith("__"):
            continue
        obj = members[name]
        try:
            if obj.__module__ != module_name:
                continue
        except AttributeError as e:
            pass
        data.append((name, obj))
    return data


def _iter_modules(root_dir, pkg_dir):
    path = misc.build_absolute_path(root_dir, pkg_dir)
    for py_filename in misc.iter_py_files(path):
        dotted_name = misc.build_module_name(root_dir, pkg_dir, py_filename)
        module = importlib.import_module(dotted_name)
        members = inspect_module(module)
        yield module, members


def create_member_info(member):
    name, obj = member
    is_class = is_func = is_field = False
    bases = None
    if inspect.isclass(obj):
        is_class = True
        bases = obj.__bases__
    elif inspect.isfunction(obj):
        is_func = True
    else:  # is_field
        is_field = True
    doc = get_printable_doc(obj)
    signature = _get_signature(obj)
    class_members = get_class_members(obj) if is_class else None
    return MemberInfo(name, obj, doc, signature, bases, class_members,
                      is_field, is_class, is_func)


def get_class_members(obj):
    result = list()
    attrs = sort_class_attrs(get_class_attrs(obj))
    for attr, value in attrs.items():
        if attr.startswith("__") and attr != "__init__":
            continue
        obj, lineage = value
        doc = get_printable_doc(obj)
        is_field = is_property = is_method = False
        signature = None
        # PROPERTY handler
        if isinstance(obj, property):
            is_property = True
        # METHOD handler
        elif inspect.isfunction(obj) or inspect.ismethod(obj):
            is_method = True
            signature = _get_signature(obj)
        # FIELDS handler
        else:
            is_field = True
        info = ClassMemberInfo(attr, obj, doc, signature, lineage,
                               is_field, is_property, is_method)
        result.append(info)
    return sort_class_members(result)


def get_class_attrs(obj):
    attrs = {}
    reversed_mro = list(obj.__mro__)
    reversed_mro.reverse()
    for cls in reversed_mro:
        if cls is object:
            continue
        lineage = list()
        for name in cls.__dict__.keys():
            try:
                obj = getattr(cls, name)
            except AttributeError as e:
                continue
            if name.startswith("__") and name != "__init__":
                continue
            lineage.insert(0, cls)
            attrs[name] = (obj, lineage)
    return attrs


def sort_class_attrs(attrs):
    protected_attrs = list()
    result = dict()
    for attr in sorted(attrs.keys()):
        if attr.startswith("_"):
            protected_attrs.append(attr)
            continue
        result[attr] = attrs[attr]
    for attr in protected_attrs:
        result[attr] = attrs[attr]
    return result


def sort_class_members(members):
    fields = list()
    properties = list()
    methods = list()
    result = list()
    for member in members:
        if member.name == "__init__":
            result.append(member)
        elif member.is_field:
            fields.append(member)
        elif member.is_property:
            properties.append(member)
        elif member.is_method:
            methods.append(member)
    result.extend(fields)
    result.extend(properties)
    result.extend(methods)
    return result


def restrict_members(members, restrict_to):
    cache = []
    for name in sorted(members):
        obj = members[name]
        if name in restrict_to:
            cache.append((name, obj))
    return cache


def get_printable_doc(entity):
    return inspect.getdoc(entity)


def _get_signature(obj):
    try:
        return inspect.signature(obj)
    except Exception as e:
        pass
