
from .private import private_routers
from .errors import errors_router
from .echo import echo_router

routers_list = [
    *private_routers,
    errors_router,
    echo_router,
]

__all__ = [
    "routers_list",
]
