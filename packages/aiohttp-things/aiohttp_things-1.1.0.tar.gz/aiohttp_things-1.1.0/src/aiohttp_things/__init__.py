from importlib.metadata import version

from aiohttp_things import views, web_handlers
from aiohttp_things.web_handlers import (
    AbstractHandler,
    ContextMixin,
    HTTPMethodMixin,
    ItemMixin,
    Jinja2Mixin,
    JSONMixin,
    ListMixin,
    PaginationMixin,
    PrimaryKeyMixin,
    ResponseAutoformatMixin,
    ResponseFormatMixin,
)

__version__ = version(__package__)
__all__ = [
    "AbstractHandler",
    "ContextMixin",
    "HTTPMethodMixin",
    "ItemMixin",
    "JSONMixin",
    "Jinja2Mixin",
    "ListMixin",
    "PaginationMixin",
    "PrimaryKeyMixin",
    "ResponseAutoformatMixin",
    "ResponseFormatMixin",
    "views",
    "web_handlers",
]
