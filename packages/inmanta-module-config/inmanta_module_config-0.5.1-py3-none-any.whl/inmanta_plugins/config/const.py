"""
:copyright: 2022 Inmanta
:contact: code@inmanta.com
:license: Inmanta EULA
"""

import re

from inmanta_plugins.std.types import regex_string  # type: ignore

INMANTA_PATH_PATTERN = r"^inmanta:\/\/([^\/]+)?((\/files)|(\/templates))(\/[^\/]+)+$"
INMANTA_PATH_EXPRESSION = re.compile(INMANTA_PATH_PATTERN)
InmantaPath = regex_string(regex=INMANTA_PATH_PATTERN)
"""
A path, prefixed by 'inmanta://'.  The rest of the string is a path to a file in an inmanta project or module.
    If the path starts with `/`, the path is in the project's folder.  For example,
        `inmanta:///files/example/inventory.yaml` points to a file located in `files/example/inventory.yaml`
        at the root of the project using this module.
    If the path doesn't start with `/`, the part of the string before the first `/` is
        the name of the module in the files of which the inventory is located. For example,
        `inmanta://example/files/inventory.yaml` points to a file located in `files/inventory.yaml` at the
        root of the module named example.
"""


INMANTA_TEMPLATE_PATH_PATTERN = r"^template:\/\/([^\/]+)?(\/[^\/]+)+$"
INMANTA_TEMPLATE_PATH_EXPRESSION = re.compile(INMANTA_TEMPLATE_PATH_PATTERN)
InmantaTemplatePath = regex_string(regex=INMANTA_TEMPLATE_PATH_PATTERN)
"""
A path, prefixed by 'template://'.  The rest of the string is a path to a file in the templates folder of
    an inmanta project or module.  To determine whether the path refers to a project or a module, the same
    logic as for the InmantaPath applies.
This path can also be used with the std::template plugin.
"""


INMANTA_SOURCE_PATH_PATTERN = r"^source:\/\/([^\/]+)?(\/[^\/]+)+$"
INMANTA_SOURCE_PATH_EXPRESSION = re.compile(INMANTA_SOURCE_PATH_PATTERN)
InmantaSourcePath = regex_string(regex=INMANTA_SOURCE_PATH_PATTERN)
"""
A path, prefixed by 'source://'.  The rest of the string is a path to a file in the files folder of
    an inmanta project or module.  To determine whether the path refers to a project or a module, the same
    logic as for the InmantaPath applies.
This path can also be used with the std::source plugin.
"""


SYSTEM_PATH_PATTERN = r"^file:\/\/(\/[^\/]+)+?$"
SYSTEM_PATH_EXPRESSION = re.compile(SYSTEM_PATH_PATTERN)
SystemPath = regex_string(regex=SYSTEM_PATH_PATTERN)
"""
A path, prefixed by 'file://'.  The rest of the string is the absolute path to the file.
"""
