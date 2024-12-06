import re
from datetime import datetime, timedelta

import pytz


def iso8601_duration_to_float(iso_duration: str, unit: str = "S") -> float:
    if unit not in ("S", "M"):
        raise ValueError("Invalid unit. Must be 'S' or 'M'.")

    # Warning: ignores years, months and days, which are rarely used
    pattern = re.compile(
        r"P.*T(?:(\d+(?:\.\d+)?)H)?(?:(\d+(?:\.\d+)?)M)?(?:(\d+(?:\.\d+)?)S)?"
    )
    match = pattern.match(iso_duration)

    if not match:
        raise ValueError("Invalid ISO8601 duration format")

    hours, minutes, seconds = match.groups()
    total_seconds = (
        (float(hours or 0) * 3600) + (float(minutes or 0) * 60) + float(seconds or 0)
    )

    if unit == "S":
        return total_seconds
    else:
        return total_seconds / 60


def iso8601_duration_to_datetime(iso_duration: str) -> datetime:
    return datetime.now(pytz.utc) + timedelta(
        seconds=iso8601_duration_to_float(iso_duration)
    )


def to_relative_time(dt, with_milliseconds=False):
    now = datetime.now(pytz.utc)

    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt)

    time_difference = dt - now

    if abs(time_difference) > timedelta(days=1):
        return f'{"+" if time_difference >= timedelta(days=1) else "-"}24h+'

    sign = "+" if time_difference >= timedelta(0) else "-"
    time_difference = abs(time_difference)
    hours, remainder = divmod(time_difference.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = time_difference.microseconds // 1000

    if with_milliseconds:
        return f"{sign}{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
    else:
        return f"{sign}{hours:02d}:{minutes:02d}:{seconds:02d}"


def to_local_tz(dt_with_timezone):
    current_tz = datetime.now().astimezone().tzinfo
    dt_local = dt_with_timezone.astimezone(current_tz)
    return (
        dt_local.strftime("%Y-%m-%d %H:%M:%S.")
        + f"{dt_local.microsecond // 1000:03d} {dt_local.tzname()}"
    )


def relative_time(time: datetime):
    return "{} ({})".format(to_local_tz(time), to_relative_time(time))


def seconds_to_timecode(duration: float, with_milliseconds=False) -> str:
    hours, remainder = divmod(duration, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    seconds = int(seconds)

    if with_milliseconds:
        return f"{int(hours)}:{int(minutes):02d}:{seconds:02d}.{milliseconds:03d}"
    else:
        return f"{int(hours)}:{int(minutes):02d}:{seconds:02d}"
