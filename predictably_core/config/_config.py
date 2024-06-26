#!/usr/bin/env python3 -u
# copyright: predict-ably, BSD-3-Clause License (see LICENSE file)
# Includes functionality like get_config, set_config, and config_context
# that is similar to scikit-learn and skbase. These elements are copyrighted by
# their respective developers. For conditions see
# https://github.com/scikit-learn/scikit-learn/blob/main/COPYING
# https://github.com/sktime/skbase/blob/main/LICENSE
"""Implement logic for global configuration of predictably_core.

Allows users to configure `predictably_core`.
"""

import threading
from contextlib import contextmanager
from typing import Any, Dict, Iterator, List, Literal, Optional

from predictably_core.config._config_param_setting import GlobalConfigParamSetting

__author__: List[str] = ["RNKuhns"]
__all__: List[str] = [
    "config_context",
    "get_config",
    "reset_config",
    "set_config",
]

GlobalConfigParam = Literal["print_changed_only", "display"]

_CONFIG_REGISTRY: Dict[GlobalConfigParam, GlobalConfigParamSetting] = {
    "print_changed_only": GlobalConfigParamSetting(
        name="print_changed_only",
        expected_type=bool,
        allowed_values=(True, False),
        default_value=True,
    ),
    "display": GlobalConfigParamSetting(
        name="display",
        expected_type=str,
        allowed_values=("text", "diagram"),
        default_value="text",
    ),
}

_GLOBAL_CONFIG_DEFAULT: Dict[GlobalConfigParam, Any] = {
    config_settings.name: config_settings.default_value
    for _, config_settings in _CONFIG_REGISTRY.items()
}

global_config = _GLOBAL_CONFIG_DEFAULT.copy()

_THREAD_LOCAL_DATA = threading.local()


def _get_threadlocal_config() -> Dict[GlobalConfigParam, Any]:
    """Get a threadlocal **mutable** configuration.

    If the configuration does not exist, copy the default global configuration.

    Returns
    -------
    dict
        Threadlocal global config or copy of default global configuration.
    """
    if not hasattr(_THREAD_LOCAL_DATA, "global_config"):
        _THREAD_LOCAL_DATA.global_config = global_config.copy()
    return _THREAD_LOCAL_DATA.global_config  # type: ignore


def get_config(default: bool = False) -> Dict[GlobalConfigParam, Any]:
    """Retrieve current values for configuration set by :meth:`set_config`.

    Will return the default configuration if know updated configuration has
    been set by :meth:`set_config`.

    Parameters
    ----------
    default : bool, default=False
        Whether to return the default current configuration or the
        default configuration.

        - If False (the default), then the current configuration is is returned.
        - If True, then return the package's default configuration.

    Returns
    -------
    dict
        The configurable settings (keys) and their default values (values).

    See Also
    --------
    config_context :
        Configuration context manager.
    set_config :
        Set global configuration.
    reset_config :
        Reset configuration to ``predictably_core`` default.

    Examples
    --------
    >>> from predictably_core.config import get_config
    >>> get_config()  # doctest: +ELLIPSIS
    {'print_changed_only': True, ...}
    """
    if default:
        return _GLOBAL_CONFIG_DEFAULT.copy()
    else:
        return _get_threadlocal_config().copy()


def set_config(
    *,
    print_changed_only: Optional[bool] = None,
    display: Optional[Literal["text", "diagram"]] = None,
    local_threadsafe: bool = False,
) -> None:
    """Set global configuration.

    Allows the ``predictably_core`` global configuration to be updated.

    Parameters
    ----------
    print_changed_only : bool, default=None
        If True, only the parameters that were set to non-default
        values will be printed when printing a BaseObject instance. For example,
        ``print(SVC())`` while True will only print 'SVC()', but would print
        'SVC(C=1.0, cache_size=200, ...)' with all the non-changed parameters
        when False. If None, the existing value won't change.
    display : {'text', 'diagram'}, default=None
        If 'diagram', instances inheriting from BaseOBject will be displayed
        as a diagram in a Jupyter lab or notebook context. If 'text', instances
        inheriting from BaseObject will be displayed as text. If None, the
        existing value won't change.
    local_threadsafe : bool, default=False
        If False, set the backend as default for all threads.

    Returns
    -------
    None
        No output returned.

    See Also
    --------
    config_context :
        Configuration context manager.
    get_config :
        Retrieve current global configuration values.
    reset_config :
        Reset configuration to default.

    Examples
    --------
    >>> from predictably_core.config import get_config, set_config
    >>> get_config()  # doctest: +ELLIPSIS
    {'print_changed_only': True, ...}
    >>> set_config(display='diagram')
    >>> get_config()  # doctest: +ELLIPSIS
    {'print_changed_only': True, ...}
    """
    local_config = _get_threadlocal_config()
    msg = "Attempting to set an invalid value for a global configuration.\n"
    msg += "Using current configuration value of parameter as a result.\n"

    def _update_local_config(
        local_config: Dict[GlobalConfigParam, Any],
        param: Any,
        param_name: str,
        msg: str,
    ) -> Dict[GlobalConfigParam, Any]:
        """Update a local config with a parameter value.

        Utility function used to update the local config dictionary.

        Parameters
        ----------
        local_config : dict[GlobalConfigParam, Any]
            The local configuration to update.
        param : Any
            The parameter value to update.
        param_name : str
            The name of the parameter to update.
        msg : str
            Message to pass to `GlobalConfigParam.get_valid_param_or_default`.

        Returns
        -------
        dict
            The updated local configuration.
        """
        config_reg = _CONFIG_REGISTRY.copy()
        value = config_reg[param_name].get_valid_param_or_default(
            param,
            default_value=local_config[param_name],
            msg=msg,
        )
        local_config[param_name] = value
        return local_config

    if print_changed_only is not None:
        local_config = _update_local_config(
            local_config, print_changed_only, "print_changed_only", msg
        )
    if display is not None:
        local_config = _update_local_config(local_config, display, "display", msg)

    if not local_threadsafe:
        global_config.update(local_config)

    return None


def reset_config() -> None:
    """Reset the global configuration to the default.

    Will remove any user updates to the global configuration and reset the values
    back to the ``predictably_core`` defaults.

    Returns
    -------
    None
        No output returned.

    See Also
    --------
    config_context :
        Configuration context manager.
    get_config :
        Retrieve current global configuration values.
    set_config :
        Set global configuration.

    Examples
    --------
    >>> from predictably_core.config import get_config, set_config, reset_config
    >>> get_config()  # doctest: +ELLIPSIS
    {'print_changed_only': True, ...}
    >>> set_config(display='diagram')
    >>> get_config()  # doctest: +ELLIPSIS
    {'print_changed_only': True, ...}
    >>> get_config() == get_config(default=True)
    False
    >>> reset_config()
    >>> get_config()  # doctest: +ELLIPSIS
    {'print_changed_only': True, ...}
    >>> get_config() == get_config(default=True)
    True
    """
    default_config = get_config(default=True)
    set_config(**default_config)
    return None


@contextmanager
def config_context(
    *,
    print_changed_only: Optional[bool] = None,
    display: Optional[Literal["text", "diagram"]] = None,
    local_threadsafe: bool = False,
) -> Iterator[None]:
    """Context manager for global configuration.

    Provides the ability to run code using different configuration without
    having to update the global config.

    Parameters
    ----------
    print_changed_only : bool, default=None
        If True, only the parameters that were set to non-default
        values will be printed when printing a Model instance. For example,
        ``print(Model())`` while True will only print 'Model()', but would print
        'Model(C=1.0, cache_size=200, ...)' with all the unchanged parameters
        when False. If None, the existing value won't change.
    display : {'text', 'diagram'}, default=None
        If 'diagram', instances inheriting from BaseOBject will be displayed
        as a diagram in a Jupyter lab or notebook context. If 'text', instances
        inheriting from BaseObject will be displayed as text. If None, the
        existing value won't change.
    local_threadsafe : bool, default=False
        If False, set the config as default for all threads.

    Yields
    ------
    None
        No output returned.

    See Also
    --------
    get_config :
        Retrieve current values of the global configuration.
    set_config :
        Set global configuration.
    reset_config :
        Reset configuration to ``predictably_core`` default.

    Notes
    -----
    All settings, not just those presently modified, will be returned to
    their previous values when the context manager is exited.

    Examples
    --------
    >>> from predictably_core.config import config_context
    >>> with config_context(display='diagram'):
    ...     pass
    """
    old_config = get_config()
    set_config(
        print_changed_only=print_changed_only,
        display=display,
        local_threadsafe=local_threadsafe,
    )

    try:
        yield
    finally:
        set_config(**old_config)
