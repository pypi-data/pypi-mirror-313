import logging
import types
import typing
import warnings

from . import _loggers
from . import _settings

log = _loggers.get_logger(__name__)


def _patch_loggers(settings: _settings.Base) -> None:
    # root logger is not in `loggerDict` so we have to patch it separately
    _configure_logger(settings, logging.root)
    for logger in logging.Logger.manager.loggerDict.values():
        _configure_logger(settings, logger)


def _configure_logger(
    settings: _settings.Base, logger: logging.Logger | logging.PlaceHolder
) -> None:
    if isinstance(logger, (_loggers.Logtator, logging.PlaceHolder)):
        return

    logger.makeRecord = types.MethodType(_loggers.Logtator.makeRecord, logger)  # type: ignore[method-assign]
    logger._log = types.MethodType(_loggers.Logtator._log, logger)  # type: ignore[method-assign]
    logger.addHandler = types.MethodType(_loggers.Logtator.addHandler, logger)  # type: ignore[method-assign]
    logger.bind = types.MethodType(_loggers.Logtator.bind, logger)  # type: ignore[attr-defined]

    logger.handlers = []
    logger.propagate = True

    if settings.force_default_level:
        logger.setLevel(settings.default_level)


def _patch_warning(settings: _settings.Base) -> None:
    warnings.showwarning = types.MethodType(
        _loggers.Logtator._log_warning, logging.root
    )
    if settings.reset_warning_filters:
        warnings.filters = []


def _log_known_loggers() -> None:
    loggers: typing.List[str | typing.Dict[str, typing.Any]] = []
    unique_loggers = set()

    for logger in logging.Logger.manager.loggerDict.values():
        if isinstance(logger, logging.PlaceHolder):
            continue
        main_logger = logger.name.split(".")[0]
        if main_logger in unique_loggers:
            continue
        if log.level <= logging.DEBUG:
            loggers.append(
                {
                    "name": logger.name,
                    "level": logger.level,
                    "propagate": logger.propagate,
                    "disabled": logger.disabled,
                    "handlers": logger.handlers,
                }
            )
            continue
        loggers.append(main_logger)
        unique_loggers.add(main_logger)

    loggers.sort(key=lambda x: x["name"] if isinstance(x, dict) else x)
    log.info("known-loggers", loggers=loggers)


def patch(settings: _settings.Base) -> None:
    if logging.getLoggerClass() is _loggers.Logtator:
        log.debug("already-patched")
        return

    logging.setLoggerClass(_loggers.Logtator)
    logging.root.setLevel(settings.default_level)
    logging.lastResort.setLevel(settings.default_level)  # type: ignore[union-attr]
    logging._defaultFormatter = settings.logs_formatter  # type: ignore[attr-defined]

    _patch_warning(settings)
    _patch_loggers(settings)
    _log_known_loggers()
