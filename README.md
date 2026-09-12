# Woolworths against Coles

A weekly price comparison for one household's actual shopping list. It reads
the current online price of 23 pinned products from both chains, works out
which is cheaper per unit, and says whether each price is unusual for that
product rather than just whether the shop has badged it a special.

The page is built as static HTML and published to GitHub Pages, so it opens on
a phone from anywhere.

## Why it runs on this PC and not in the cloud

Woolworths returns 403 to data centre addresses. The same request from a home
connection returns 200. Coles serves the real site to curl and a bot challenge
to Python's own HTTP client from the same address with identical headers, which
is why every request here goes out through curl.

One more, found the hard way and worth knowing before touching
`retailers.py`: Coles serves a bot challenge to every request carrying
`Accept-Language: en-AU,en;q=0.9`, and the real site to the same request
carrying `en-US,en;q=0.9`. No other header changes the outcome, and it
reproduces on demand. Woolworths is unaffected and keeps `en-AU`.

None of those is a stable contract. All are undocumented internal endpoints
and either chain can change them without notice. When a run starts failing,
that file's comments record what was true and how it was measured.

## Running it

    python fetch_prices.py          fetch both chains and rebuild the page
    python fetch_prices.py --render rebuild the page from the last fetch
    run_weekly.cmd                  fetch, rebuild, commit and publish

A scheduled task runs `run_weekly.cmd` every Wednesday at 7am, and on the next
wake if the machine was asleep.

## Adding a product

Copy the product's web address from either shop and paste it in:

    python add_item.py <woolworths url> <coles url>
    python add_item.py <url>                       one chain only
    python add_item.py <url> --into "Beef Mince Regular 500g"

The product is fetched once to confirm the identifier resolves, so a row is
never pinned to something that does not exist. `products.json` is plain text
and can also be edited by hand.

## What the page shows

Each product gets one ticket per chain. The pack price leads, because that is
the number already known by heart. The unit price sits beneath it and is what
actually decides which chain is cheaper, so a larger pack can win while costing
more.

Above the list, **worth stocking up on** ranks this week's specials by how
unusual the price is over the last 90 days rather than by the size of the
discount. A product that drops every fortnight is not news; the same product at
a genuine three-month low is. The same measure puts a stamp on individual
tickets, including on prices the shop has not badged at all.

## What it does not do

- **No member pricing.** Neither Everyday Rewards nor Flybuys prices are
  published without signing in, confirmed across 250 Woolworths and 53 Coles
  products. Every price here is the standard shelf price.
- **No store selection.** Woolworths offers none without signing in, and two
  Victorian Coles stores returned identical prices. Prices are national online
  prices and in-store may differ.
- **No guessed products.** Every row is pinned to a product identifier. When a
  chain does not stock a line the page says so; when a pin stops resolving the
  page shows it in red, which means the pin needs fixing.

## Files

| File | Purpose |
|---|---|
| `products.json` | The 23 pinned products, their categories and unit bases |
| `fetch_prices.py` | The run: fetch, measure, render |
| `retailers.py` | Woolworths and Coles clients |
| `history.py` | Price history and how unusual today's price is |
| `sizes.py` | Pack sizes reduced to comparable quantities |
| `render.py` | The page |
| `add_item.py` | Add a product by pasting its address |
| `docs/index.html` | The published page |
| `docs/data.json` | The last fetch, as data |
| `samples/` | Two visual directions that were not chosen |

## Data sources

Current prices and special flags come from each chain's own product listing.
Price history comes from the [hotprices.org](https://hotprices.org) community
dataset, built by [Javex/hotprices-au](https://github.com/Javex/hotprices-au)
under the MIT licence, which is cached in `cache/` and refreshed daily at most.
