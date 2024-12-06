"""
:copyright: 2022 Inmanta
:contact: code@inmanta.com
:license: Inmanta EULA
"""

import os
import pathlib
import typing
import urllib.parse

import inmanta_plugins.std  # type: ignore
import jinja2
import pkg_resources

import inmanta
import inmanta.ast
import inmanta.execute.proxy
import inmanta.module
import inmanta.plugins
import inmanta.util
import inmanta.util.dict_path

CONFIG_CACHE: dict[int, tuple[object, dict]] = {}
jinja2_env: typing.Optional[jinja2.Environment] = None


def inmanta_reset_state() -> None:
    # Reset the cache of configs
    global CONFIG_CACHE
    CONFIG_CACHE = {}

    # Resetting jinja2_env
    global jinja2_env
    jinja2_env = None


@inmanta.plugins.plugin
def get_const(name: "string") -> "any":  # type: ignore
    """
    Get a value defined in the const python module (inmanta_plugins/config/const.py)
    """
    import inmanta_plugins.config.const

    return getattr(inmanta_plugins.config.const, name)


@inmanta.plugins.plugin
def absolute_path(path: "string") -> "string":  # type: ignore
    """
    Transform the input path into its absolute counterpart.

    :param path: The path, relative or not, for which we wish to resolve
        the absolute path.
    """
    return os.path.abspath(path)


@inmanta.plugins.plugin
def resolve_path(raw_path: "config::path") -> "string":  # type: ignore
    """
    Takes a string representation of a path, prefixed with one of the following: file://, inmanta://
    and convert it to a valid path on the host.  The different inmanta types are never guaranteed to
    return an absolute path.  If you wish to resolve the absolute path, transform the returned value with
    `config::absolute_path` plugin.

    The path should start with a prefix, specifying how to resolve it.  The supported prefixes are:
        - `file://`: The rest of the string is the absolute path to the file.
        - `inmanta://`: The rest of the string is a path to a file in an inmanta files folder.
            If the path starts with `/`, the path is in the project's folder.  For example,
                `inmanta:///files/example/inventory.yaml` points to a file located in `files/example/inventory.yaml`
                at the root of the project using this module.
            If the path doesn't start with `/`, the part of the string before the first `/` is
                the name of the module in the files of which the inventory is located. For example,
                `inmanta://example/files/inventory.yaml` points to a file located in `files/inventory.yaml` at the
                root of the module named example.
        - `template://`: Similar to std::template plugin
        - `source://`: Similar to std::source plugin

    If the provided path doesn't match any of the previous format, an ValueError is raised.
    """
    parsed_uri = urllib.parse.urlparse(raw_path)
    if parsed_uri.scheme == "file":
        return (
            parsed_uri.path
            if not parsed_uri.netloc
            else f"{parsed_uri.netloc}{parsed_uri.path}"
        )

    path_parts: list[str]
    if parsed_uri.scheme == "template":
        # Split the path into parts
        # 0: "template:", 1: <empty>, 2: <module-name-or-empty>, 3-...: <rest-of-the-path>
        path_parts = raw_path.split("/")

        # Replace the scheme with the inmanta generic one
        path_parts[0] = "inmanta:"

        # Insert the templates folder in the path
        path_parts.insert(3, "templates")

        # Delegate to the generic inmanta path the resolution of the real path
        return resolve_path("/".join(path_parts))

    if parsed_uri.scheme == "source":
        # Split the path into parts
        # 0: "source:", 1: <empty>, 2: <module-name-or-empty>, 3-...: <rest-of-the-path>
        path_parts = raw_path.split("/")

        # Replace the scheme with the inmanta generic one
        path_parts[0] = "inmanta:"

        # Insert the templates folder in the path
        path_parts.insert(3, "files")

        # Delegate to the generic inmanta path the resolution of the real path
        return resolve_path("/".join(path_parts))

    if parsed_uri.scheme == "inmanta":
        if not parsed_uri.netloc:
            # Path starts with a /, looking for project files
            module_path = inmanta.module.Project.get().project_path
        else:
            modules = inmanta.module.Project.get().modules
            if parsed_uri.netloc not in modules:
                raise Exception(f"Can not find a module with name: {parsed_uri.netloc}")
            module_path = modules[parsed_uri.netloc]._path

        return os.path.join(
            module_path,
            parsed_uri.path.lstrip("/"),
        )

    raise ValueError(f"The path is missing a known prefix: {raw_path}")


@inmanta.plugins.plugin
def get_config_value(config: "dict", dict_path: "string") -> "any":  # type: ignore
    """
    Get an element from the config using its dict_path.
    """
    import inmanta_plugins.config.utils

    assert isinstance(config, inmanta.execute.proxy.DictProxy)
    # Get the id of the object in the model, the wrapper has a very short lifetime
    # and its id could be reused for different model objects.
    instance = config._get_instance()
    wrapped_config_id = id(instance)

    if wrapped_config_id not in CONFIG_CACHE:
        # This is nasty, but dict_patch expressions don't work on DictProxy, so we need to
        # convert the dict proxy to an actual dict.
        # We HAVE to save the instance in the cache, to make sure its object doesn't get
        # garbage collected and its id reused by another object.  This is because this function
        # might also be called from a python context, where all created objects might have a
        # shorter lifetime that the compile process running.
        CONFIG_CACHE[wrapped_config_id] = (
            instance,
            inmanta_plugins.config.utils.unwrap(config),
        )

    return inmanta.util.dict_path.to_path(dict_path).get_element(
        CONFIG_CACHE[wrapped_config_id][1]
    )


@inmanta.plugins.plugin
def get_config_value_as_string(config: "dict", dict_path: "string") -> "string":  # type: ignore
    """
    Get an element from the config using its dict_path.  The element returned will be
    of type string.  If the value we got from the configuration is not a string, an exception
    is raised.
    """
    elem = get_config_value(config, dict_path)
    if not isinstance(elem, str):
        raise inmanta.plugins.PluginException(
            f"Configuration element at path `{dict_path}` should be "
            f"of type `str` but was of type `{type(elem).__name__}`"
        )

    return elem


@inmanta.plugins.plugin
def get_config_value_as_bool(config: "dict", dict_path: "string") -> "bool":  # type: ignore
    """
    Get an element from the config using its dict_path.  The element returned will be
    of type bool.  If the value we got from the configuration is not a boolean, an exception
    is raised.
    """
    elem = get_config_value(config, dict_path)
    if not isinstance(elem, bool):
        raise inmanta.plugins.PluginException(
            f"Configuration element at path `{dict_path}` should be "
            f"of type `bool` but was of type `{type(elem).__name__}`"
        )

    return elem


@inmanta.plugins.plugin
def get_config_value_as_int(config: "dict", dict_path: "string") -> "int":  # type: ignore
    """
    Get an element from the config using its dict_path.  The element returned will be
    of type int.  If the value we got from the configuration is not an integer, an exception
    is raised.
    """
    elem = get_config_value(config, dict_path)
    if not isinstance(elem, int):
        raise inmanta.plugins.PluginException(
            f"Configuration element at path `{dict_path}` should be "
            f"of type `int` but was of type `{type(elem).__name__}`"
        )

    return elem


@inmanta.plugins.deprecated(replaced_by="config::get_config_value_as_float")
@inmanta.plugins.plugin
def get_config_value_as_number(config: "dict", dict_path: "string") -> "any":  # type: ignore
    """
    DEPRECATED The usage of the number type is deprecated, use floats instead.

    Get an element from the config using its dict_path.  The element returned will be
    of type number.  If the value we got from the configuration is not a float nor an
    integer, an exception is raised.
    """
    elem = get_config_value(config, dict_path)
    if isinstance(elem, float) or isinstance(elem, int):
        return elem

    raise inmanta.plugins.PluginException(
        f"Configuration element at path `{dict_path}` should be "
        f"of type `float` or `int` but was of type `{type(elem).__name__}`"
    )


@inmanta.plugins.plugin
def get_config_value_as_float(config: "dict", dict_path: "string") -> "float":  # type: ignore
    """
    Get an element from the config using its dict_path.  The element returned will be
    of type float.  If the value we got from the configuration is not a float nor an
    integer, an exception is raised.
    """
    elem = get_config_value(config, dict_path)
    if isinstance(elem, float):
        return elem

    raise inmanta.plugins.PluginException(
        f"Configuration element at path `{dict_path}` should be "
        f"of type `float` but was of type `{type(elem).__name__}`"
    )


def get_template_value(  # type: ignore
    ctx: inmanta.plugins.Context,
    config: "dict",  # type: ignore
    dict_path: "string",  # type: ignore
    **kwargs: "any",  # type: ignore
) -> "any":  # type: ignore
    """
    Get an element from the config using its dict_path.  If the value is a template path,
    the template will be rendered using the instance passed in argument and the additional values
    in kwargs.

    :param config: The config dict that the value should be taken from.
    :param dict_path: The dict_path pointing to the desired value
    :param kwargs: Any entity or primitive value that should be accessible to the template.
    """
    # Getting the template path from the config
    template_path = get_config_value(config, dict_path)

    if not isinstance(template_path, str):
        # This can not be a template path, we then default to the value
        return template_path

    try:
        resolved_template_path: str = resolve_path(template_path)
    except ValueError:
        # This is not a path we know how to resolve, it can not be a template path
        # We then default to the value
        return template_path

    if not resolved_template_path.endswith(".j2"):
        # This is not a path pointing to a jinja file, we then default to the value
        return template_path

    # Setting up the jinja2 environment
    global jinja2_env
    if jinja2_env is None:
        jinja2_env = jinja2.Environment(undefined=jinja2.StrictUndefined)

        # Registering all plugins as filters
        def curywrapper(func: inmanta.plugins.Plugin) -> typing.Callable:
            def safewrapper(*args, **kwargs) -> typing.Any:

                # Make sure that a plugin with a Context argument can be called
                # inside a template
                if func._context != -1:
                    new_args = list(args)
                    new_args.insert(func._context, ctx)
                    args = tuple(new_args)

                return inmanta_plugins.std.JinjaDynamicProxy.return_value(
                    func(*args, **kwargs)
                )

            return safewrapper

        for name, cls in ctx.get_compiler().get_plugins().items():
            jinja2_env.filters[name.replace("::", ".")] = curywrapper(cls)

    # Reading the template string and building the template object
    template_string = pathlib.Path(resolved_template_path).read_text()
    template = jinja2_env.from_string(template_string)

    try:
        return template.render(
            config=inmanta_plugins.std.JinjaDynamicProxy.return_value(config),
            **{
                k: inmanta_plugins.std.JinjaDynamicProxy.return_value(v)
                for k, v in kwargs.items()
            },
        )
    except jinja2.exceptions.UndefinedError as e:
        raise inmanta.ast.NotFoundException(ctx.owner, "", e.message)


@inmanta.plugins.plugin
def get_config_template_value(  # type: ignore
    ctx: inmanta.plugins.Context,
    config: "dict",  # type: ignore
    dict_path: "string",  # type: ignore
    instance: "std::Entity?" = None,  # type: ignore
    kwargs: "any" = None,  # type: ignore
) -> "any":  # type: ignore
    """
    Get an element from the config using its dict_path.  If the value is a template path,
    the template will be rendered using the instance passed in argument and the additional values
    in kwargs.

    :param config: The config dict that the value should be taken from.
    :param dict_path: The dict_path to the desired value
    :param instance: The instance that can be accessed during the template rendering
    :param kwargs: Additional values that can be accessed during the template rendering.
    """
    return get_template_value(
        ctx,
        config,
        dict_path,
        instance=instance,
        **(kwargs or {}),
    )


def get_template_value_as_string(
    ctx: inmanta.plugins.Context,
    config: "dict",  # type: ignore
    dict_path: "string",  # type: ignore
    **kwargs: "any",  # type: ignore
) -> "string":  # type: ignore
    """
    Get an element from the config using its dict_path.  If the value is a template path,
    the template will be rendered using the instance passed in argument and the additional values
    in kwargs.  The element returned will be of type string.  If the value we got from the
    configuration is not a string, an exception is raised.

    :param config: The config dict that the value should be taken from.
    :param dict_path: The dict_path pointing to the desired value
    :param kwargs: Any entity or primitive value that should be accessible to the template.
    """
    elem = get_template_value(ctx, config, dict_path, **kwargs)

    if not isinstance(elem, str):
        raise inmanta.plugins.PluginException(
            f"Configuration element at path `{dict_path}` should be "
            f"of type `str` but was of type `{type(elem).__name__}`"
        )

    return elem


@inmanta.plugins.plugin
def get_config_template_value_as_string(  # type: ignore
    ctx: inmanta.plugins.Context,
    config: "dict",  # type: ignore
    dict_path: "string",  # type: ignore
    instance: "std::Entity?" = None,  # type: ignore
    kwargs: "any" = None,  # type: ignore
) -> "string":  # type: ignore
    """
    Get an element from the config using its dict_path.  If the value is a template path,
    the template will be rendered using the instance passed in argument and the additional values
    in kwargs.  The element returned will be of type string.  If the value we got from the
    configuration is not a string, an exception is raised.

    :param config: The config dict that the value should be taken from.
    :param dict_path: The dict_path to the desired value
    :param instance: The instance that can be accessed during the template rendering
    :param kwargs: Additional values that can be accessed during the template rendering
    """
    return get_template_value_as_string(
        ctx,
        config,
        dict_path,
        instance=instance,
        **(kwargs or {}),
    )


def get_template_value_as_bool(
    ctx: inmanta.plugins.Context,
    config: "dict",  # type: ignore
    dict_path: "string",  # type: ignore
    **kwargs: "any",  # type: ignore
) -> "bool":  # type: ignore
    """
    Get an element from the config using its dict_path.  If the value is a template path,
    the template will be rendered using the instance passed in argument and the additional values
    in kwargs.  The element returned will be of type bool.  If the value we got from the
    configuration is not a boolean, an exception is raised.

    :param config: The config dict that the value should be taken from.
    :param dict_path: The dict_path pointing to the desired value
    :param kwargs: Any entity or primitive value that should be accessible to the template.
    """
    elem = get_template_value(ctx, config, dict_path, **kwargs)

    if isinstance(elem, bool):
        # In case the returned value hasn't been rendered through a template
        return elem

    if elem.lower() == "true":
        return True

    if elem.lower() == "false":
        return False

    raise inmanta.plugins.PluginException(
        f"Configuration element at path `{dict_path}` should be "
        f"of type `bool` but the value `{elem}` can not be parsed as such"
    )


@inmanta.plugins.plugin
def get_config_template_value_as_bool(  # type: ignore
    ctx: inmanta.plugins.Context,
    config: "dict",  # type: ignore
    dict_path: "string",  # type: ignore
    instance: "std::Entity?" = None,  # type: ignore
    kwargs: "any" = None,  # type: ignore
) -> "bool":  # type: ignore
    """
    Get an element from the config using its dict_path.  If the value is a template path,
    the template will be rendered using the instance passed in argument and the additional values
    in kwargs.  The element returned will be of type bool.  If the value we got from the
    configuration is not a boolean, an exception is raised.

    :param config: The config dict that the value should be taken from.
    :param dict_path: The dict_path to the desired value
    :param instance: The instance that can be accessed during the template rendering
    :param kwargs: Additional values that can be accessed during the template rendering
    """
    return get_template_value_as_bool(
        ctx,
        config,
        dict_path,
        instance=instance,
        **(kwargs or {}),
    )


def get_template_value_as_int(
    ctx: inmanta.plugins.Context,
    config: "dict",  # type: ignore
    dict_path: "string",  # type: ignore
    **kwargs: "any",  # type: ignore
) -> "int":  # type: ignore
    """
    Get an element from the config using its dict_path.  If the value is a template path,
    the template will be rendered using the instance passed in argument and the additional values
    in kwargs.  The element returned will be of type int.  If the value we got from the
    configuration is not an integer, an exception is raised.

    :param config: The config dict that the value should be taken from.
    :param dict_path: The dict_path pointing to the desired value
    :param kwargs: Any entity or primitive value that should be accessible to the template.
    """
    elem = get_template_value(ctx, config, dict_path, **kwargs)

    try:
        return int(elem)
    except ValueError as e:
        raise inmanta.plugins.PluginException(
            f"Configuration element at path `{dict_path}` should be "
            f"of type `int` but the value `{elem}` can not be parsed as such:\n{repr(e)}"
        )


@inmanta.plugins.plugin
def get_config_template_value_as_int(  # type: ignore
    ctx: inmanta.plugins.Context,
    config: "dict",  # type: ignore
    dict_path: "string",  # type: ignore
    instance: "std::Entity?" = None,  # type: ignore
    kwargs: "any" = None,  # type: ignore
) -> "int":  # type: ignore
    """
    Get an element from the config using its dict_path.  If the value is a template path,
    the template will be rendered using the instance passed in argument and the additional values
    in kwargs.  The element returned will be of type int.  If the value we got from the
    configuration is not an integer, an exception is raised.

    :param config: The config dict that the value should be taken from.
    :param dict_path: The dict_path to the desired value
    :param instance: The instance that can be accessed during the template rendering
    :param kwargs: Additional values that can be accessed during the template rendering
    """
    return get_template_value_as_int(
        ctx,
        config,
        dict_path,
        instance=instance,
        **(kwargs or {}),
    )


def get_template_value_as_float(
    ctx: inmanta.plugins.Context,
    config: "dict",  # type: ignore
    dict_path: "string",  # type: ignore
    **kwargs: "any",  # type: ignore
) -> "float":  # type: ignore
    """
    Get an element from the config using its dict_path.  If the value is a template path,
    the template will be rendered using the instance passed in argument and the additional values
    in kwargs.  The element returned will be of type int.  If the value we got from the
    configuration is not an integer, an exception is raised.

    :param config: The config dict that the value should be taken from.
    :param dict_path: The dict_path pointing to the desired value
    :param kwargs: Any entity or primitive value that should be accessible to the template.
    """
    elem = get_template_value(ctx, config, dict_path, **kwargs)

    try:
        return float(elem)
    except ValueError as e:
        raise inmanta.plugins.PluginException(
            f"Configuration element at path `{dict_path}` should be "
            f"of type `float` but the value `{elem}` can not be parsed as such:\n{repr(e)}"
        )


@inmanta.plugins.deprecated(replaced_by="config::get_template_value_as_float")
@inmanta.plugins.plugin
def get_config_template_value_as_number(  # type: ignore
    ctx: inmanta.plugins.Context,
    config: "dict",  # type: ignore
    dict_path: "string",  # type: ignore
    instance: "std::Entity?" = None,  # type: ignore
    kwargs: "any" = None,  # type: ignore
) -> "any":  # type: ignore
    """
    DEPRECATED The usage of the number type is deprecated, use floats instead.

    Get an element from the config using its dict_path.  If the value is a template path,
    the template will be rendered using the instance passed in argument and the additional values
    in kwargs.  The element returned will be of type number.  If the value we got from the
    configuration is not a float nor an integer, an exception is raised.

    :param config: The config dict that the value should be taken from.
    :param dict_path: The dict_path to the desired value
    :param instance: The instance that can be accessed during the template rendering
    :param kwargs: Additional values that can be accessed during the template rendering
    """
    return get_template_value_as_float(
        ctx,
        config,
        dict_path,
        instance=instance,
        **(kwargs or {}),
    )


if pkg_resources.parse_version(inmanta.COMPILER_VERSION) >= pkg_resources.parse_version(
    "2024.1"
):
    # Some of the plugins defined in this module can not be used with
    # older versions of the compiler.  This if block is only executed when
    # such version of the compiler (or greater) is installed.
    # Register all **kwargs plugins
    inmanta.plugins.plugin(get_template_value)
    inmanta.plugins.plugin(get_template_value_as_string)
    inmanta.plugins.plugin(get_template_value_as_bool)
    inmanta.plugins.plugin(get_template_value_as_int)
    inmanta.plugins.plugin(get_template_value_as_float)
