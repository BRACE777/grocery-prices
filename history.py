"""How unusual is today's price?

The retailers' own feeds say whether something is on special. They do not say
whether the special is any good. A product that bounces between $12 and $10
every fortnight is on special most weeks; the same product at $6 is worth
acting on. Telling those apart needs history, which the retailer feeds do not
carry but the hotprices.org community dataset does.

The dataset records price *changes*, not daily snapshots, so a price stands
until the next recorded change. Everything here reconstructs the step function
first and then measures against it.
"""

from __future__ import annotations

import datetime as dt
import gzip
import json
import pathlib
import shutil
import subprocess
import time

ROOT = pathlib.Path(__file__).resolve().parent
CACHE = ROOT / "cache"

SOURCE = "https://hotprices.org/data/latest-canonical.{chain}.compressed.json.gz"
DATASET_CHAIN = {"woolworths": "woolies", "coles": "coles"}

WINDOW_DAYS = 90
CACHE_MAX_AGE = 6 * 60 * 60  # seconds; the dataset refreshes about daily

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
)


class HistoryUnavailable(RuntimeError):
    """The dataset could not be read. Rarity is then simply not shown."""


def _download(chain: str, path: pathlib.Path) -> None:
    curl = shutil.which("curl")
    if not curl:
        raise HistoryUnavailable("curl not found")
    path.parent.mkdir(exist_ok=True)
    temporary = path.with_suffix(".part")
    result = subprocess.run(
        [
            curl, "--silent", "--show-error", "--location", "--fail",
            "--max-time", "120",
            "--user-agent", UA,
            "--header", "Referer: https://hotprices.org/",
            "--output", str(temporary),
            SOURCE.format(chain=chain),
        ],
        capture_output=True,
        check=False,
    )
    if result.returncode != 0 or not temporary.exists():
        detail = (result.stderr or b"").decode("utf-8", "replace").strip()
        raise HistoryUnavailable(f"download failed: {detail or result.returncode}")
    temporary.replace(path)


def load(chain: str, refresh: bool = True) -> dict[str, dict]:
    """Price history for one chain, keyed by product id. Cached on disk."""
    dataset = DATASET_CHAIN[chain]
    path = CACHE / f"{dataset}.json.gz"
    stale = not path.exists() or (time.time() - path.stat().st_mtime) > CACHE_MAX_AGE
    if stale and refresh:
        try:
            _download(dataset, path)
        except HistoryUnavailable:
            if not path.exists():
                raise
            # A stale cache beats no history at all.
    if not path.exists():
        raise HistoryUnavailable("no cached dataset")
    try:
        with gzip.open(path) as handle:
            records = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise HistoryUnavailable(f"cache unreadable: {exc}") from exc
    return {str(record["id"]): record for record in records}


def _series(record: dict) -> list[tuple[dt.date, float]]:
    """Recorded price changes, oldest first."""
    out: list[tuple[dt.date, float]] = []
    for point in record.get("priceHistory") or []:
        try:
            when = dt.date.fromisoformat(point["date"])
            price = float(point["price"])
        except (KeyError, TypeError, ValueError):
            continue
        if price > 0:
            out.append((when, price))
    out.sort()
    return out


def rarity(
    record: dict | None,
    current_price: float | None,
    today: dt.date | None = None,
    window_days: int = WINDOW_DAYS,
) -> dict | None:
    """Measure today's price against the product's own recent history.

    Returns None when there is not enough history to say anything honest.

    days_at_or_below  how many days of the window sat at or under today's price
    share             that as a fraction of the window, so 0.02 means rare
    base              the standing shelf price, taken as the window's highest
    depth             how far under the standing price today sits, 0 to 1
    is_low            today equals the cheapest the window ever saw
    spells            how many separate times it reached this price or lower
    """
    if record is None or current_price is None:
        return None
    series = _series(record)
    if len(series) < 2:
        return None

    today = today or dt.date.today()
    start = today - dt.timedelta(days=window_days)

    # The price in force when the window opened, plus every change inside it.
    prior = [p for d, p in series if d <= start]
    inside = [(d, p) for d, p in series if start < d <= today]
    if not prior and not inside:
        return None
    steps: list[tuple[dt.date, float]] = []
    if prior:
        steps.append((start, prior[-1]))
    steps.extend(inside)
    if not steps:
        return None
    if steps[0][0] > start:
        # No price known at the window's start; begin where the record does.
        start = steps[0][0]

    days_at_or_below = 0
    prices: list[float] = []
    spells = 0
    previously_low = False
    for index, (when, price) in enumerate(steps):
        until = steps[index + 1][0] if index + 1 < len(steps) else today
        span = max((until - when).days, 0)
        if span == 0 and index + 1 < len(steps):
            continue
        prices.append(price)
        low_now = price <= current_price + 1e-9
        if low_now:
            days_at_or_below += span
            if not previously_low:
                spells += 1
        previously_low = low_now

    total_days = max((today - start).days, 1)
    if not prices:
        return None
    base = max(prices)
    if base <= 0:
        return None

    return {
        "days_at_or_below": days_at_or_below,
        "window_days": total_days,
        "share": round(min(days_at_or_below / total_days, 1.0), 4),
        "base": round(base, 2),
        "depth": round(max(base - current_price, 0) / base, 4),
        "is_low": current_price <= min(prices) + 1e-9,
        "spells": spells,
    }


def notability(measure: dict | None) -> float:
    """How much this week's price deserves the headline.

    Depth alone promotes whatever is biggest and cheapest. Rarity alone
    promotes anything with a thin record. Multiplying them promotes the deep
    cut on a product that is seldom this cheap, which is the thing worth
    knowing about.
    """
    if not measure or measure["depth"] <= 0:
        return 0.0
    scarcity = 1.0 - measure["share"]
    score = measure["depth"] * (scarcity ** 2)
    if measure["is_low"]:
        score *= 1.35
    return round(score, 6)


def is_notable(measure: dict | None) -> bool:
    """Does this price deserve a mark on the ticket?

    A deep discount that happens most weeks is not news, so depth alone does
    not qualify. Either this is the cheapest the window saw, or the price has
    been this low for only a small slice of it.
    """
    if not measure or measure["depth"] <= 0:
        return False
    return bool(measure["is_low"]) or measure["share"] <= 0.25


def phrase(measure: dict | None) -> str:
    """A short, honest description of how unusual this price is."""
    if not measure or measure["depth"] <= 0:
        return ""
    months = max(round(measure["window_days"] / 30), 1)
    span = "a month" if months == 1 else f"{months} months"
    if measure["is_low"]:
        return f"cheapest in {span}"
    days = measure["days_at_or_below"]
    if days == 0:
        return f"not been this cheap in {span}"
    day_word = "day" if days == 1 else "days"
    if measure["share"] <= 0.08:
        return f"only {days} {day_word} this cheap in {span}"
    if measure["share"] <= 0.25:
        return f"{days} {day_word} this cheap in {span}"
    return "about as cheap as it usually gets"
