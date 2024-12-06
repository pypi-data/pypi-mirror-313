from __future__ import annotations

from datetime import datetime, tzinfo
from zoneinfo import ZoneInfo, available_timezones

from pyutilkit.data.timezones import UNAVAILABLE_TIMEZONES

UTC = ZoneInfo("UTC")


def get_timezones() -> set[str]:
    """Get all the available timezones.

    This takes into accounts timezones that might not be present in
    all systems.
    """
    return available_timezones() - UNAVAILABLE_TIMEZONES


def now(tz_info: ZoneInfo = UTC) -> datetime:
    return datetime.now(UTC).astimezone(tz_info)


def from_iso(date_string: str, tz_info: tzinfo = UTC) -> datetime:
    """Get datetime from an iso string.

    This to allow the Zulu timezone, which is a valid ISO timezone.
    """
    date_string = date_string.replace("Z", "+00:00")
    dt = datetime.fromisoformat(date_string)
    try:
        return add_timezone(dt, tz_info)
    except ValueError:
        return convert_timezone(dt, tz_info)


def from_timestamp(timestamp: float, tz_info: tzinfo = UTC) -> datetime:
    """Get a datetime tz-aware time object from a timestamp."""
    utc_dt = datetime.fromtimestamp(timestamp, tz=UTC)
    return convert_timezone(utc_dt, tz_info)


def add_timezone(dt: datetime, tz_info: tzinfo = UTC) -> datetime:
    """Add a timezone to a naive datetime.

    Raise an error in case of a tz-aware datetime
    """
    if dt.tzinfo is not None:
        msg = f"{dt} is already tz-aware"
        raise ValueError(msg)
    return dt.replace(tzinfo=tz_info)


def convert_timezone(dt: datetime, tz_info: tzinfo = UTC) -> datetime:
    """Change the timezone of a tz-aware datetime.

    Raise an error in case of a naive datetime
    """
    if dt.tzinfo is None:
        msg = f"{dt} is a naive datetime"
        raise ValueError(msg)
    return dt.astimezone(tz_info)
