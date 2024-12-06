"""
:copyright: 2024 Inmanta
:contact: code@inmanta.com
:license: Inmanta EULA
"""

import pathlib
import typing

import pydantic
import yaml

import inmanta_plugins.config


class ConfigABC(pydantic.BaseModel):
    """
    Base class for module-level configuration.  Each module whose behavior
    can be adapted via a configuration can extend this class to:
    1. Define where the configuration file should be located (by implementing
        the raw_config_path method)
    2. Define the values that the configuration expects, by adding class
        attributes to the defined class (in a pydantic's base model fashion).

    For example, the given class could be defined in the module example:

    .. code-block:: python

        class ExampleConfig(inmanta_plugins.config.abc.ConfigABC):
            option1: str = "default"
            option2: int = 0

            @classmethod
            def raw_config_path(cls) -> str:
                return "inmanta:///files/example-config.yml"

    And a valid configuration file for this module would be located in the files
    folder of the project where the module is imported, and named `example-config.yml`.
    The content of the configuration file might look like this:

    .. code-block:: yaml

        option1: "default"
        option2: 3

    To access the configuration in the module that defines it, the module can simply
    define a plugin that loads the config and returns it as a dict.  i.e.

    .. code-block:: python

        @plugin()
        def get_config() -> "dict":
            return ExampleConfig.load().as_dict()

    """

    @classmethod
    def raw_config_path(cls) -> str:
        """
        Get the path to the config file, as an inmanta path.  This method
        should be implemented for each project that defines a config.  The
        returned value will be processed by `inmanta_plugins.config.resolve_path`
        to resolve the full path.
        """
        raise NotImplementedError(
            f"Config defined in {cls.__module__}.{cls.__name__} should overwrite "
            "the raw_config_path classmethod to define where the configuration file should "
            "be loaded from."
        )

    @classmethod
    def path(cls) -> pathlib.Path:
        """
        Get the path, in the current project, where the configuration
        file should be stored.
        """
        return pathlib.Path(inmanta_plugins.config.resolve_path(cls.raw_config_path()))

    @classmethod
    def load(cls: type["C"]) -> "C":
        """
        Get the config from the project files, load it and validate
        it with pydantic.  Return the corresponding pydantic object.
        """
        with open(str(cls.path())) as fd:
            raw_config = yaml.safe_load(fd)
            return cls(**raw_config)

    def as_dict(self) -> dict:
        """
        Convert the current in-memory configuration into a dictionary that can
        safely be used and accessed in an inmanta model.
        """
        return self.model_dump(mode="json")

    def save(self) -> None:
        """
        Save the current in-memory configuration to file.
        """
        self.path().write_text(yaml.safe_dump(self.as_dict()))


C = typing.TypeVar("C", bound=ConfigABC)
