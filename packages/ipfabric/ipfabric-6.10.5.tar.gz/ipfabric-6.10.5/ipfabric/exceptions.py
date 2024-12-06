from __future__ import annotations

import logging
from typing import TYPE_CHECKING
from warnings import warn

if TYPE_CHECKING:
    from ipfabric.models.users import User

logger = logging.getLogger("ipfabric")


def api_insuf_rights(user: User):
    msg = f'API_INSUFFICIENT_RIGHTS for user "{user.username}" '
    if user.token:
        msg += f'token "{user.token.description}" '
    return msg


def deprecated_args_decorator(  # noqa: C901
    version: str, arg_type=None, no_args: bool = True, kwargs_only: bool = False
):

    def inner(func):

        fname = func.__name__

        def wrapper(*args, **kwargs):
            if arg_type:
                arg_types = [arg_type] if isinstance(arg_type, str) else arg_type
                msg = (
                    f"`{fname}()` no longer accepts parameter of `{arg_type}` and will be removed in version {version}."
                )
                if args:
                    for arg in args:
                        if type(arg).__name__ in arg_types:
                            warn(msg, DeprecationWarning, stacklevel=2)
                            logger.warning(msg)
                if kwargs:
                    for arg in kwargs.values():
                        if type(arg).__name__ in arg_types:
                            warn(msg, DeprecationWarning, stacklevel=2)
                            logger.warning(msg)
            elif no_args and (len(args) > 1 or kwargs):
                warn(
                    f"`{fname}()` parameters are deprecated and will be removed in version {version}.",
                    DeprecationWarning,
                    stacklevel=2,
                )
                logger.warning(f"`{fname}()` parameters are deprecated and will be removed in version {version}.")
            elif kwargs_only and len(args):
                msg = (
                    f"`{fname}()` positional arguments are deprecated and will be removed in version {version}. "
                    f"Please switch to keyword arguments only."
                )
                warn(msg, DeprecationWarning, stacklevel=2)
                logger.warning(msg)
            return func(*args, **kwargs)

        return wrapper

    return inner
