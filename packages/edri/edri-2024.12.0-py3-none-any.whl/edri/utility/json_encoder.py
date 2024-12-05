from enum import Enum
from json import JSONEncoder
from pathlib import Path
from typing import Any


class CustomJSONEncoder(JSONEncoder):
    """
    A custom JSON encoder for converting various data types to JSON-compatible
    formats, including support for Enums, datetime objects, Paths, bytes, and
    more.

    Inherits from JSONEncoder to override the default() method for custom serialization.
    """

    def default(self, data) -> Any:
        if hasattr(data, "to_json"):
            return data.to_json()
        elif hasattr(data, "isoformat"):
            return data.isoformat()
        elif isinstance(data, Path):
            return data.as_posix()
        elif isinstance(data, bytes) or isinstance(data, bytearray):
            return data.hex()
        elif isinstance(data, Enum):
            return data.value
        else:
            return super().default(data)
