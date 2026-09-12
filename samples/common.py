"""Shared data preparation for the three direction samples.

Each sample renders the same real fetch, so the comparison between them is a
comparison of design and not of data.
"""

from __future__ import annotations

import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "site" / "data.json"
OUT = ROOT / "samples"

CHAINS = ("woolworths", "coles")
CHAIN_LABEL = {"woolworths": "Woolworths", "coles": "Coles"}
CHAIN_SHORT = {"woolworths": "WOOLIES", "coles": "COLES"}


def load() -> dict:
    return json.loads(DATA.read_text(encoding="utf-8"))


def e(value) -> str:
    """Escape for HTML text and attribute contexts."""
    return html.escape(str(value if value is not None else ""), quote=True)


def money(value) -> str:
    return "" if value is None else f"{value:,.2f}"


def grouped(payload: dict) -> list[tuple[dict, list[dict]]]:
    """Rows in category order, skipping categories with nothing in them."""
    out = []
    for category in payload["categories"]:
        rows = [r for r in payload["rows"] if r["category"] == category["id"]]
        if rows:
            out.append((category, rows))
    return out


def headline(payload: dict) -> dict | None:
    """The single deepest discount this week, used as each sample's focal moment.

    Ranked by percentage off rather than dollars, so a cheap item halving beats
    a dear item losing a token amount.
    """
    best = None
    for row in payload["rows"]:
        for chain, offer in row["offers"].items():
            percent = offer.get("savingPercent")
            if not percent:
                continue
            if best is None or percent > best["percent"]:
                best = {
                    "percent": percent,
                    "row": row,
                    "chain": chain,
                    "offer": offer,
                }
    return best


def stats(payload: dict) -> dict:
    rows = payload["rows"]
    offers = [o for r in rows for o in r["offers"].values()]
    return {
        "rows": len(rows),
        "specials": sum(1 for o in offers if o.get("onSpecial")),
        "failures": sum(1 for o in offers if o.get("error")),
        "wins": {
            chain: sum(1 for r in rows if r["winner"] == chain) for chain in CHAINS
        },
    }


def cheaper(row: dict) -> str | None:
    """Which chain wins this row, or None when it is a tie or single-chain."""
    return row.get("winner")


def only_stockist(row: dict) -> str | None:
    """The one chain carrying this item, when the other does not stock it.

    A sole stockist holds the only rate there is, so a design that marks the
    cheaper chain must not mark it as the dearer one.
    """
    live = [
        chain
        for chain in CHAINS
        if (offer := row["offers"].get(chain)) and not offer.get("error")
    ]
    return live[0] if len(live) == 1 else None


def offer_state(row: dict, chain: str) -> str:
    """One of: ok, dearer, missing, failed."""
    offer = row["offers"].get(chain)
    if offer is None:
        return "missing"
    if offer.get("error"):
        return "failed"
    winner = row.get("winner")
    if winner and winner != chain:
        return "dearer"
    return "ok"


def write(name: str, markup: str) -> pathlib.Path:
    OUT.mkdir(exist_ok=True)
    path = OUT / name
    path.write_text(markup, encoding="utf-8")
    return path
