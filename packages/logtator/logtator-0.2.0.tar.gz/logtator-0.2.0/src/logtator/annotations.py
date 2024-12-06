import logging
import typing


class Logger(logging.Logger):
    def debug(self, msg: object, *args: typing.Any, **kwargs: typing.Any) -> None: ...

    def info(self, msg: object, *args: typing.Any, **kwargs: typing.Any) -> None: ...

    def warning(self, msg: object, *args: typing.Any, **kwargs: typing.Any) -> None: ...

    def error(self, msg: object, *args: typing.Any, **kwargs: typing.Any) -> None: ...

    def exception(
        self, msg: object, *args: typing.Any, **kwargs: typing.Any
    ) -> None: ...

    def critical(
        self, msg: object, *args: typing.Any, **kwargs: typing.Any
    ) -> None: ...

    def log(
        self, level: int, msg: object, *args: typing.Any, **kwargs: typing.Any
    ) -> None: ...

    def bind(self, **kwargs: typing.Any) -> "Logger": ...  # type: ignore[empty-body]
