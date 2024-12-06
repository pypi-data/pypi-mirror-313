from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ipfabric.models.users import User

logger = logging.getLogger("ipfabric")


def api_insuf_rights(user: User):
    msg = f'API_INSUFFICIENT_RIGHTS for user "{user.username}" '
    if user.token:
        msg += f'token "{user.token.description}" '
    return msg
