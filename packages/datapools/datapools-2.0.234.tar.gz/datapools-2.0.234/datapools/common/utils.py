import re
from .types import InvalidUsageException


def parse_size(size: str | int):
    if isinstance(size, int):
        return size
    m = re.match(r"^(\d+)(M|G|Mi|Gi|T|Ti|K|Ki)?$", size)
    if m:
        g = m.groups()

        base = int(g[0])
        scale = g[1]
        if scale == "M":
            return base * 10**6
        if scale == "G":
            return base * 10**9
        if scale == "K":
            return base * 1000
        if scale == "T":
            return base * 10**12

        if scale == "Mi":
            return base * 2**20
        if scale == "Gi":
            return base * 2**30
        if scale == "Ki":
            return base * 2**10
        if scale == "Ti":
            return base * 2**40
        if scale is None:
            return base
    raise InvalidUsageException(f"Unparsable size {size}")
