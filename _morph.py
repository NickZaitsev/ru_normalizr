from __future__ import annotations

import functools

import pymorphy3


@functools.lru_cache(maxsize=1)
def get_morph() -> pymorphy3.MorphAnalyzer:
    return pymorphy3.MorphAnalyzer()
