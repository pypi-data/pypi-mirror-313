import datetime
import json
import traceback
import types
import typing


class Base(json.JSONEncoder):
    def default(self, obj: object) -> str | typing.List[str] | typing.Any:
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        if isinstance(obj, types.TracebackType):
            return traceback.format_tb(obj)

        try:
            return super().default(obj)
        except TypeError:
            return str(obj)

    def _recursive_convert_key(self, obj: object) -> dict[str, object] | object:
        if isinstance(obj, dict):
            return {
                self.default(key): self._recursive_convert_key(value)
                for key, value in obj.items()
            }
        return obj

    def encode(self, obj: object) -> str:
        try:
            return super().encode(obj)
        except TypeError:
            return super().encode(self._recursive_convert_key(obj))
