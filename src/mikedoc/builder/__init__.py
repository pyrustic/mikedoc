"""The `Builder` class and the `build` function are defined in this module."""
import os
import os.path
from enum import Enum
from mikedoc.browser import browse
from mikedoc import templates, misc


__all__ = ["build", "Builder"]


MODULE_DESC_LEN_ON_HOME_PAGE = 256
MEMBER_DESC_LEN_ON_MODULE_PAGE = 128
DEFAULT_INTRO_FOR_EXCEPTIONS_SECTION = "The table below outlines exceptions that may occur."


def build(root_dir, project_name, project_url, pkg_dir, api_dir):
    """Build the API reference (Markdown files) in the api directory

    [param]
    - root_dir: The project root directory
    - project_name: The public (stylized or not) name of the project.
        Example, a project named `MyProject` might have `my_project` as package name and
        `my-project` as project directory name.
    - project_url: The url to the project, it might be the relative url to the README.md file
    - pkg_dir: Relative path to the root_dir indicating the package directory.
    Slash is the only allowed separator. Example: "my_package" or "src/my_package
    - api_dir: Relative path to the root_dir indicating the api reference directory.
    Slash is the only allowed separator. Example: "docs/api".
    """
    builder = Builder(root_dir, project_name, project_url, pkg_dir, api_dir)
    return builder.build()


class Builder:
    """Class to build the API reference"""
    def __init__(self, root_dir, project_name,
                 project_url, pkg_dir, api_dir):
        """Init

        [param]
        - root_dir: The project root directory
        - project_name: The public (stylized or not) name of the project.
            Example, a project named `MyProject` might have `my_project` as package name and
            `my-project` as project directory name.
        - project_url: The url to the project, it might be the relative url to the README.md file
        - pkg_dir: Relative path to the root_dir indicating the package directory.
        Slash is the only allowed separator. Example: "my_package" or "src/my_package
        - api_dir: Relative path to the root_dir indicating the api reference directory.
        Slash is the only allowed separator. Example: "docs/api".
        """
        self._root_dir = root_dir
        self._project_name = project_name
        self._project_url = project_url
        self._pkg_dir = pkg_dir
        self._api_dir = api_dir

    @property
    def root_dir(self):
        return self._root_dir

    @property
    def project_name(self):
        return self._project_name

    @property
    def project_url(self):
        return self._project_url

    @property
    def pkg_dir(self):
        return self._pkg_dir

    @property
    def api_dir(self):
        return self._api_dir

    def build(self):
        """Build the API reference"""
        cached_modules = list()
        _ensure_api_dir(self._root_dir, self._api_dir)
        for module_info, members in browse(self._root_dir, self._pkg_dir):
            if not members:
                continue
            cached_modules.append(module_info)
            fields, funcs, classes = _categorize_module_members(members)
            # create overview page
            self._create_overview_page(module_info, fields, funcs, classes)
            # create fields page
            self._create_fields_page(module_info, fields)
            # create functions page
            self._create_funcs_page(module_info, funcs)
            # create class pages
            for class_info in classes:
                self._create_class_page(module_info, class_info)
        # create home page
        self._create_home_page(cached_modules)

    def _create_home_page(self, modules):
        if not modules:
            return
        home_page = HomePage(self, modules)
        text = home_page.build()
        misc.save_api_page(text, self._root_dir, self._api_dir)

    def _create_overview_page(self, module_info, fields, funcs, classes):
        overview_page = ModuleOverviewPage(self, module_info, fields, funcs, classes)
        text = overview_page.build()
        basename = "README.md"
        modules_api_dir = self._api_dir + "/modules"
        misc.save_api_page(text, self._root_dir, modules_api_dir,
                           module_info.name, basename)

    def _create_fields_page(self, module_info, fields):
        if not fields:
            return
        fields_doc_page = FieldsDocPage(self, module_info, fields)
        text = fields_doc_page.build()
        basename = "fields.md"
        modules_api_dir = self._api_dir + "/modules"
        misc.save_api_page(text, self._root_dir, modules_api_dir,
                           module_info.name, basename)

    def _create_funcs_page(self, module_info, funcs):
        if not funcs:
            return
        funcs_doc_page = FuncsDocPage(self, module_info, funcs)
        text = funcs_doc_page.build()
        basename = "funcs.md"
        modules_api_dir = self._api_dir + "/modules"
        misc.save_api_page(text, self._root_dir, modules_api_dir,
                           module_info.name, basename)

    def _create_class_page(self, module_info, class_info):
        class_doc_page = ClassDocPage(self, module_info, class_info)
        text = class_doc_page.build()
        basename = "class-{}.md".format(class_info.name)
        modules_api_dir = self._api_dir + "/modules"
        misc.save_api_page(text, self._root_dir, modules_api_dir,
                           module_info.name, basename)


class HomePage:
    def __init__(self, builder, modules):
        self._builder = builder
        self._modules = modules
        self._project_name = builder.project_name
        self._project_url = builder.project_url
        self._api_dir = builder.api_dir

    @property
    def builder(self):
        return self._builder

    @property
    def modules(self):
        return self._modules

    def build(self):
        contents = list()
        for module_info in self._modules:
            name = module_info.name
            docstring_dict = misc.parse_docstring(module_info.doc)
            description = docstring_dict.get("", "No docstring.")
            short_description = misc.get_short_description(description,
                                                           length=MODULE_DESC_LEN_ON_HOME_PAGE)
            api_url = misc.build_api_url(self._api_dir, name, "README.md")
            escaped_module_name = misc.escape_emphasis(name)
            module_entry = templates.MODULE_LINE.format(module_name=escaped_module_name,
                                                        api_url=api_url,
                                                        short_description=short_description)
            contents.append(module_entry)
        escaped_project_name = misc.escape_emphasis(self._project_name)
        back_to_top = _create_back_to_top(self._project_name)
        text = templates.HOME_PAGE.format(project_name=escaped_project_name,
                                          project_url=self._project_url,
                                          contents="\n\n".join(contents),
                                          back_to_top=back_to_top)
        return text


class ModuleOverviewPage:
    def __init__(self, builder, module_info, fields, funcs, classes):
        self._builder = builder
        self._module_info = module_info
        self._fields = fields
        self._funcs = funcs
        self._classes = classes
        self._module_name = module_info.name
        self._project_name = builder.project_name
        self._project_url = builder.project_url
        self._pkg_dir = builder.pkg_dir
        self._api_dir = builder.api_dir

    @property
    def builder(self):
        return self._builder

    @property
    def module_info(self):
        return self._module_info

    @property
    def fields(self):
        return self._fields

    @property
    def funcs(self):
        return self._funcs

    @property
    def classes(self):
        return self._classes

    def build(self):
        text = templates.OVERVIEW_PAGE
        members_section = self._create_members_section()
        # source url
        header_div = _create_header_div_1(self._project_name, self._project_url,
                                          self._pkg_dir, self._api_dir, self._module_name)
        back_to_top = _create_back_to_top(self._project_name)
        docstring_dict = misc.parse_docstring(self._module_info.doc)
        text = text.format(header_div=header_div,
                           module_name=misc.escape_emphasis(self._module_name),
                           description=docstring_dict.get("", "No docstring."),
                           members=members_section,
                           back_to_top=back_to_top)
        return text

    def _create_members_section(self):
        sections = list()
        for text in (self._create_fields_section(),
                     self._create_funcs_section(),
                     self._create_classes_section()):
            if not text:
                continue
            sections.append(text)
        return "\n\n".join(sections)

    def _create_fields_section(self):
        if not self._fields:
            return
        fields_page_url = misc.build_api_url(self._api_dir, self._module_name, "fields.md")
        contents = list()
        for field_info in self._fields:
            value = "`{}`".format(repr(field_info.obj))
            line = templates.FIELD_LINE.format(name=misc.escape_emphasis(field_info.name),
                                               value=value)
            contents.append(line)
        back_to_top = _create_back_to_top(self._project_name)
        text = templates.ALL_FIELDS_SECTION.format(fields_page_url=fields_page_url,
                                                   contents="\n".join(contents),
                                                   back_to_top=back_to_top)
        return text

    def _create_funcs_section(self):
        if not self._funcs:
            return
        funcs_page_url = misc.build_api_url(self._api_dir, self._module_name, "funcs.md")
        contents = list()
        for func_info in self._funcs:
            docstring_dict = misc.parse_docstring(func_info.doc)
            func_description = docstring_dict.get("", "No docstring.")
            length = MEMBER_DESC_LEN_ON_MODULE_PAGE
            func_short_description = misc.get_short_description(func_description,
                                                                length=length)
            urlified_func_name = misc.urlify_section_title(func_info.name)
            func_doc_url = funcs_page_url + urlified_func_name
            line = templates.FUNC_LINE.format(name=misc.escape_emphasis(func_info.name),
                                              doc_url=func_doc_url,
                                              short_description=func_short_description)
            contents.append(line)
        back_to_top = _create_back_to_top(self._project_name)
        text = templates.ALL_FUNCTIONS_SECTION.format(funcs_page_url=funcs_page_url,
                                                      contents="\n".join(contents),
                                                      back_to_top=back_to_top)
        return text

    def _create_classes_section(self):
        if not self._classes:
            return
        contents = list()
        for class_info in self._classes:
            docstring_dict = misc.parse_docstring(class_info.doc)
            class_description = docstring_dict.get("", "No docstring.")
            length = MEMBER_DESC_LEN_ON_MODULE_PAGE
            class_short_description = misc.get_short_description(class_description,
                                                                 length=length)
            basename = "class-{}.md".format(class_info.name)
            class_page_url = misc.build_api_url(self._api_dir, self._module_name, basename)
            if issubclass(class_info.obj, Enum):
                sub_contents = self._create_enum_members_section(class_info.obj)
            elif misc.is_namedtuple_class(class_info.obj):
                sub_contents = self._create_namedtuple_members_section(class_info.obj)
            else:
                sub_contents = self._create_class_members_section(class_info.members, 
                                                                  class_page_url)
            sub_text = templates.CLASS_SECTION.format(name=misc.escape_emphasis(class_info.name),
                                                      doc_url=class_page_url,
                                                      short_description=class_short_description,
                                                      contents=sub_contents)
            contents.append(sub_text)
        back_to_top = _create_back_to_top(self._project_name)
        text = templates.ALL_CLASSES_SECTION.format(contents="\n".join(contents),
                                                    back_to_top=back_to_top)
        return text

    def _create_class_members_section(self, members, class_page_link):
        contents = list()
        for member in members:
            if member.name == "__init__":
                continue
            kv_sign = ":"
            if member.is_property:
                urlified_member_name = misc.urlify_section_title("Properties table")
                kv_sign = ";"
                property_methods = _name_property_methods(member)
                description = "_{}_".format(", ".join(property_methods))
            elif member.is_field:
                urlified_member_name = misc.urlify_section_title("Fields table")
                kv_sign = " ="
                description = "`{}`".format(repr(member.obj))
            else:
                urlified_member_name = misc.urlify_section_title(member.name)
                docstring_dict = misc.parse_docstring(member.doc)
                description = docstring_dict.get("", "No docstring.")
            length = MEMBER_DESC_LEN_ON_MODULE_PAGE
            short_description = misc.get_short_description(description, length=length)

            member_doc_url = class_page_link + urlified_member_name
            line = templates.CLASS_MEMBER_LINE.format(name=misc.escape_emphasis(member.name),
                                                      doc_url=member_doc_url, kv_sign=kv_sign,
                                                      short_description=short_description)
            contents.append(line)
        return "\n".join(contents)

    def _create_enum_members_section(self, obj):
        contents = list()
        for item in obj:
            name, value = item.name, item.value
            value = "`{}`".format(repr(value))
            line = templates.FIELD_LINE.format(name=misc.escape_emphasis(name),
                                               value=value)
            contents.append(line)
        return "\n".join(contents)

    def _create_namedtuple_members_section(self, obj):
        contents = list()
        for name in obj._fields:
            description = getattr(obj, name).__doc__
            line = "    - {name}: {description}".format(name=misc.escape_emphasis(name),
                                                        description=description)
            contents.append(line)
        return "\n".join(contents)


class FieldsDocPage:
    def __init__(self, builder, module_info, fields):
        self._builder = builder
        self._module_info = module_info
        self._fields = fields
        self._module_name = module_info.name
        self._project_name = builder.project_name
        self._project_url = builder.project_url
        self._pkg_dir = builder.pkg_dir
        self._api_dir = builder.api_dir

    @property
    def builder(self):
        return self._builder

    @property
    def module_info(self):
        return self._module_info

    @property
    def fields(self):
        return self._fields

    def build(self):
        if not self._fields:
            return
        entries = list()
        for field_info in self._fields:
            col1, col2 = misc.escape_emphasis(field_info.name), "`{}`".format(repr(field_info.obj))
            line = templates.TWO_COLUMNS_TABLE_ENTRY.format(col1=col1, col2=col2)
            entries.append(line)
        module_api_url = misc.build_api_url(self._api_dir, self._module_name, "README.md")
        header_div = _create_header_div_2(self._project_name, self._project_url,
                                          self._pkg_dir, self._api_dir, self._module_name)
        escaped_module_name = misc.escape_emphasis(self._module_name)
        back_to_top = _create_back_to_top(self._project_name)
        text = templates.FIELDS_PAGE.format(header_div=header_div,
                                            module_name=escaped_module_name,
                                            module_api_url=module_api_url,
                                            entries="\n".join(entries),
                                            back_to_top=back_to_top)
        return text


class FuncsDocPage:
    def __init__(self, builder, module_info, funcs):
        self._builder = builder
        self._module_info = module_info
        self._funcs = funcs
        self._module_name = module_info.name
        self._project_name = builder.project_name
        self._project_url = builder.project_url
        self._pkg_dir = builder.pkg_dir
        self._api_dir = builder.api_dir

    @property
    def builder(self):
        return self._builder

    @property
    def module_info(self):
        return self._module_info

    @property
    def funcs(self):
        return self._funcs

    def build(self):
        contents = list()
        index_of_funcs = list()
        for func_info in self._funcs:
            func_section = _create_func_doc(self._project_name, func_info)
            contents.append(func_section)
            # update index of funcs
            line = "- [{func_name}]({url})"
            line = line.format(func_name=misc.escape_emphasis(func_info.name),
                               url=misc.urlify_section_title(func_info.name))
            index_of_funcs.append(line)
        contents = "\n\n".join(contents)
        module_api_url = misc.build_api_url(self._api_dir, self._module_name, "README.md")
        header_div = _create_header_div_2(self._project_name, self._project_url,
                                          self._pkg_dir, self._api_dir, self._module_name)
        # text of funcs_doc_page
        escaped_module_name = misc.escape_emphasis(self._module_name)
        text = templates.FUNCS_DOC_PAGE.format(header_div=header_div,
                                               index_of_funcs="\n".join(index_of_funcs),
                                               module_name=escaped_module_name,
                                               module_api_url=module_api_url, contents=contents)
        return text


class ClassDocPage:
    def __init__(self, builder, module_info, class_info):
        self._builder = builder
        self._module_info = module_info
        self._class_info = class_info
        self._module_name = module_info.name
        self._project_name = builder.project_name
        self._project_url = builder.project_url
        self._pkg_dir = builder.pkg_dir
        self._api_dir = builder.api_dir

    @property
    def builder(self):
        return self._builder

    @property
    def module_info(self):
        return self._module_info

    @property
    def class_info(self):
        return self._class_info

    def build(self):
        contents = list()
        fields, properties, methods = _categorize_class_members(self._class_info.members)
        if misc.is_namedtuple_class(self._class_info.obj):
            fields_section = self._create_namedtuple_fields_doc(self._class_info.obj)
        elif issubclass(self._class_info.obj, Enum):
            fields_section = self._create_enum_fields_doc(self._class_info.obj)
        else:
            fields_section = self._create_fields_doc(fields)
        properties_section = self._create_properties_doc(properties)
        methods_section = self._create_methods_doc(methods)
        # update contents
        for section in (fields_section, properties_section, methods_section):
            if section:
                contents.append(section)
        #
        module_api_url = misc.build_api_url(self._api_dir, self._module_name, "README.md")
        header_div = _create_header_div_2(self._project_name, self._project_url,
                                          self._pkg_dir, self._api_dir, self._module_name)
        inheritance = _create_inheritance_segment(self._class_info.bases,
                                                  self._pkg_dir, self._api_dir)
        escaped_module_name = misc.escape_emphasis(self._module_name)
        docstring_dict = misc.parse_docstring(self._class_info.doc)
        description = docstring_dict.get("", "No class docstring.")
        escaped_class_name = misc.escape_emphasis(self._class_info.name)
        text = templates.CLASS_DOC_PAGE.format(header_div=header_div,
                                               class_name=escaped_class_name,
                                               module_name=escaped_module_name,
                                               module_api_url=module_api_url,
                                               inheritance=inheritance,
                                               description=description,
                                               contents="\n\n".join(contents))
        return text

    def _create_fields_doc(self, fields):
        if not fields:
            return
        entries = list()
        for field in fields:
            key = misc.escape_emphasis(field.name)
            val = "`{}`".format(repr(field.obj))
            entry = templates.TWO_COLUMNS_TABLE_ENTRY.format(col1=key, col2=val)
            entries.append(entry)
        back_to_top = _create_back_to_top(self._project_name)
        text = templates.FIELDS_EXPOSED_IN_CLASS.format(contents="\n".join(entries),
                                                        back_to_top=back_to_top)
        return text

    def _create_namedtuple_fields_doc(self, obj):
        if not obj._fields:
            return
        contents = list()
        for name in obj._fields:
            description = getattr(obj, name).__doc__
            description = description if description else "No description."
            description = description.replace("\n", " ")
            line = templates.TWO_COLUMNS_TABLE_ENTRY.format(col1=misc.escape_emphasis(name),
                                                            col2=description)
            contents.append(line)
        back_to_top = _create_back_to_top(self._project_name)
        text = templates.FIELDS_EXPOSED_IN_NAMEDTUPLE.format(contents="\n".join(contents),
                                                             back_to_top=back_to_top)
        return text

    def _create_enum_fields_doc(self, obj):
        if not obj.__members__:
            return
        contents = list()
        for item in obj:
            name, value = item.name, item.value
            value = "`{}`".format(repr(value))
            line = templates.TWO_COLUMNS_TABLE_ENTRY.format(col1=misc.escape_emphasis(name),
                                                            col2=value)
            contents.append(line)
        back_to_top = _create_back_to_top(self._project_name)
        text = templates.FIELDS_EXPOSED_IN_ENUM.format(contents="\n".join(contents),
                                                       back_to_top=back_to_top)
        return text

    def _create_properties_doc(self, properties):
        if not properties:
            return
        entries = list()
        for prop in properties:
            property_methods = _name_property_methods(prop)
            methods_as_str = "_{}_".format(", ".join(property_methods))
            docstring_dict = misc.parse_docstring(prop.doc)
            doc = docstring_dict.get("", "No docstring.")
            escaped_property_name = misc.escape_emphasis(prop.name)
            entry = templates.THREE_COLUMNS_TABLE_ENTRY.format(col1=escaped_property_name,
                                                               col2=methods_as_str,
                                                               col3=doc)
            entries.append(entry)
        back_to_top = _create_back_to_top(self._project_name)
        text = templates.PROPERTIES_EXPOSED_IN_CLASS.format(contents="\n".join(entries),
                                                            back_to_top=back_to_top)
        return text

    def _create_methods_doc(self, methods):
        if not methods:
            return
        contents = list()
        index_of_methods = list()
        for method_info in methods:
            decorator = _get_decorator(self._class_info, method_info)
            func_section = _create_func_doc(self._project_name, method_info,
                                            decorator=decorator)
            contents.append(func_section)
            # update index of funcs
            line = "- [{func_name}]({url})"
            line = line.format(func_name=misc.escape_emphasis(method_info.name),
                               url=misc.urlify_section_title(method_info.name))
            index_of_methods.append(line)
        index_of_methods = "\n".join(index_of_methods)
        methods_section = templates.METHODS_SECTION.format(index_of_methods=index_of_methods,
                                                           contents="\n\n".join(contents))
        return methods_section


def _get_decorator(class_info, method_info):
    decorator = ""
    obj = None
    for cls in class_info.obj.__mro__:
        try:
            obj = cls.__dict__[method_info.name]
        except KeyError as e:
            continue
    if obj:
        if isinstance(obj, staticmethod):
            decorator = "@staticmethod"
        if isinstance(obj, classmethod):
            decorator = "@classmethod"
    return decorator


def _ensure_api_dir(root_dir, api_dir):
    misc.delete_api_dir(root_dir, api_dir)
    api_dir_parts = misc.split_relative_path(api_dir)
    content_path = os.path.join(root_dir, *api_dir_parts, "modules")
    misc.ensure_dir(content_path)
    mikedoc_filename = os.path.join(root_dir, *api_dir_parts, "MIKEDOC")
    with open(mikedoc_filename, "w", encoding="utf-8") as file:
        text = ("API Reference generated with "
                "[MikeDoc](https://github.com/pyrustic/mikedoc).\n")
        file.write(text)
    readme_filename = os.path.join(root_dir, *api_dir_parts, "README.md")
    with open(readme_filename, "w") as file:
        pass


def _categorize_module_members(members):
    all_fields = list()
    all_functions = list()
    all_classes = list()
    for member in members:
        if member.is_func:
            all_functions.append(member)
        elif member.is_class:
            all_classes.append(member)
        elif member.is_field:
            all_fields.append(member)
    return all_fields, all_functions, all_classes


def _categorize_class_members(members):
    all_fields = list()
    all_properties = list()
    all_methods = list()
    for member in members:
        if member.is_field:
            all_fields.append(member)
        elif member.is_property:
            all_properties.append(member)
        elif member.is_method:
            all_methods.append(member)
    return all_fields, all_properties, all_methods


def _create_header_div_1(project_name, project_url, pkg_dir, api_dir, module_name):
    src_url = misc.build_src_url(pkg_dir, module_name)
    escaped_project_name = misc.escape_emphasis(project_name)
    home_url = misc.build_api_url(api_dir)
    header_div = templates.HEADER_DIV_1.format(project_name=escaped_project_name,
                                               project_url=project_url,
                                               home_url=home_url, src_url=src_url)
    return header_div


def _create_header_div_2(project_name, project_url, pkg_dir, api_dir, module_name):
    src_url = misc.build_src_url(pkg_dir, module_name)
    api_url = misc.build_api_url(api_dir, module_name, "README.md")
    escaped_project_name = misc.escape_emphasis(project_name)
    home_url = misc.build_api_url(api_dir)
    header_div = templates.HEADER_DIV_2.format(project_name=escaped_project_name,
                                               project_url=project_url,
                                               home_url=home_url,
                                               api_url=api_url, src_url=src_url)
    return header_div


def _create_back_to_top(project_name):
    href = misc.urlify_section_title("{} API Reference".format(project_name))
    return templates.BACK_TO_TOP.format(href=href)


def _name_property_methods(prop):
    property_methods = list()
    x = [(prop.obj.fget, "getter"), (prop.obj.fset, "setter"),
         (prop.obj.fdel, "deleter")]
    for a, b in x:
        if a:
            property_methods.append(b)
    return property_methods


def _create_func_doc(project_name, func_info, decorator=None):
    decorator = decorator + "\n" if decorator else ""
    func_name = func_info.name
    docstring_dict = misc.parse_docstring(func_info.doc)
    description = docstring_dict.get("", "No docstring")
    contents = list()
    # params
    params = docstring_dict.get("params")
    if params:
        table = _create_func_params_table(params)
        contents.append(table)
    # returns
    returns_note = docstring_dict.get("returns", "")
    returns_note = returns_note.strip()
    if returns_note:
        section = _create_func_returns_section(returns_note)
        contents.append(section)
    # yields
    yields_note = docstring_dict.get("yields", "")
    yields_note = yields_note.strip()
    if yields_note:
        section = _create_func_yields_section(yields_note)
        contents.append(section)
    # exceptions
    exceptions = docstring_dict.get("raises")
    if exceptions:
        table = _create_func_exceptions_section(exceptions)
        contents.append(table)
    # append 'back to top' link
    back_to_top = _create_back_to_top(project_name)
    contents.append(back_to_top)
    escaped_func_name = misc.escape_emphasis(func_name)
    text = templates.FUNC_DOC_SECTION.format(func_name_1=escaped_func_name,
                                             func_name_2=func_name,
                                             description=description,
                                             decorator=decorator,
                                             signature=func_info.signature,
                                             contents="\n\n".join(contents))
    return text


def _create_func_params_table(data):
    if not data:
        return
    contents = list()
    intro = data.get("")
    if intro is not None:
        contents.append(intro)
        del data[""]
    entries = list()
    for key, value in data.items():
        x = templates.TWO_COLUMNS_TABLE_ENTRY.format(col1=misc.escape_emphasis(key),
                                                     col2=value)
        entries.append(x)
    text = templates.FUNC_PARAMS_TABLE.format(contents="\n".join(entries))
    contents.append(text)
    return "\n\n".join(contents)


def _create_func_exceptions_section(data):
    if not data:
        return
    contents = list()
    intro = data.get("")
    intro = intro if intro else DEFAULT_INTRO_FOR_EXCEPTIONS_SECTION
    contents.append(intro)
    try:
        del data[""]
    except KeyError as e:
        pass
    entries = list()
    for key, value in data.items():
        x = templates.TWO_COLUMNS_TABLE_ENTRY.format(col1=key, col2=value)
        entries.append(x)
    text = templates.FUNC_EXCEPTIONS_TABLE.format(contents="\n".join(entries))
    contents.append(text)
    text = templates.FUNC_EXCEPTIONS_SECTION.format(contents="\n\n".join(contents))
    return text


def _create_func_returns_section(text):
    return templates.FUNC_RETURNS_LINE.format(text=text.strip())


def _create_func_yields_section(text):
    return templates.FUNC_YIELDS_LINE.format(text=text.strip())


def _create_inheritance_segment(bases, pkg_dir, api_dir):
    cache = list()
    for base in bases:
        class_dotted_name = misc.get_class_dotted_name(base, escape_md=False)
        parts = class_dotted_name.split(".")
        module_name = ".".join(parts[0:-1])
        pkg_name = parts[0]
        class_name = parts[-1]
        edited_class_name = class_dotted_name.replace(".__init__.", ".")
        escaped_class_name = misc.escape_emphasis(edited_class_name)
        # if the base class is part of the project, we will turn it into a link
        if pkg_name == misc.split_relative_path(pkg_dir)[-1]:
            basename = "class-{}.md".format(class_name)
            api_url = misc.build_api_url(api_dir, module_name, basename)
            s = "[{class_dotted_name}]({api_url})".format(class_dotted_name=escaped_class_name,
                                                          api_url=api_url)
        else:
            s = "`{}`".format(escaped_class_name)
        cache.append(s)
    return ", ".join(cache) if cache else "No inheritance."
