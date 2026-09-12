"""Produce the screenshots the finish review needs.

Some of the page's states do not exist in this week's real data, so a few
captures are rendered from fixtures derived from the real fetch. Each fixture
changes exactly one thing and says so in its name; nothing here invents a
price.

    python make_review_captures.py

Captures land in .impeccable/review/ and are not committed.
"""

from __future__ import annotations

import copy
import json
import pathlib
import shutil
import subprocess
import sys

import render

ROOT = pathlib.Path(__file__).resolve().parent
DATA = ROOT / "docs" / "data.json"
STAGE = ROOT / ".impeccable" / "review" / "_pages"
OUT = ROOT / ".impeccable" / "review"

CHROME = next(
    (
        p
        for p in (
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        )
        if pathlib.Path(p).exists()
    ),
    "",
)

PHONE = (390, 844)


def variant(html: str, *, dark: bool = False, no_motion: bool = False) -> str:
    """Force a theme or suppress motion, by rewriting the media queries only."""
    if dark:
        html = html.replace("@media (prefers-color-scheme:dark){", "@media all{")
    if no_motion:
        # The motion block only applies under no-preference, so pointing it at
        # reduce means an ordinary browser never runs it.
        html = html.replace(
            "@media (prefers-reduced-motion:no-preference){",
            "@media (prefers-reduced-motion:reduce){",
        )
    return html


def subset(payload: dict, titles: list[str], board: bool = False) -> dict:
    """The same page, narrowed to named rows, for a close capture of one state."""
    small = copy.deepcopy(payload)
    small["rows"] = [r for r in payload["rows"] if r["title"] in titles]
    keep = {r["category"] for r in small["rows"]}
    small["categories"] = [c for c in payload["categories"] if c["id"] in keep]
    if not board:
        small["stockUp"] = []
    return small


def dead_pin(payload: dict) -> dict:
    """A fixture: one pinned product no longer resolves.

    This state cannot be captured from live data, because nothing is currently
    broken. The error text is the real one the client raises on a 404.
    """
    fixture = copy.deepcopy(payload)
    for row in fixture["rows"]:
        if row["title"] == "Beef Mince Regular 500g":
            offer = row["offers"]["coles"]
            offer.update(
                {
                    "error": "HTTP 404",
                    "price": None,
                    "wasPrice": None,
                    "comparablePrice": None,
                    "onSpecial": False,
                    "notable": False,
                    "rarityPhrase": "",
                }
            )
            row["winner"] = None
    return fixture


def shoot(page: pathlib.Path, name: str, width: int, height: int,
          scale: float = 1.0) -> bool:
    """One headless capture. Virtual time lets transitions settle first."""
    target = OUT / name
    command = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--no-first-run",
        "--no-default-browser-check",
        f"--force-device-scale-factor={scale}",
        "--virtual-time-budget=6000",
        f"--window-size={width},{height}",
        f"--screenshot={target}",
        page.as_uri(),
    ]
    subprocess.run(command, capture_output=True, timeout=180, check=False)
    ok = target.exists() and target.stat().st_size > 2000
    size = target.stat().st_size // 1024 if target.exists() else 0
    print(f"  {'ok ' if ok else 'FAILED'} {name:<30} {width}x{height} @{scale}x  {size}KB")
    return ok


def page_height(html: str, rows: int) -> int:
    """Enough window height to capture the whole page in one shot."""
    return 900 + rows * 260


def main() -> int:
    if not CHROME:
        print("No Chrome or Edge found for headless capture.")
        return 1
    if not DATA.exists():
        print("No fetch to render. Run fetch_prices.py first.")
        return 1

    payload = json.loads(DATA.read_text(encoding="utf-8"))
    if OUT.exists():
        shutil.rmtree(OUT)
    STAGE.mkdir(parents=True)

    full = render.page(payload)
    rows = len(payload["rows"])

    pages: dict[str, str] = {
        "full": full,
        "special": render.page(
            subset(payload, [
                "Coca-Cola Zero Sugar Bottle 1.25L",
                "Arnott's Cracker Chips Balsamic Vinegar & Sea Salt 150g",
                "Harvest Snaps Pea Crisps Salt & Vinegar 120g",
            ])
        ),
        "notstocked": render.page(
            subset(payload, [
                "Chicken Bulk Schnitzels 1.2kg",
                "Chicken Bulk Schnitzels 1.5kg",
            ])
        ),
        "deadpin": render.page(
            subset(dead_pin(payload), ["Beef Mince Regular 500g",
                                       "Beef Mince Extra Lean 500g"])
        ),
        "stamp": render.page(
            subset(payload, ["Coca-Cola Zero Sugar Bottle 1.25L"])
        ),
    }
    for name, html in pages.items():
        (STAGE / f"{name}.html").write_text(html, encoding="utf-8", newline="\n")

    tall = page_height(full, rows)
    jobs = [
        # page, out, width, height, scale, dark, reduce motion, full page
        ("full",       "mobile.png",                390,  844,  1, 0, 0, 1),
        ("full",       "desktop.png",               1440, 900,  1, 0, 0, 1),
        ("full",       "mobile-first-viewport.png", 390,  844,  1, 0, 0, 0),
        ("full",       "mobile-dark.png",           390,  844,  1, 1, 0, 1),
        ("full",       "mobile-no-motion.png",      390,  844,  1, 0, 1, 1),
        ("special",    "state-special.png",         390,  844,  2, 0, 0, 1),
        ("notstocked", "state-not-stocked.png",     390,  844,  2, 0, 0, 1),
        ("deadpin",    "state-dead-pin.png",        390,  844,  2, 0, 0, 1),
        ("stamp",      "state-rarity-stamp.png",    390,  844,  2, 0, 0, 1),
    ]
    spec = [
        {
            "page": str(STAGE / f"{src}.html"),
            "out": str(OUT / name),
            "width": w, "height": h, "scale": sc,
            "dark": bool(dark), "reduceMotion": bool(rm), "fullPage": bool(fp),
        }
        for src, name, w, h, sc, dark, rm, fp in jobs
    ]
    plan = STAGE / "jobs.json"
    plan.write_text(
        json.dumps(spec, indent=1), encoding="utf-8", newline="\n"
    )

    print(f"Capturing with {pathlib.Path(CHROME).name} over the DevTools protocol")
    result = subprocess.run(
        ["node", str(ROOT / "capture.mjs"), str(plan)],
        capture_output=True, text=True, timeout=600, check=False,
    )
    print(result.stdout.rstrip() or result.stderr.rstrip())
    done = sum(1 for j in spec if pathlib.Path(j["out"]).exists())

    notes = OUT / "CAPTURES.md"
    notes.write_text(
        "# Review captures\n\n"
        "Taken with headless Chrome against the generated page, with a virtual\n"
        "time budget so every transition out of `@starting-style` has settled.\n"
        "Nothing here is a mid-transition frame.\n\n"
        "| Capture | How it was produced |\n"
        "|---|---|\n"
        "| `mobile.png` | The real page, full length, phone width. |\n"
        "| `desktop.png` | The real page, full length, 1440 wide. |\n"
        "| `mobile-first-viewport.png` | The real page clipped to one phone screen, no scroll. |\n"
        "| `mobile-dark.png` | The real page with the dark media query forced on. |\n"
        "| `mobile-no-motion.png` | The real page with the motion block pointed at `reduce`, so no transition runs. |\n"
        "| `state-special.png` | Real rows carrying a half-price, a multibuy and a save-amount flash, at 2x. |\n"
        "| `state-not-stocked.png` | The two real bulk schnitzel rows, one stocked per chain, at 2x. |\n"
        "| `state-dead-pin.png` | **Fixture.** One real row's Coles offer given the client's real 404 error, because nothing is currently broken. No price invented. |\n"
        "| `state-rarity-stamp.png` | One real row carrying the rarity stamp, at 2x. |\n\n"
        "State captures are rendered from the same generator with the payload\n"
        "narrowed to the named rows, so what is shown is the shipping markup.\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"\n{done} of {len(jobs)} captures written to {OUT}")
    return 0 if done == len(jobs) else 1


if __name__ == "__main__":
    raise SystemExit(main())
