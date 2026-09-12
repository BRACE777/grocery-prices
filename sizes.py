"""Turn a retailer's pack-size string into comparable quantities.

The two chains describe the same pack differently ("1.25L" against "1.25 L",
"24 Pack" against "24x375mL"), and each row of the app compares on one chosen
basis. This module reduces any size string to grams, millilitres and a unit
count so the comparison is apples to apples.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_NUM = r"(\d+(?:\.\d+)?)"

# Order matters: the multipack pattern must be tried before the plain one so
# "24x375mL" is read as 24 units of 375mL rather than a 24mL pack.
_MULTIPACK = re.compile(rf"{_NUM}\s*[x×]\s*{_NUM}\s*(g|kg|ml|l|mls?)\b", re.I)
_COUNT = re.compile(rf"{_NUM}\s*(?:pack|pk|pce|piece|each|ea)\b", re.I)
_WEIGHT = re.compile(rf"{_NUM}\s*(kg|g)\b", re.I)
_VOLUME = re.compile(rf"{_NUM}\s*(ml|l)\b", re.I)

_TO_GRAMS = {"g": 1.0, "kg": 1000.0}
_TO_ML = {"ml": 1.0, "mls": 1.0, "l": 1000.0}


@dataclass
class Size:
    grams: float | None = None
    millilitres: float | None = None
    count: int | None = None

    @property
    def empty(self) -> bool:
        return self.grams is None and self.millilitres is None and self.count is None


def parse(text: str | None) -> Size:
    """Read whatever quantities a size string contains. Never raises."""
    size = Size()
    if not text:
        return size
    s = str(text).strip()

    multi = _MULTIPACK.search(s)
    if multi:
        count = float(multi.group(1))
        each = float(multi.group(2))
        unit = multi.group(3).lower()
        size.count = int(count)
        if unit in _TO_GRAMS:
            size.grams = count * each * _TO_GRAMS[unit]
        elif unit in _TO_ML:
            size.millilitres = count * each * _TO_ML[unit]
        return size

    count = _COUNT.search(s)
    if count:
        size.count = int(float(count.group(1)))

    weight = _WEIGHT.search(s)
    if weight:
        size.grams = float(weight.group(1)) * _TO_GRAMS[weight.group(2).lower()]

    volume = _VOLUME.search(s)
    if volume:
        size.millilitres = float(volume.group(1)) * _TO_ML[volume.group(2).lower()]

    return size


# What each basis needs, how to divide, and how to label the result.
BASIS = {
    "100g":  ("grams",       100.0,  "/100g"),
    "100ml": ("millilitres", 100.0,  "/100mL"),
    "kg":    ("grams",       1000.0, "/kg"),
    "can":   ("count",       1.0,    " a can"),
    "pack":  ("count",       1.0,    " a pack"),
    "piece": ("count",       1.0,    " each"),
}


def merge(primary: Size, backup: Size) -> Size:
    """Fill gaps in one size from another.

    The retailers describe the same pack differently: Woolworths calls the Jin
    Ramen a "5 pack" while Coles calls it "600g". Taking the weight from one and
    the count from the other is what makes the two comparable on either basis.
    """
    return Size(
        grams=primary.grams if primary.grams is not None else backup.grams,
        millilitres=(
            primary.millilitres
            if primary.millilitres is not None
            else backup.millilitres
        ),
        count=primary.count if primary.count is not None else backup.count,
    )


def unit_price(price: float | None, size: Size, basis: str) -> tuple[float | None, str]:
    """Price expressed on the row's chosen basis, plus its label."""
    spec = BASIS.get(basis)
    if price is None or spec is None:
        return None, ""
    attribute, divisor, label = spec
    quantity = getattr(size, attribute, None)
    if not quantity:
        return None, label
    return round(price / (quantity / divisor), 2), label
