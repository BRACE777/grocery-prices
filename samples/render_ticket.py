"""Sample B: The Shelf Ticket.

A wall of Australian shelf-edge price tickets, with one inversion: the legally
mandated unit-pricing line, normally set in the smallest type on the ticket, is
promoted to the headline. The pack price becomes the fine print instead.

Two tickets per product sit in a rail, one green-railed and one red-railed. The
cheaper ticket stands proud of its neighbour.

Motion: tickets are slotted into the rail from the left at an aisle's cadence,
then the cheaper of each pair rises proud. Specials flash their ticket in last.
Under reduced motion the tickets are already seated and the winner already
raised.
"""

from __future__ import annotations

import common as c

FONT = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?'
    "family=Barlow+Condensed:wght@400;500;600;700&family=Barlow:wght@400;500;700"
    '&display=swap" rel="stylesheet">'
)

CSS = """
:root{
  --aisle:#e3e7e6; --rail:#aeb6b3; --card:#ffffff;
  --ink:#111315; --ink-soft:#697370; --hair:#c9cfcd;
  --card-ink:#111315; --card-soft:#697370;
  --wool:#0f8a3f; --coles:#d8121f; --flash:#ffd400;
  --ease:cubic-bezier(0.16,1,0.3,1); --step:34ms;
  color-scheme:light dark;
}
/* The aisle after hours. Printed card does not change colour, so the tickets
   stay white and only the aisle around them goes dark. */
@media (prefers-color-scheme:dark){
  :root{--aisle:#191c1d; --rail:#333a3c; --hair:#3d4446;
        --ink:#e9edea; --ink-soft:#9aa4a0}
}
*{box-sizing:border-box}
body{
  margin:0; background:var(--aisle); color:var(--ink);
  font-family:Barlow,system-ui,sans-serif; font-size:15px; line-height:1.35;
  font-variant-numeric:tabular-nums; -webkit-text-size-adjust:100%;
}
::selection{background:var(--flash); color:#111315}
:focus-visible{outline:2px solid var(--flash); outline-offset:3px}
main{max-width:44rem; margin:0 auto; padding:0 .75rem 3rem}

.masthead{padding:1.9rem .25rem 1.1rem}
.masthead h1{
  font-family:"Barlow Condensed",sans-serif; font-weight:700; font-size:1.95rem;
  line-height:1; letter-spacing:-.01em; text-transform:uppercase; margin:0;
}
.masthead p{margin:.45rem 0 0; color:var(--ink-soft); max-width:60ch}
.masthead b{color:var(--ink); font-weight:700}

/* The deepest cut of the week wears the flash ticket, full width. */
.flashcard{
  background:var(--flash); color:#111315; padding:.9rem 1rem 1rem;
  display:flex; flex-direction:column; gap:.15rem;
}
.flashcard .lede{
  font-family:"Barlow Condensed",sans-serif; font-weight:700;
  text-transform:uppercase; letter-spacing:.12em; font-size:.95rem;
}
.flashcard .what{font-family:"Barlow Condensed",sans-serif; font-weight:600;
  font-size:1.35rem; line-height:1.1; text-transform:uppercase}
.flashcard .figs{display:flex; align-items:baseline; gap:.6rem; margin-top:.25rem}
.flashcard .big{font-family:"Barlow Condensed",sans-serif; font-weight:700;
  font-size:2.6rem; line-height:.9}
.flashcard .was{text-decoration:line-through; opacity:.7; font-weight:500}

/* Aisle sign. */
h2{
  font-family:"Barlow Condensed",sans-serif; font-weight:700; font-size:1.1rem;
  text-transform:uppercase; letter-spacing:.16em; margin:2.1rem 0 .55rem;
  padding-bottom:.3rem; border-bottom:2px solid var(--hair);
  display:flex; justify-content:space-between; align-items:baseline; gap:1em;
}
h2 em{font-family:Barlow,sans-serif; font-style:normal; font-weight:500;
  font-size:.8rem; letter-spacing:.04em; color:var(--ink-soft)}

/* A pair of tickets in one rail slot. */
.pair{margin:0 0 1.15rem}
.pair > .rail{
  display:grid; grid-template-columns:1fr 1fr; gap:.5rem; align-items:end;
  padding-bottom:.5rem; border-bottom:3px solid var(--rail);
}
.ticket{
  background:var(--card); color:var(--card-ink); text-decoration:none;
  display:flex; flex-direction:column; min-height:9.5rem;
  border-top:5px solid var(--chain);
  box-shadow:0 1px 2px rgba(0,0,0,.16);
  transition:transform 180ms var(--ease),box-shadow 180ms var(--ease);
}
/* Tickets are seated by default. The slot-in only slides them; nothing here
   animates from invisible, so a page that never animates is still readable. */
@keyframes seat{from{transform:translateX(-16px)} to{transform:none}}
@keyframes proud{
  from{transform:translateX(-16px)}
  55%{transform:translateY(0)}
  to{transform:translateY(-9px)}
}
@keyframes flash{from{transform:scale(.86)} to{transform:none}}
@media (prefers-reduced-motion:no-preference){
  .ticket,.blank{animation:seat 420ms var(--ease) both;
                 animation-delay:calc(var(--i,0)*var(--step))}
  .ticket.proud{animation:proud 560ms var(--ease) both;
                animation-delay:calc(var(--i,0)*var(--step) + 180ms)}
  .ticket .flash{animation:flash 300ms var(--ease) both;
                 animation-delay:calc(var(--i,0)*var(--step) + 340ms)}
  .flashcard{animation:seat 460ms var(--ease) both}
}
.ticket[data-chain=woolworths]{--chain:var(--wool)}
.ticket[data-chain=coles]{--chain:var(--coles)}
.ticket .chain{
  font-family:"Barlow Condensed",sans-serif; font-weight:700; font-size:.78rem;
  letter-spacing:.16em; text-transform:uppercase; color:var(--chain);
  padding:.35rem .6rem 0;
}
.ticket .name{
  font-family:"Barlow Condensed",sans-serif; font-weight:500; font-size:.92rem;
  line-height:1.1; text-transform:uppercase; padding:.15rem .6rem .35rem;
  color:var(--card-ink);
}
.ticket .unit{
  margin-top:auto; padding:0 .6rem; display:flex; align-items:baseline;
  gap:.1rem;
}
.ticket .unit .cur{
  font-family:"Barlow Condensed",sans-serif; font-weight:600;
  font-size:1.05rem; align-self:flex-start; margin-top:.12rem;
}
.ticket .unit .n{
  font-family:"Barlow Condensed",sans-serif; font-weight:700; font-size:2.5rem;
  line-height:.88; letter-spacing:-.02em;
}
.ticket .unit .per{
  font-family:"Barlow Condensed",sans-serif; font-weight:600; font-size:.85rem;
  text-transform:uppercase; letter-spacing:.06em; color:var(--card-soft);
}
.ticket .pack{
  padding:.15rem .6rem .55rem; font-size:.82rem; color:var(--card-soft);
}
/* The cheaper ticket stands proud in the rail. */
.ticket.proud{
  transform:translateY(-9px);
  box-shadow:0 7px 14px rgba(0,0,0,.2),0 2px 3px rgba(0,0,0,.14);
}
.ticket:hover{transform:translateY(-13px)}
.ticket.proud:hover{transform:translateY(-15px)}
/* The special flash, slotted in behind the price. */
.ticket .flash{
  align-self:flex-start; margin:.35rem .6rem 0; background:var(--flash);
  color:#111315; font-family:"Barlow Condensed",sans-serif; font-weight:700;
  font-size:.78rem; letter-spacing:.1em; text-transform:uppercase;
  padding:.1rem .4rem;
}

/* An empty slot in the rail: the chain does not stock it. */
.blank{
  min-height:9.5rem; display:flex; align-items:flex-end; padding:.6rem;
  border-top:5px solid var(--rail);
  background-image:repeating-linear-gradient(45deg,
    var(--rail) 0 1px,transparent 1px 5px);
  font-family:"Barlow Condensed",sans-serif; text-transform:uppercase;
  letter-spacing:.1em; font-size:.82rem; color:var(--ink);
  font-weight:600; opacity:.82;
}
.broke{
  min-height:9.5rem; display:flex; align-items:flex-end; padding:.6rem;
  border-top:5px solid var(--coles); box-shadow:inset 0 0 0 2px var(--coles);
  background:var(--card); color:#c00d1a; font-weight:700;
  font-family:"Barlow Condensed",sans-serif; text-transform:uppercase;
  letter-spacing:.08em; font-size:.85rem;
}
.pair .note{margin:.4rem .1rem 0; font-size:.85rem; color:var(--ink-soft)}

footer{margin-top:2.4rem; padding-top:1rem; border-top:2px solid var(--hair);
  color:var(--ink-soft); font-size:.88rem}
footer p{margin:.4rem 0} footer code{font-family:ui-monospace,monospace;
  color:var(--ink); font-size:.85rem}

@media (prefers-reduced-motion:reduce){
  .ticket:hover,.ticket.proud:hover{transform:translateY(-9px)}
}
"""


def _ticket(row: dict, chain: str, index: int) -> str:
    state = c.offer_state(row, chain)
    label = c.CHAIN_LABEL[chain]
    if state == "missing":
        return (
            f'<div class="blank" style="--i:{index}">{label} '
            f"does not stock it</div>"
        )
    offer = row["offers"][chain]
    if state == "failed":
        return f'<div class="broke">{label} — could not read, repin</div>'

    proud = " proud" if c.cheaper(row) == chain else ""
    unit = (
        f'<span class="n">{c.money(offer["comparablePrice"])}</span>'
        f'<span class="per">{c.e(offer["comparableLabel"])}</span>'
        if offer["comparablePrice"] is not None
        else '<span class="n">—</span>'
    )
    was = (
        f'was ${c.money(offer["wasPrice"])} · ' if offer["wasPrice"] else ""
    )
    flash = ""
    if offer["onSpecial"]:
        flash = f'<span class="flash">{c.e(offer["specialLabel"] or "Special")}</span>'
    return (
        f'<a class="ticket{proud}" data-chain="{chain}" style="--i:{index}" '
        f'href="{c.e(offer["url"])}" rel="noreferrer">'
        f'<span class="chain">{label}</span>'
        f'<span class="name">{c.e(offer["name"] or row["title"])}'
        f'{" · " + c.e(offer["size"]) if offer["size"] else ""}</span>'
        f"{flash}"
        f'<span class="unit"><span class="cur">$</span>{unit}</span>'
        f'<span class="pack">{was}${c.money(offer["price"])} a pack</span></a>'
    )


def render(payload: dict) -> str:
    stats = c.stats(payload)
    head = c.headline(payload)
    step = 0
    parts: list[str] = []

    parts.append('<div class="masthead"><h1>What is worth<br>buying this week</h1>')
    parts.append(
        f'<p>Every price per 100g, per litre or per can, because that is the '
        f"number that decides. Read "
        f'<b>{c.e(payload["generatedLabel"])}</b>. '
        f'<b>{stats["specials"]}</b> of the {stats["rows"] * 2} prices are on '
        f"special.</p></div>"
    )

    if head:
        offer = head["offer"]
        parts.append(
            f'<div class="flashcard"><span class="lede">Deepest cut this week'
            f'</span><span class="what">{c.e(head["row"]["title"])}</span>'
            f'<span class="figs"><span class="big">'
            f'${c.money(offer["price"])}</span>'
            f'<span class="was">was ${c.money(offer["wasPrice"])}</span>'
            f'<span>at {c.CHAIN_LABEL[head["chain"]]}, '
            f'{head["percent"]}% off</span></span></div>'
        )

    for category, rows in c.grouped(payload):
        specials = sum(
            1 for r in rows for o in r["offers"].values() if o.get("onSpecial")
        )
        tail = f"{specials} on special" if specials else "nothing on special"
        parts.append(f"<h2>{c.e(category['label'])}<em>{tail}</em></h2>")
        for row in rows:
            step = min(step + 1, 26)
            tickets = "".join(_ticket(row, chain, step) for chain in c.CHAINS)
            note = (
                f'<p class="note">{c.e(row["note"])}</p>' if row["note"] else ""
            )
            parts.append(f'<div class="pair"><div class="rail">{tickets}</div>{note}</div>')

    parts.append(
        f"<footer><p>Woolworths is cheaper on "
        f'{stats["wins"]["woolworths"]} of the {stats["rows"]} lines, Coles on '
        f'{stats["wins"]["coles"]}.</p>'
        f"<p>Standard shelf prices. No Everyday Rewards or Flybuys member "
        f"pricing, and in-store prices may differ.</p>"
        f"<p>Add a product with <code>python add_item.py</code> and the "
        f"address copied from either shop.</p></footer>"
    )

    return (
        "<!doctype html><html lang=en-AU><head><meta charset=utf-8>"
        '<meta name=viewport content="width=device-width,initial-scale=1">'
        "<title>Personal Shopping · Shelf Ticket</title>"
        f"{FONT}<style>{CSS}</style></head><body><main>"
        f'{"".join(parts)}</main></body></html>'
    )


if __name__ == "__main__":
    print(c.write("ticket.html", render(c.load())))
