"""
:copyright: 2022 Inmanta
:contact: code@inmanta.com
:license: Inmanta EULA
"""

import inmanta.ast
import inmanta.execute.proxy


def unwrap(item: object) -> object:
    """
    Converts a value from the plugin domain to the python domain.

    This method is based on DynamicProxy.unwrap, which doesn't handle the None values
    as we would like to, so we only change this part of its behavior.
    https://github.com/inmanta/inmanta-core/blob/88d8465d487e432ec104e207682e783fb9aeae66/src/inmanta/execute/proxy.py#L93
    """
    if item is None:
        return None

    if isinstance(item, inmanta.execute.proxy.NoneValue):
        return None

    if isinstance(item, inmanta.execute.proxy.DynamicProxy):
        item = item._get_instance()

    if isinstance(item, list):
        return [unwrap(x) for x in item]

    if isinstance(item, dict):

        def recurse_dict_item(
            key_value: tuple[object, object],
        ) -> tuple[object, object]:
            (key, value) = key_value
            if not isinstance(key, str):
                raise inmanta.ast.RuntimeException(
                    None,
                    "dict keys should be strings, got %s of type %s with dict value %s"
                    % (key, type(key), value),
                )
            return (key, unwrap(value))

        return dict(map(recurse_dict_item, item.items()))

    return item
