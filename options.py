from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Optional


@dataclass(frozen=True, slots=True)
class NormalizeOptions:
    """Public configuration for ru_normalizr."""

    enable_caps_normalization: bool = True
    enable_first_word_decap: bool = True
    remove_links: bool = True
    remove_links_ignore_interval: tuple[int, int] = (1000, 2200)
    enable_year_normalization: bool = True
    enable_roman_normalization: bool = True
    enable_dates_time_normalization: bool = True
    enable_numeral_normalization: bool = True
    enable_abbreviation_expansion: bool = True
    enable_dictionary_normalization: bool = False
    enable_latinization: bool = True
    latinization_backend: Literal["ipa", "dictionary"] = "ipa"
    latin_dictionary_filename: str = "65_ЛАТИНИЦА@.dic"
    dictionary_include_files: tuple[str, ...] = ()
    dictionary_exclude_files: tuple[str, ...] = ()
    dictionaries_path: Optional[Path] = None
