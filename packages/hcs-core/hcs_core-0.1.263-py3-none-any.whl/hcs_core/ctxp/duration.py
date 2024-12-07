# Utility for Java Duration interoperability

import re

PATTERN = (
    "([-+]?)P(?:([-+]?[0-9]+)D)?(T(?:([-+]?[0-9]+)H)?(?:([-+]?[0-9]+)M)?(?:([-+]?[0-9]+)(?:[.,]([0-9]{0,9}))?S)?)?"
)

# Examples

# PT0.555S
# PT9M15S
# PT9H15M
# PT555H
# PT13320H


def to_seconds(duration_string: str):
    duration_string = duration_string.upper()

    p = re.compile(PATTERN)
    matcher = p.fullmatch(duration_string)
    if matcher is None:
        raise Exception("Unsupported duration format: %s" % duration_string)

    if matcher.start(3) >= 0 and matcher.end(3) == matcher.start(3) + 1 and duration_string[matcher.start(3)] == "T":
        raise Exception("Unsupported duration format: %s" % duration_string)

    day_start = matcher.start(2)
    day_end = matcher.end(2)
    hour_start = matcher.start(4)
    hour_end = matcher.end(4)
    minute_start = matcher.start(5)
    minute_end = matcher.end(5)
    second_start = matcher.start(6)
    second_end = matcher.end(6)

    total_seconds = 0
    if day_start >= 0:
        days = int(duration_string[day_start:day_end])
        total_seconds += days * 24 * 3600
    if hour_start >= 0:
        hours = int(duration_string[hour_start:hour_end])
        total_seconds += hours * 3600
    if minute_start >= 0:
        minutes = int(duration_string[minute_start:minute_end])
        total_seconds += minutes * 60
    if second_start >= 0:
        seconds = int(duration_string[second_start:second_end])
        total_seconds += seconds

    return total_seconds


if __name__ == "__main__":
    assert to_seconds("PT5S") == 5
    assert to_seconds("PT5M") == 5 * 60
    assert to_seconds("PT5H") == 5 * 3600
    assert to_seconds("PT2M3S") == 2 * 60 + 3
    assert to_seconds("PT2H3M") == 2 * 3600 + 3 * 60
    assert to_seconds("PT2H3S") == 2 * 3600 + 3
    assert to_seconds("PT2H3M4S") == 2 * 3600 + 3 * 60 + 4
    assert to_seconds("P1D") == 1 * 24 * 60 * 60
    assert to_seconds("P1DT1M") == 1 * 24 * 60 * 60 + 1 * 60
    assert to_seconds("P1DT1S") == 1 * 24 * 60 * 60 + 1
    assert to_seconds("P1DT1H1S") == 1 * 24 * 60 * 60 + 1 * 3600 + 1
    print("SUCCESS")
