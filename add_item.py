"""Add a tracked product by pasting its web address.

    python add_item.py <woolworths url> <coles url>   both chains, one row
    python add_item.py <url>                          one chain only
    python add_item.py <url> --into "Beef Mince Regular 500g"
                                                      add a chain to a row

Copy the address from either shop, on the phone or the desktop, and paste it
in. The product is fetched once to confirm it exists and to read its real name
and pack size, so a row is never pinned to an identifier that does not resolve.

Category and unit basis are asked for when they are not obvious and not given
on the command line.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

import retailers
import sizes

ROOT = pathlib.Path(__file__).resolve().parent
CONFIG = ROOT / "products.json"
STATE = ROOT / "state.json"

# Woolworths: /shop/productdetails/623034/some-slug
# Coles:      /product/some-slug-2993706
PATTERNS = (
    ("woolworths", re.compile(r"woolworths\.com\.au/shop/productdetails/(\d+)", re.I)),
    ("woolworths", re.compile(r"woolworths\.com\.au/.*?[?&]stockcode=(\d+)", re.I)),
    ("coles", re.compile(r"coles\.com\.au/product/(?:.*-)?(\d+)", re.I)),
)

BASES = ("100g", "100ml", "kg", "can", "pack", "piece")


def identify(url: str) -> tuple[str, str]:
    """Which chain, and which product id, this address refers to."""
    for chain, pattern in PATTERNS:
        found = pattern.search(url)
        if found:
            return chain, found.group(1)
    raise SystemExit(
        f"Could not read a product id from:\n  {url}\n\n"
        "Expected a Woolworths address like\n"
        "  https://www.woolworths.com.au/shop/productdetails/623034/...\n"
        "or a Coles address like\n"
        "  https://www.coles.com.au/product/...-2993706"
    )


def suggest_basis(size: str, title: str) -> str:
    """A sensible unit basis from the pack size, for the user to confirm."""
    measured = sizes.merge(sizes.parse(size), sizes.parse(title))
    if measured.count and measured.count > 1:
        return "can" if re.search(r"\bcans?\b", f"{size} {title}", re.I) else "piece"
    if measured.grams and measured.grams >= 900:
        return "kg"
    if measured.millilitres:
        return "100ml"
    return "100g"


def ask(question: str, options: tuple[str, ...], default: str) -> str:
    """Prompt only when there is somebody to answer."""
    if not sys.stdin.isatty():
        return default
    listing = ", ".join(options)
    while True:
        reply = input(f"{question}\n  [{listing}]\n  default {default}: ").strip()
        if not reply:
            return default
        if reply in options:
            return reply
        print(f"  '{reply}' is not one of them.")


def fetch(chain: str, product_id: str, build_id: str = "") -> retailers.Offer:
    client = (
        retailers.Coles(build_id_hint=build_id)
        if chain == "coles"
        else retailers.Woolworths()
    )
    offer = client.fetch(product_id)
    if not offer.ok:
        raise SystemExit(
            f"{chain} would not return that product ({offer.error or 'no price'}).\n"
            "Check the address opens in a browser, then try again."
        )
    return offer


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("urls", nargs="+", help="one product address per chain")
    parser.add_argument("--title", default="", help="row title on the page")
    parser.add_argument("--category", default="", help="category id")
    parser.add_argument("--basis", default="", choices=("",) + BASES,
                        help="unit basis for the comparison")
    parser.add_argument("--note", default="", help="note shown under the row")
    parser.add_argument("--into", default="", metavar="TITLE",
                        help="add these chains to an existing row")
    args = parser.parse_args()

    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    categories = [c["id"] for c in config["categories"]]
    build_id = ""
    if STATE.exists():
        build_id = json.loads(STATE.read_text(encoding="utf-8")).get("colesBuildId", "")

    found: dict[str, retailers.Offer] = {}
    for url in args.urls:
        chain, product_id = identify(url)
        if chain in found:
            raise SystemExit(f"Two {chain} addresses given; one per chain.")
        print(f"Checking {chain} {product_id}...", flush=True)
        offer = fetch(chain, product_id, build_id)
        found[chain] = offer
        print(f"  {offer.name}  |  {offer.size}  |  ${offer.price:.2f}")

    if args.into:
        row = next(
            (i for i in config["items"] if i["title"].lower() == args.into.lower()),
            None,
        )
        if row is None:
            raise SystemExit(f"No row titled {args.into!r}.")
        for chain, offer in found.items():
            row[chain] = offer.product_id
        print(f"\nAdded to existing row: {row['title']}")
    else:
        sample = next(iter(found.values()))
        title = args.title or f"{sample.name} {sample.size}".strip()
        basis = args.basis or suggest_basis(sample.size, title)
        basis = args.basis or ask(
            f"Compare {title!r} on which basis?", BASES, basis
        )
        category = args.category or ask(
            "Which category?", tuple(categories), categories[0]
        )
        if category not in categories:
            raise SystemExit(
                f"Unknown category {category!r}. Known: {', '.join(categories)}"
            )
        row = {
            "title": title,
            "category": category,
            "unitBasis": basis,
            "woolworths": found["woolworths"].product_id if "woolworths" in found else None,
            "coles": found["coles"].product_id if "coles" in found else None,
        }
        if args.note:
            row["note"] = args.note
        config["items"].append(row)
        print(f"\nAdded row: {title}  [{category}, per {basis}]")

    CONFIG.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    print(f"{CONFIG.name} now tracks {len(config['items'])} products.")
    print("Run 'python fetch_prices.py' to rebuild the page.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
