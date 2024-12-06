"""Meteocat Helpers."""

from datetime import datetime
from typing import Any
import re
import unicodedata
from zoneinfo import ZoneInfo

TZ_UTC = ZoneInfo("UTC")


def dict_nested_value(data: dict[str, Any] | None, keys: list[str] | None) -> Any:
    """Get value from dict with nested keys."""
    if keys is None or len(keys) == 0:
        return None
    for key in keys or {}:
        if data is not None:
            data = data.get(key)
    return data


def get_current_datetime(tz: ZoneInfo = TZ_UTC, replace: bool = True) -> datetime:
    """Return current datetime in UTC."""
    cur_dt = datetime.now(tz=tz)
    if replace:
        cur_dt = cur_dt.replace(minute=0, second=0, microsecond=0)
    return cur_dt


def parse_api_timestamp(timestamp: str, tz: ZoneInfo = TZ_UTC) -> datetime:
    """Parse API timestamp into datetime."""
    return datetime.fromisoformat(timestamp).replace(tzinfo=tz)


def slugify(value: str, allow_unicode: bool = False) -> str:
    """Convert string to a valid file name."""
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s]", "-", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")
