import linecache
import logging
import sys
import types
import typing

from . import annotations


def get_logger(name: str) -> annotations.Logger:
    return logging.getLogger(name)  # type: ignore[return-value]


getLogger = get_logger
log = get_logger(__name__)


class Logtator(logging.Logger):
    def makeRecord(
        self,
        name: str,
        level: int,
        fn: str,
        lno: int,
        msg: object,
        args: typing.Tuple[object, ...] | typing.Mapping[str, object],
        exc_info: tuple[type[BaseException], BaseException, types.TracebackType | None]
        | tuple[None, None, None]
        | None,
        func: str | None = None,
        extra: typing.Mapping[str, object] | None = None,
        sinfo: str | None = None,
        **kwargs: typing.Any,
    ) -> logging.LogRecord:
        rv = logging._logRecordFactory(  # type: ignore[attr-defined]
            name, level, fn, lno, msg, args, exc_info, func, sinfo
        )
        rv.extra = extra
        rv.kwargs = kwargs
        return rv  # type: ignore[no-any-return]

    def _log(
        self,
        level: int,
        msg: object,
        args: typing.Tuple[object, ...] | typing.Mapping[str, object],
        exc_info: bool
        | tuple[type[BaseException], BaseException, types.TracebackType | None]
        | tuple[None, None, None]
        | BaseException
        | None
        | None = None,
        extra: typing.Mapping[str, object] | None = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        **kwargs: typing.Any,
    ) -> None:
        sinfo = None
        if logging._srcfile:
            try:
                # We need to increase `stacklevel` by 1 otherwise caller would be this
                # line instead of the actual caller.
                fn, lno, func, sinfo = self.findCaller(stack_info, stacklevel + 1)
            except ValueError:
                fn, lno, func = "(unknown file)", 0, "(unknown function)"
        else:
            fn, lno, func = "(unknown file)", 0, "(unknown function)"
        if exc_info:
            if isinstance(exc_info, BaseException):
                exc_info = (type(exc_info), exc_info, exc_info.__traceback__)
            elif not isinstance(exc_info, tuple):
                exc_info = sys.exc_info()
        record = self.makeRecord(
            self.name,
            level,
            fn,
            lno,
            msg,
            args,
            exc_info,  # type: ignore[arg-type]
            func,
            extra,
            sinfo,
            **kwargs,
        )
        self.handle(record)

    def _log_warning(
        self,
        message: str,
        category: str,
        filename: str,
        lineno: int,
        file: str | None = None,
        line: str | None = None,
    ) -> None:
        if file:
            log.debug("warning-file-ignored", file=file)
        if not line:
            line = linecache.getline(filename, lineno)
        record = self.makeRecord(
            self.name,
            logging.WARNING,
            filename,
            lineno,
            message,
            (),
            None,
            category=category,
            location=f"{filename}:{lineno}",
            line=line,
        )
        self.handle(record)

    def addHandler(self, handler: logging.Handler) -> None:
        log.debug(
            "handler-thrown-away",
            logger=self.name,
            handler=handler.name,
        )

    def bind(self, **kwargs: typing.Any) -> "_Adapter":
        return _Adapter(self, **kwargs)


class _Adapter(logging.LoggerAdapter[Logtator]):
    def __init__(self, logger: Logtator, **kwargs: typing.Any) -> None:
        super().__init__(logger)
        self.kwargs = kwargs

    def process(
        self, msg: str, kwargs: typing.Any
    ) -> typing.Tuple[str, typing.MutableMapping[str, typing.Any]]:
        kwargs.update(self.kwargs)
        return msg, kwargs
