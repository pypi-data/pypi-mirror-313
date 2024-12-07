from datetime import timedelta, datetime, timezone
import re


def display(d: timedelta, use_double_digits: bool = False) -> str:
    years = int(d.days / 365)
    remaining = d.days % 365
    weeks = int(remaining / 7)
    days = remaining % 7

    hours = int(d.seconds / 3600)
    remaining = d.seconds % 3600
    minutes = int(remaining / 60)
    seconds = remaining % 60

    if use_double_digits:
        if years:
            return f"{years:02}y{weeks:02}w"
        if weeks:
            return f"{weeks:02}w{days:02}d"
        if days:
            return f"{days:02}d{hours:02}h"
        if hours:
            return f"{hours:02}h{minutes:02}m"
        if minutes:
            return f"{minutes:02}m{seconds:02}s"
        return f"{seconds}s"
    else:
        if years:
            return f"{years}y{weeks}w"
        if weeks:
            return f"{weeks}w{days}d"
        if days:
            return f"{days}d{hours}h"
        if hours:
            return f"{hours}h{minutes}m"
        if minutes:
            return f"{minutes}m{seconds}s"
        return f"{seconds}s"


def human_delta_to_iso(delta_str: str):
    now = datetime.now(timezone.utc)
    if delta_str == "now":
        return now.isoformat(timespec="milliseconds").replace("+00:00", "Z")

    if not delta_str.startswith("-") and not delta_str.startswith("+"):
        return delta_str

    # Initialize a timedelta object
    time_delta = timedelta()

    # Determine if the input represents a subtraction (-) or addition (+)
    if delta_str.startswith("-"):
        sign = -1
    elif delta_str.startswith("+"):
        sign = 1
    else:
        raise ValueError("Time delta must start with '+' or '-'")

    # Regular expressions for weeks, days, hours, minutes, and seconds
    patterns = {
        "w": r"([+-]\d+)w",  # Weeks
        "d": r"([+-]\d+)d",  # Days
        "h": r"([+-]\d+)h",  # Hours
        "m": r"([+-]\d+)m",  # Minutes
        "s": r"([+-]\d+)s",  # Seconds
    }

    # Extract and apply each time unit
    for unit, pattern in patterns.items():
        match = re.search(pattern, delta_str)
        if match:
            value = int(match.group(1))
            if unit == "w":
                time_delta += timedelta(weeks=value)
            elif unit == "d":
                time_delta += timedelta(days=value)
            elif unit == "h":
                time_delta += timedelta(hours=value)
            elif unit == "m":
                time_delta += timedelta(minutes=value)
            elif unit == "s":
                time_delta += timedelta(seconds=value)
    result_time = now + time_delta

    return result_time.strftime("%Y-%m-%dT%H:%M:%S.") + f"{result_time.microsecond // 1000:03d}Z"


def _test():
    # Example usage
    print(human_delta_to_iso("-1w"))  # One week ago
    print(human_delta_to_iso("-1h35m"))  # 1 hour and 35 minutes ago
    print(human_delta_to_iso("+2h10m5s"))  # 2 hours, 10 minutes, and 5 seconds from now
    print(human_delta_to_iso("+3d1w"))
