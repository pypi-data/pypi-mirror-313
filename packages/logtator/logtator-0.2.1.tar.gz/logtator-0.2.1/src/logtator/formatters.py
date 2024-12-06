import datetime as dt
import json
import logging
import traceback
import typing

try:
    import ddtrace
except ImportError:
    ddtrace = None  # type: ignore[assignment]

from . import encoders


class HumanReadable(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        if record.exc_info:
            traceback.print_exception(*record.exc_info)
        return (
            f"{record.levelname}: {record.getMessage()} {record.extra or ''} "  # type: ignore[attr-defined]
            f"{record.kwargs or ''}"  # type: ignore[attr-defined]
        ).strip()


class Json(logging.Formatter):
    def __init__(
        self,
        fmt: str | None = None,
        datefmt: str | None = None,
        style: typing.Literal["%", "{", "$"] = "%",
        validate: bool = True,
        *,
        defaults: typing.Dict[str, typing.Any] | None = None,
        flatten_extra: bool = True,
        flatten_kwargs: bool = True,
        nest_record: bool = True,
        add_datadog_fields: bool = False,
        add_google_cloud_fields: bool = False,
    ) -> None:
        super().__init__(
            fmt=fmt, datefmt=datefmt, style=style, validate=validate, defaults=defaults
        )
        self.flatten_extra = flatten_extra
        self.flatten_kwargs = flatten_kwargs
        self.nest_record = nest_record
        self.add_datadog_fields = add_datadog_fields
        # https://cloud.google.com/logging/docs/agent/logging/configuration#special-fields
        self.add_google_cloud_fields = add_google_cloud_fields

    def format(self, record: logging.LogRecord) -> str:
        record_dict = record.__dict__
        record_dict = self._adjust_dict(record, record_dict)

        if self.add_datadog_fields:
            Json._add_datadog_fields(record_dict)
        if self.add_google_cloud_fields:
            Json._add_google_cloud_fields(record, record_dict)
        return json.dumps(record_dict, cls=encoders.Base)

    def _adjust_dict(
        self, record: logging.LogRecord, record_dict: typing.Dict[str, typing.Any]
    ) -> typing.Dict[str, typing.Any]:
        if self.nest_record:
            record_dict = {"record": record.__dict__}
        record_dict["message"] = record.getMessage()

        if self.flatten_extra:
            record_dict.update(
                record_dict.get("record", record_dict).pop("extra", {}) or {}
            )
        if self.flatten_kwargs:
            record_dict.update(
                record_dict.get("record", record_dict).pop("kwargs", {}) or {}
            )
        return record_dict

    @staticmethod
    def _add_datadog_fields(record_dict: typing.Dict[str, typing.Any]) -> None:
        if not ddtrace:
            raise ImportError("ddtrace is not installed")

        context = ddtrace.tracer.get_log_correlation_context()
        record_dict["dd.trace_id"] = context["trace_id"]
        record_dict["dd.span_id"] = context["span_id"]
        record_dict["dd.service"] = context["service"]
        record_dict["dd.version"] = context["version"]
        record_dict["dd.env"] = context["env"]

    @staticmethod
    def _add_google_cloud_fields(
        record: logging.LogRecord, record_dict: typing.Dict[str, typing.Any]
    ) -> None:
        map_google_severity = {
            "NOTSET": "DEFAULT",
            "WARN": "WARNING",
            "FATAL": "CRITICAL",
        }
        record_dict["severity"] = map_google_severity.get(
            record.levelname, record.levelname
        )
        record_dict["time"] = (
            dt.datetime.fromtimestamp(record.__dict__["created"], tz=dt.timezone.utc)
            .isoformat()
            .replace("+00:00", "Z")
        )
