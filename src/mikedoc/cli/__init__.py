"""The command-line interface class is defined here"""
import os
import os.path
import kvf
import paradict
import mikedoc


__all__ = ["Cli"]


HELP_TEXT = """\
MikeDoc - Neat docstring format for generating API references
https://github.com/pyrustic/mikedoc

COMMANDS:
    init        Create the config file
    build       Build the API reference"""


CONFIG_TEXT = """\
# project name
project_name = '{project_name}'

# project's website or README
project_url = '/README.md'

# package directory (relative path)
pkg_dir = '{pkg_dir}'

# API directory (relative path)
api_dir = 'docs/api'
"""


CONFIG_SCHEMA = {"project_name": "str",
                 "project_url": "str",
                 "pkg_dir": "str",
                 "api_dir": "str"}


class Cli:
    """Command-line interface class"""
    def __init__(self, root_dir, silent_mode=False):
        """Init

        [param]
        - root_dir: Path the project root directory
        - silent_mode: Boolean to tell whether output should be printed or not"""
        self._root_dir = root_dir
        self._silent_mode = silent_mode

    @property
    def root_dir(self):
        return self._root_dir

    @property
    def silent_mode(self):
        return self._silent_mode

    @silent_mode.setter
    def silent_mode(self, val):
        self._silent_mode = val

    def run(self, *args):
        """Run a command. Valid commands are `init`, `build` and `help`."""
        if not args or len(args) > 1:
            self.echo(HELP_TEXT)
            return False
        command = args[0].lower()
        if command == "init":
            return self._create_config_file()
        elif command == "build":
            return self._build_api_reference()
        else:
            self.echo(HELP_TEXT)
            return False

    def echo(self, text):
        """Print text if `silent_mode` is False"""
        if self._silent_mode:
            return False
        print(text)
        return True

    def _create_config_file(self):
        filename = os.path.join(self._root_dir, "mikedoc.kvf")
        if os.path.exists(filename):
            self.echo("Config file 'mikedoc.kvf' already exists.")
            return False
        text = create_config_text(self._root_dir)
        with open(filename, "w", encoding="utf-8") as file:
            file.write(text)
        self.echo("Config file 'mikedoc.kvf' created !")
        return True

    def _build_api_reference(self):
        config = self._load_config()
        if not config:
            return False
        build_api_reference(self._root_dir, config)
        self.echo("API reference built in '{}' !".format(config.get("api_dir")))
        return True

    def _load_config(self):
        filename = os.path.join(self._root_dir, "mikedoc.kvf")
        if not os.path.exists(filename):
            self.echo("Missing config file 'mikedoc.kvf'. Run the 'init' command in the root dir.")
            return
        config = load_config(filename)
        if not config:
            self.echo("Invalid config file. Delete it then run the 'init' command.")
            return
        return config


def create_config_text(root_dir):
    basename = os.path.basename(root_dir)
    project_name = basename.capitalize()
    pkg_name = basename.replace("-", "_")
    if os.path.isdir(os.path.join(root_dir, pkg_name)):
        pkg_dir = pkg_name
    else:
        pkg_dir = "src/" + pkg_name
    return CONFIG_TEXT.format(project_name=project_name,
                              pkg_dir=pkg_dir)


def load_config(filename):
    config = kvf.get_config(filename).get("")
    if not paradict.is_valid(config, CONFIG_SCHEMA):
        return
    return config


def build_api_reference(root_dir, config):
    mikedoc.build(root_dir, **config)
