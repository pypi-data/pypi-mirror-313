from __future__ import annotations

from typing import Any, Callable, ParamSpec, Sequence, TypeVar

from starlette.applications import Starlette
from starlette.datastructures import State
from starlette.middleware import Middleware
from starlette.routing import BaseRoute
from starlette.types import ASGIApp

from siteforge.routing import Router

_P = ParamSpec("_P")
_R = TypeVar("_R")


class SiteForge(Starlette):
    """SiteForge main class."""

    router: Router

    def __init__(
        self,
        debug: bool = False,
        routes: Sequence[BaseRoute] | None = None,
        middleware: Sequence[Middleware] | None = None,
        # TODO: Add lifespan type hint.
        lifespan: Any | None = None,
    ) -> None:
        self.debug = debug
        # TODO: Remove the state.
        self.state = State()
        self.router = Router(routes, lifespan=lifespan)
        self.exception_handlers = {}
        self.user_middleware = [] if middleware is None else list(middleware)
        self.middleware_stack: ASGIApp | None = None

    def head(
        self, path: str, name: str | None = None, include_in_schema: bool = True
    ) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
        return self.router.head(path, name=name, include_in_schema=include_in_schema)

    def get(
        self, path: str, name: str | None = None, include_in_schema: bool = True
    ) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
        return self.router.get(path, name=name, include_in_schema=include_in_schema)

    def post(
        self, path: str, name: str | None = None, include_in_schema: bool = True
    ) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
        return self.router.post(path, name=name, include_in_schema=include_in_schema)

    def put(
        self, path: str, name: str | None = None, include_in_schema: bool = True
    ) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
        return self.router.put(path, name=name, include_in_schema=include_in_schema)

    def delete(
        self, path: str, name: str | None = None, include_in_schema: bool = True
    ) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
        return self.router.delete(path, name=name, include_in_schema=include_in_schema)

    def patch(
        self, path: str, name: str | None = None, include_in_schema: bool = True
    ) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
        return self.router.patch(path, name=name, include_in_schema=include_in_schema)
