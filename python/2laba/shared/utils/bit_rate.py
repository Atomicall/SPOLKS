import enum


class SPEED_PREFIXES(enum.Enum):
    Kb = 1024 / 8
    Mb = 1024**2 / 8
    Gb = 1024**3 / 8
    KB = 1024
    MB = 1024**2
    GB = 1024**3


def bit_rate(file_size: int, time_spent: float) -> str:
    if time_spent < 0:
        return str(-1)

    speed = file_size / time_spent
    result = ""
    if speed > SPEED_PREFIXES.Gb.value:
        result = str(round(speed / SPEED_PREFIXES.GB.value, 3)) + " " + \
            SPEED_PREFIXES.GB.name + "/sec OR " + \
            str(round(speed / SPEED_PREFIXES.Gb.value, 3)) + " " + \
            SPEED_PREFIXES.Gb.name + "/sec\n"
    elif speed > SPEED_PREFIXES.Mb.value:
        result = str(round(speed / SPEED_PREFIXES.MB.value, 3)) + " " + \
            SPEED_PREFIXES.MB.name + "/sec OR " + \
            str(round(speed / SPEED_PREFIXES.Mb.value, 3)) + " " + \
            SPEED_PREFIXES.Mb.name + "/sec\n"
    elif speed > SPEED_PREFIXES.Kb.value:
        result = str(round(speed / SPEED_PREFIXES.KB.value, 3)) + " " + \
            SPEED_PREFIXES.KB.name + "/sec OR " + \
            str(round(speed / SPEED_PREFIXES.Kb.value, 3)) + \
            " " + SPEED_PREFIXES.Kb.name + "/sec\n"
    return result
