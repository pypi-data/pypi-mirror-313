from typing import Dict
from collections import Counter

from ..common.logger import logger


class CounterCache:
    cache: Dict[str, int]

    def __init__(self):
        self.cache = {}

    def has(self, key: str) -> bool:
        return key in self.cache

    def add(self, key: str):
        self.cache[key] = 1

    def inc(self, key: str):
        self.cache[key] += 1

    def clean(self, keep: int):
        logger.debug(f"cleanup: {len(self.cache)=}")
        if len(self.cache) > keep:
            c = Counter(self.cache)
            self.cache = {url: used for url, used in c.most_common(keep)}
        logger.debug(f"cleanup result: {len(self.cache)=}")
