"""
Expandable abstraction and mixins for AIOHTTP class based request handlers.
"""

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from collections.abc import Awaitable, Generator, Iterable
from typing import Any, Callable

from aiohttp.abc import AbstractView
from aiohttp.hdrs import METH_ALL
from aiohttp.web import Request, Response, StreamResponse, json_response
from aiohttp.web_exceptions import HTTPMethodNotAllowed

try:
    from aiohttp_jinja2 import render_template_async

    HAS_AIOHTTP_JINJA2 = True
except ImportError:
    HAS_AIOHTTP_JINJA2 = False


REQUESTED_METHOD = Callable[[], Awaitable[StreamResponse]]


class AbstractHandler(AbstractView, metaclass=ABCMeta):
    def __init__(self, request: Request) -> None:
        super().__init__(request)

    def __await__(self) -> Generator[Any, None, StreamResponse]:
        return self.handle_request().__await__()

    @abstractmethod
    async def handle_request(self) -> StreamResponse: ...

    @abstractmethod
    async def determine_requested_method(
        self,
    ) -> REQUESTED_METHOD | None: ...


class ContextMixin(AbstractView, metaclass=ABCMeta):
    context: dict[str, Any]

    def __init__(self, request: Request) -> None:
        super().__init__(request)
        self.context = {}


class HTTPMethodMixin(AbstractHandler):
    async def determine_requested_method(self) -> REQUESTED_METHOD:
        await super().determine_requested_method()  # type: ignore

        http_method_name = self.request.method
        if http_method_name not in METH_ALL:
            raise HTTPMethodNotAllowed(
                self.request.method, {m for m in METH_ALL if hasattr(self, m.lower())}
            )

        requested_method: REQUESTED_METHOD | None = getattr(
            self,
            http_method_name.lower(),
            None,
        )
        if requested_method is None:
            raise HTTPMethodNotAllowed(
                self.request.method, {m for m in METH_ALL if hasattr(self, m.lower())}
            )

        return requested_method


class PaginationMixin(AbstractView, metaclass=ABCMeta):
    page: Any = None
    page_adapter: Callable[..., Any]
    page_key: Any = None
    page_key_adapter: Callable[..., Any]
    paginator: Any = None

    def __init__(self, request: Request) -> None:
        super().__init__(request)
        page_key = self.request.rel_url.query.get("page_key")
        if page_key:
            page_key_adapter = getattr(self, "page_key_adapter", lambda v: v)
            self.page_key = page_key_adapter(page_key)


class PrimaryKeyMixin(AbstractView, metaclass=ABCMeta):
    pk: Any = None
    pk_adapter: Callable[..., Any]

    def __init__(self, request: Request) -> None:
        super().__init__(request)
        pk = self.request.match_info.get("pk")
        if pk:
            pk_adapter = getattr(self, "pk_adapter", lambda v: v)
            self.pk = pk_adapter(pk)


class ItemMixin(AbstractView, metaclass=ABCMeta):
    item: Any

    def __init__(self, request: Request) -> None:
        super().__init__(request)
        self.item = None


class ListMixin(AbstractView, metaclass=ABCMeta):
    items: Iterable[Any]

    def __init__(self, request: Request) -> None:
        super().__init__(request)
        self.items = []


class Jinja2Mixin(ContextMixin, metaclass=ABCMeta):
    template: str

    def __init__(self, request: Request) -> None:
        super().__init__(request)
        if not HAS_AIOHTTP_JINJA2:
            msg = (
                "If you want use `Jinja2Mixin`, "
                "then you need install `aiohttp-jinja2` package."
            )
            raise ImportError(msg)

    async def finalize_response(self, **kwargs: Any) -> Response:
        return await render_template_async(
            self.template,
            self.request,
            self.context,
            **kwargs,
        )


class JSONMixin(ContextMixin, metaclass=ABCMeta):
    async def finalize_response(self, **kwargs: Any) -> Response:
        return json_response(self.context, **kwargs)


class ResponseFormatMixin(AbstractView, metaclass=ABCMeta):
    response_format: str

    def __init__(self, request: Request) -> None:
        super().__init__(request)
        self.response_format = self.request.match_info.get("format", ".html")


class ResponseAutoformatMixin(ContextMixin, ResponseFormatMixin):
    template: str

    async def finalize_response(self, **kwargs: Any) -> Response:
        if self.response_format == ".json":
            return json_response(self.context, **kwargs)

        return await render_template_async(
            self.template,
            self.request,
            self.context,
            **kwargs,
        )
