from datetime import datetime


def timestamp_or_empty_string(ts: datetime | str | None) -> str:
    if isinstance(ts, datetime):
        return ts.strftime("%Y-%m-%d %H:%M:%S")
    if ts is None:
        return ""
    return ts
