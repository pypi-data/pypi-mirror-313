from __future__ import annotations

from typing import Any, Callable, ParamSpec, TypeVar

from starlette.routing import BaseRoute, Host, Mount, Route, Router as _Router, WebSocketRoute

__all__ = ("BaseRoute", "Host", "Mount", "Route", "Router", "WebSocketRoute")

_P = ParamSpec("_P")
_R = TypeVar("_R")

# TODO: Use the HTTPMethod.
# HTTPMethod = Literal["HEAD", "GET", "POST", "PUT", "DELETE", "PATCH"]


class Router(_Router):
    def add_route(
        self,
        path: str,
        endpoint: Callable[..., Any],
        methods: list[str] | None = None,
        name: str | None = None,
        include_in_schema: bool = True,
    ) -> None:
        return super().add_route(path, endpoint, methods, name, include_in_schema)

    def head(
        self, path: str, name: str | None = None, include_in_schema: bool = True
    ) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
        def decorator(func: Callable[_P, _R]) -> Callable[_P, _R]:
            self.add_route(path, func, methods=["HEAD"], name=name, include_in_schema=include_in_schema)
            return func

        return decorator

    def get(
        self, path: str, name: str | None = None, include_in_schema: bool = True
    ) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
        def decorator(func: Callable[_P, _R]) -> Callable[_P, _R]:
            self.add_route(path, func, methods=["GET"], name=name, include_in_schema=include_in_schema)
            return func

        return decorator

    def post(
        self, path: str, name: str | None = None, include_in_schema: bool = True
    ) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
        def decorator(func: Callable[_P, _R]) -> Callable[_P, _R]:
            self.add_route(path, func, methods=["POST"], name=name, include_in_schema=include_in_schema)
            return func

        return decorator

    def put(
        self, path: str, name: str | None = None, include_in_schema: bool = True
    ) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
        def decorator(func: Callable[_P, _R]) -> Callable[_P, _R]:
            self.add_route(path, func, methods=["PUT"], name=name, include_in_schema=include_in_schema)
            return func

        return decorator

    def delete(
        self, path: str, name: str | None = None, include_in_schema: bool = True
    ) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
        def decorator(func: Callable[_P, _R]) -> Callable[_P, _R]:
            self.add_route(path, func, methods=["DELETE"], name=name, include_in_schema=include_in_schema)
            return func

        return decorator

    def patch(
        self, path: str, name: str | None = None, include_in_schema: bool = True
    ) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
        def decorator(func: Callable[_P, _R]) -> Callable[_P, _R]:
            self.add_route(path, func, methods=["PATCH"], name=name, include_in_schema=include_in_schema)
            return func

        return decorator
