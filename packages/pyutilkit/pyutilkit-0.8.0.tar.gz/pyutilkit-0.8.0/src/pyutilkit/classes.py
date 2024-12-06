from __future__ import annotations

from typing import cast


class Singleton(type):
    instance: type[Singleton] | None

    def __init__(
        cls, name: str, bases: tuple[type[object], ...], namespace: dict[str, object]
    ) -> None:
        super().__init__(name, bases, namespace)
        cls.instance = None

    def __call__(cls) -> type[Singleton]:
        if cls.instance is None:
            cls.instance = super().__call__()
        return cast(type[Singleton], cls.instance)
