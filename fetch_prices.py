"""Fetch current Woolworths and Coles prices for the pinned shopping list.

Runs on this machine, not in the cloud: Woolworths refuses requests from data
centre addresses. Writes docs/data.json and regenerates docs/index.html.

    python fetch_prices.py            # fetch and rebuild the page
    python fetch_prices.py --render   # rebuild the page from the last fetch

Prices are standard shelf prices. Neither retailer exposes Everyday Rewards or
Flybuys member pricing without signing in, so member specials are not included.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import sys
import time
import zoneinfo

import history
import render
import retailers
import sizes

ROOT = pathlib.Path(__file__).parent
CONFIG = ROOT / "products.json"
STATE = ROOT / "state.json"
# GitHub Pages serves a repository's /docs folder directly, so the
# generated page lives there rather than in a build directory.
SITE = ROOT / "docs"
DATA = SITE / "data.json"
MELBOURNE = zoneinfo.ZoneInfo("Australia/Melbourne")

CHAINS = ("woolworths", "coles")


# Specials reset on Wednesday, so "current" means fetched at or after the most
# recent Wednesday 7am.
RESET_WEEKDAY = 2  # Monday is 0
RESET_HOUR = 7


def last_reset(now: dt.datetime | None = None) -> dt.datetime:
    """The most recent Wednesday 7am Melbourne time, at or before now."""
    now = now or dt.datetime.now(MELBOURNE)
    back = (now.weekday() - RESET_WEEKDAY) % 7
    candidate = (now - dt.timedelta(days=back)).replace(
        hour=RESET_HOUR, minute=0, second=0, microsecond=0
    )
    if candidate > now:
        candidate -= dt.timedelta(days=7)
    return candidate


def is_current(now: dt.datetime | None = None) -> bool:
    """Has the page already been built since the last specials reset?

    The scheduled task runs daily and leans on this rather than on Windows
    remembering a missed trigger, which it does not do reliably: a run missed
    because the machine was asleep at 7am was silently dropped and the next run
    moved a week out. Deciding here means any day the machine is awake after a
    reset brings the page up to date, and every other run costs nothing.
    """
    if not DATA.exists():
        return False
    try:
        payload = json.loads(DATA.read_text(encoding="utf-8"))
        built = dt.datetime.fromisoformat(payload["generatedAt"])
    except (OSError, json.JSONDecodeError, KeyError, ValueError):
        return False
    return built >= last_reset(now)


def load_config() -> dict:
    with CONFIG.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_state() -> dict:
    """Small bits of memory between runs, chiefly the Coles build id."""
    if not STATE.exists():
        return {}
    try:
        return json.loads(STATE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def save_state(state: dict) -> None:
    STATE.write_text(
        json.dumps(state, indent=1), encoding="utf-8", newline="\n"
    )


def build_offer(
    client, item: dict, chain: str, past: dict[str, dict] | None = None
) -> dict | None:
    """Fetch one chain's offer for one row, or None if that chain is skipped."""
    pinned = item.get(chain)
    if not pinned:
        return None

    product_id = pinned if isinstance(pinned, str) else pinned.get("id")
    slug = pinned.get("slug", "") if isinstance(pinned, dict) else ""

    if chain == "coles":
        offer = client.fetch(product_id, slug=slug)
    else:
        offer = client.fetch(product_id)

    record = offer.as_dict()
    # The retailer's own pack size leads; the row title fills whatever it omits.
    size = sizes.merge(sizes.parse(offer.size), sizes.parse(item["title"]))
    unit, label = sizes.unit_price(offer.price, size, item["unitBasis"])
    record["comparablePrice"] = unit
    record["comparableLabel"] = label

    # How unusual is this price for this product? The retailer feeds cannot
    # say, so it comes from the historical dataset instead.
    measure = history.rarity((past or {}).get(str(product_id)), offer.price)
    record["rarity"] = measure
    record["notable"] = history.is_notable(measure)
    record["rarityPhrase"] = history.phrase(measure) if record["notable"] else ""
    record["notability"] = history.notability(measure)
    return record


def decide_winner(row: dict) -> str | None:
    """Which chain wins on the row's comparable basis. None if not comparable."""
    scored = {
        chain: offer["comparablePrice"]
        for chain in CHAINS
        if (offer := row["offers"].get(chain)) and offer["comparablePrice"] is not None
    }
    if len(scored) < 2:
        return None
    best = min(scored.values())
    winners = [chain for chain, value in scored.items() if value == best]
    return winners[0] if len(winners) == 1 else None


def load_history() -> tuple[dict[str, dict[str, dict]], str]:
    """Historical prices per chain. A failure here costs rarity, not the run."""
    past: dict[str, dict[str, dict]] = {}
    problems: list[str] = []
    for chain in CHAINS:
        try:
            past[chain] = history.load(chain)
        except history.HistoryUnavailable as exc:
            past[chain] = {}
            problems.append(f"{chain}: {exc}")
    return past, "; ".join(problems)


def fetch_all(config: dict, build_id_hint: str = "") -> dict:
    clients = {
        "woolworths": retailers.Woolworths(),
        "coles": retailers.Coles(build_id_hint=build_id_hint),
    }
    print("Reading price history...", flush=True)
    past, history_problem = load_history()
    if history_problem:
        print(f"  history unavailable ({history_problem}); "
              f"prices will show without rarity", flush=True)
    rows: list[dict] = []
    failures: list[str] = []

    total = len(config["items"])
    for index, item in enumerate(config["items"], start=1):
        row = {
            "title": item["title"],
            "category": item["category"],
            "unitBasis": item["unitBasis"],
            "note": item.get("note", ""),
            "offers": {},
        }
        for chain in CHAINS:
            offer = build_offer(clients[chain], item, chain, past.get(chain))
            if offer is None:
                continue
            row["offers"][chain] = offer
        row["winner"] = decide_winner(row)
        row["_item"] = item
        rows.append(row)
        print(f"  [{index:>2}/{total}] {item['title'][:52]:<52} "
              f"{_progress_note(row)}", flush=True)

    # A single bot challenge should not leave a red cell for the week. Anything
    # that failed for a reason other than "no such product" gets one more go
    # after a pause, which clears nearly all of them.
    retried = retry_failures(clients, rows, past)
    failures = [
        f"{row['title']} at {chain}: {offer['error']}"
        for row in rows
        for chain, offer in row["offers"].items()
        if offer["error"]
    ]
    if retried:
        print(f"  retried {retried} that failed first time; "
              f"{len(failures)} still failing", flush=True)
    for row in rows:
        row.pop("_item", None)

    now = dt.datetime.now(MELBOURNE)
    return {
        "colesBuildId": clients["coles"]._build_id or "",
        "historyProblem": history_problem,
        "stockUp": stock_up(rows),
        "generatedAt": now.isoformat(timespec="minutes"),
        "generatedLabel": now.strftime("%-d %B %Y, %-I:%M%p").replace("AM", "am").replace("PM", "pm")
        if sys.platform != "win32"
        else now.strftime("%d %B %Y, %I:%M%p").lstrip("0").replace("AM", "am").replace("PM", "pm"),
        "categories": config["categories"],
        "rows": rows,
        "failures": failures,
    }


def retry_failures(clients: dict, rows: list[dict], past: dict) -> int:
    """Re-attempt offers that failed transiently. Returns how many were retried.

    A 404 means the pinned product is genuinely gone and retrying cannot help,
    so those are left alone.
    """
    pending = [
        (row, chain)
        for row in rows
        for chain, offer in row["offers"].items()
        if offer["error"] and "404" not in offer["error"]
    ]
    if not pending:
        return 0
    print(f"  {len(pending)} failed on the first pass; waiting a minute "
          f"before retrying with fresh connections", flush=True)
    time.sleep(60)
    # New clients, and therefore new cookie jars: a challenged jar stays
    # challenged, so reusing these clients would repeat the same failure.
    clients = {
        "woolworths": retailers.Woolworths(),
        "coles": retailers.Coles(
            build_id_hint=clients["coles"]._build_id or ""
        ),
    }
    for row, chain in pending:
        offer = build_offer(
            clients[chain], row["_item"], chain, past.get(chain)
        )
        if offer and not offer["error"]:
            row["offers"][chain] = offer
            row["winner"] = decide_winner(row)
    return len(pending)


def stock_up(rows: list[dict], limit: int = 3) -> list[dict]:
    """This week's specials worth acting on, rarest-and-deepest first.

    Ranked by how unusual the price is rather than by headline percentage, so a
    product that discounts every fortnight does not crowd out one that seldom
    does.
    """
    candidates = []
    for row in rows:
        for chain, offer in row["offers"].items():
            if offer.get("error") or not offer.get("onSpecial"):
                continue
            if not offer.get("notable"):
                continue
            candidates.append(
                {
                    "title": row["title"],
                    "category": row["category"],
                    "chain": chain,
                    "offer": offer,
                    "notability": offer["notability"],
                    "phrase": offer["rarityPhrase"],
                }
            )
    candidates.sort(key=lambda c: c["notability"], reverse=True)
    return candidates[:limit]


def _progress_note(row: dict) -> str:
    parts = []
    for chain in CHAINS:
        offer = row["offers"].get(chain)
        if offer is None:
            parts.append(f"{chain[:4]}: -")
        elif offer["error"]:
            parts.append(f"{chain[:4]}: FAIL")
        else:
            special = " *" if offer["onSpecial"] else ""
            parts.append(f"{chain[:4]}: ${offer['price']}{special}")
    return "  ".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--render", action="store_true",
                        help="rebuild the page from the last saved fetch")
    parser.add_argument("--coles-build-id", default="", metavar="ID",
                        help="override the cached Coles build id (see README)")
    parser.add_argument("--if-stale", action="store_true",
                        help="do nothing if the page is newer than the last "
                             "Wednesday reset; used by the scheduled task")
    args = parser.parse_args()

    if args.if_stale and not args.render and is_current():
        built = json.loads(DATA.read_text(encoding="utf-8"))["generatedLabel"]
        print(f"Already current: read {built}. Nothing to do.")
        return 0

    SITE.mkdir(exist_ok=True)

    if args.render:
        if not DATA.exists():
            print("No previous fetch found. Run without --render first.")
            return 1
        payload = json.loads(DATA.read_text(encoding="utf-8"))
    else:
        config = load_config()
        state = load_state()
        hint = args.coles_build_id or state.get("colesBuildId", "")
        print(f"Fetching {len(config['items'])} items from both chains...")
        payload = fetch_all(config, build_id_hint=hint)
        DATA.write_text(
            json.dumps(payload, indent=1), encoding="utf-8", newline="\n"
        )
        if payload.get("colesBuildId"):
            state["colesBuildId"] = payload["colesBuildId"]
            state["lastRun"] = payload["generatedAt"]
            save_state(state)

    html = render.page(payload)
    (SITE / "index.html").write_text(html, encoding="utf-8", newline="\n")

    specials = sum(
        1 for row in payload["rows"]
        for offer in row["offers"].values() if offer.get("onSpecial")
    )
    print(f"\n{len(payload['rows'])} rows, {specials} on special, "
          f"{len(payload['failures'])} failed.")
    for failure in payload["failures"]:
        print(f"  ! {failure}")
    print(f"\nWrote {SITE / 'index.html'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
