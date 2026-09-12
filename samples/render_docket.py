"""Sample A: The Split Docket.

A supermarket receipt that cannot decide which shop it came from, so it prints
both chains and rules a line through the dearer price per unit.

Disciplines carried into this world from the challengers it beat:
  one type size only, rank from weight, case, reversal and rule;
  hierarchy from indentation and full-width rules, no cards and no shadows;
  a chain that does not stock an item dithers to half density;
  one dominant moment per viewport;
  the docket prints its own instruction for adding a line;
  the chain colour is the only accent and the only interactive affordance.

Motion: the docket prints. Blocks reveal top to bottom at a printer's cadence,
and each strike-through draws across the figure it cancels once its line has
landed. Under reduced motion the page is simply already printed.
"""

from __future__ import annotations

import common as c

FONT = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?'
    "family=Sometype+Mono:wght@400;500;600;700&display=swap"
    '" rel="stylesheet">'
)

CSS = """
:root{
  --paper:#f2f4f3; --ink:#16181a; --ink-soft:#5c6360; --feed:#c3cac6;
  --wool:#0b6b33; --wool-mark:#0f8a3f;
  --coles:#b80f22; --coles-mark:#d8121f;
  --plate:#16181a; --plate-ink:#f2f4f3;
  --size:15px; --lh:1.5; --gap:10px;
  --step:26ms;
  --ease:cubic-bezier(0.16,1,0.3,1);
  color-scheme:light dark;
}
/* The carbon copy: the same docket as an NCR duplicate. */
@media (prefers-color-scheme:dark){
  :root{
    --paper:#15171a; --ink:#e7eae6; --ink-soft:#8e9793; --feed:#343a3d;
    --wool:#5ccf85; --wool-mark:#3fae69;
    --coles:#ff8a92; --coles-mark:#e2515c;
    --plate:#e7eae6; --plate-ink:#15171a;
  }
}
*{box-sizing:border-box}
html{background:var(--feed)}
body{
  margin:0; background:var(--feed);
  font-family:"Sometype Mono",ui-monospace,"Cascadia Mono","Segoe UI Mono",
    "DejaVu Sans Mono",monospace;
  font-size:var(--size); line-height:var(--lh); color:var(--ink);
  font-variant-numeric:tabular-nums; font-feature-settings:"tnum" 1;
  -webkit-text-size-adjust:100%;
  display:flex; justify-content:center; padding:0 0 0;
}
::selection{background:var(--ink); color:var(--paper)}
:focus-visible{outline:2px solid var(--ink); outline-offset:2px}

/* The roll itself. On a phone it is the whole screen; on a desk it sits on the
   counter with the feed showing above and below. */
.roll{
  width:100%; max-width:27rem; background:var(--paper);
  padding:0 1.15rem 0; position:relative;
}
/* Tear edges, top and bottom, cut from the paper rather than drawn on it. */
.roll::before,.roll::after{
  content:""; display:block; height:9px; background:var(--paper);
  -webkit-mask-image:var(--tear); mask-image:var(--tear);
  -webkit-mask-size:14px 9px; mask-size:14px 9px;
  -webkit-mask-repeat:repeat-x; mask-repeat:repeat-x;
  margin:0 -1.15rem;
}
.roll::before{--tear:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='9'%3E%3Cpath d='M0 9 L7 0 L14 9 Z' fill='%23000'/%3E%3C/svg%3E")}
.roll::after{--tear:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='9'%3E%3Cpath d='M0 0 L7 9 L14 0 Z' fill='%23000'/%3E%3C/svg%3E")}

/* The docket is fully printed by default. The print reveal is a transition
   out of @starting-style rather than a filled animation, so the printed state
   is the element's real state: if the transition never runs, for any reason,
   the page is finished rather than blank. */
.b{clip-path:inset(0 0 -2% 0)}
@media (prefers-reduced-motion:no-preference){
  /* Each block is revealed as the print head passes over it. */
  .b{transition:
      clip-path 380ms var(--ease) calc(var(--i,0)*var(--step)),
      transform 380ms var(--ease) calc(var(--i,0)*var(--step));}
  @starting-style{
    .b{clip-path:inset(0 0 100% 0); transform:translateY(-3px)}
  }
  .dearer .unit::after{
    transition:transform 260ms var(--ease)
      calc(var(--i,0)*var(--step) + 340ms);
  }
  @starting-style{.dearer .unit::after{transform:scaleX(0)}}
}

h1{font-size:1em; font-weight:700; letter-spacing:.22em; margin:1.5rem 0 0;
   text-align:center; text-transform:uppercase}
.sub{text-align:center; letter-spacing:.14em; text-transform:uppercase;
     font-weight:500; margin:.15rem 0 0}
.sub b{font-weight:700}
.meta{display:flex; justify-content:space-between; color:var(--ink-soft);
      text-transform:uppercase; letter-spacing:.06em; margin:.35rem 0 0}

hr{border:0; height:0; border-top:1px dashed var(--feed); margin:.85rem 0}
hr.solid{border-top:1px solid var(--ink)}

/* The one dominant moment: the deepest cut of the week, reversed rather than
   enlarged, because nothing on this page changes size. */
.plate{background:var(--plate); color:var(--plate-ink); margin:0 -1.15rem;
       padding:.8rem 1.15rem .85rem}
.plate p{margin:0}
.plate .lede{font-weight:700; letter-spacing:.2em; text-transform:uppercase}
.plate .what{font-weight:500; text-transform:uppercase; margin-top:.35rem}
.plate .figs{display:flex; gap:1.1em; margin-top:.2rem; flex-wrap:wrap}
.plate .was{text-decoration:line-through;
            text-decoration-thickness:1px; opacity:.65}

h2{font-size:1em; font-weight:700; letter-spacing:.2em; text-transform:uppercase;
   margin:0 0 .5rem; display:flex; justify-content:space-between; gap:1em}
h2{align-items:baseline}
h2 b{flex:1 1 auto; min-width:0; font-weight:700}
h2 span{font-weight:400; color:var(--ink-soft); letter-spacing:.06em;
        white-space:nowrap; flex:0 0 auto}

.line{margin:0 0 .95rem}
.name{font-weight:600; text-transform:uppercase; letter-spacing:.03em;
      margin:0 0 .2rem}
.note{color:var(--ink-soft); margin:0 0 .25rem; padding-left:1.35em}

/* One offer. The whole row is the link, and the chain colour is its only mark. */
a.offer{
  display:grid; grid-template-columns:1.35em 1fr auto; align-items:baseline;
  column-gap:.55em; text-decoration:none; color:inherit; padding:.08rem 0;
}
a.offer .mark{font-weight:700}
a.offer[data-chain=woolworths] .mark{color:var(--wool-mark)}
a.offer[data-chain=coles] .mark{color:var(--coles-mark)}
a.offer[data-chain=woolworths] .chain{color:var(--wool)}
a.offer[data-chain=coles] .chain{color:var(--coles)}
a.offer .chain{text-transform:uppercase; letter-spacing:.08em; font-weight:500}
a.offer .figs{display:flex; gap:.9em; align-items:baseline}
a.offer .unit{font-weight:700; position:relative}
a.offer .pack{color:var(--ink-soft)}
a.offer:hover .chain{text-decoration:underline; text-underline-offset:3px}
/* Ink press: the line inverts under the thumb. */
a.offer:active{background:var(--ink); color:var(--paper)}
a.offer:active .chain,a.offer:active .mark,a.offer:active .pack{color:inherit}

/* The strike stands on the dearer unit price, and is drawn across it once
   its line has landed when motion is allowed. */
.dearer .unit{font-weight:400; color:var(--ink-soft)}
.dearer .unit::after{
  content:""; position:absolute; left:-.1em; right:-.1em; top:52%;
  border-top:1px solid currentColor; transform-origin:left;
  transform:scaleX(1);
}

.flag{font-weight:700; text-transform:uppercase; letter-spacing:.08em}
a.offer[data-chain=woolworths] .flag{color:var(--wool)}
a.offer[data-chain=coles] .flag{color:var(--coles)}

/* Not stocked is a material state: the cell dithers to half density. */
.gone{
  display:grid; grid-template-columns:1.35em 1fr; column-gap:.55em;
  color:var(--ink-soft); background-image:repeating-linear-gradient(
    45deg,var(--feed) 0 1px,transparent 1px 4px);
  background-clip:padding-box;
}
.gone .chain{text-transform:uppercase; letter-spacing:.08em}
.broke{color:var(--coles); font-weight:700; text-transform:uppercase;
       letter-spacing:.06em; box-shadow:inset 0 0 0 1px var(--coles);
       padding:.1rem .4rem; display:block}

footer{padding:0 0 1.6rem; color:var(--ink-soft)}
footer p{margin:.35rem 0}
footer code{font:inherit; color:var(--ink); font-weight:600}
.totals{display:flex; justify-content:space-between; color:var(--ink);
        font-weight:700; text-transform:uppercase; letter-spacing:.1em}

"""


def _offer_line(row: dict, chain: str, index: int) -> str:
    state = c.offer_state(row, chain)
    short = c.CHAIN_SHORT[chain]
    if state == "missing":
        return (
            f'<div class="gone"><span aria-hidden="true">–</span>'
            f'<span><span class="chain">{short}</span> does not stock it</span></div>'
        )
    offer = row["offers"][chain]
    if state == "failed":
        return (
            f'<div class="gone"><span aria-hidden="true">!</span>'
            f'<span class="broke">{short} — could not read, repin</span></div>'
        )

    flag = ""
    if offer["onSpecial"]:
        label = offer["specialLabel"] or "Special"
        flag = f'<span class="flag">{c.e(label)}</span>'
    klass = "offer dearer" if state == "dearer" else "offer"
    unit = (
        f'{c.money(offer["comparablePrice"])}{c.e(offer["comparableLabel"])}'
        if offer["comparablePrice"] is not None
        else "—"
    )
    return (
        f'<a class="{klass}" data-chain="{chain}" style="--i:{index}" '
        f'href="{c.e(offer["url"])}" rel="noreferrer">'
        f'<span class="mark" aria-hidden="true">■</span>'
        f'<span><span class="chain">{short}</span> {flag}</span>'
        f'<span class="figs"><span class="pack">{c.money(offer["price"])}</span>'
        f'<span class="unit">{unit}</span></span></a>'
    )


def render(payload: dict) -> str:
    step = 0

    def nxt() -> int:
        nonlocal step
        step += 1
        return min(step, 34)

    stats = c.stats(payload)
    head = c.headline(payload)

    parts: list[str] = []
    parts.append(f'<div class="b" style="--i:{nxt()}">')
    parts.append("<h1>Personal Shopping</h1>")
    parts.append('<p class="sub"><b>Woolworths</b> against <b>Coles</b></p>')
    parts.append(
        f'<p class="meta"><span>{c.e(payload["generatedLabel"])}</span>'
        f'<span>{stats["rows"]} lines</span></p>'
    )
    parts.append("<hr class=solid></div>")

    if head:
        offer = head["offer"]
        parts.append(
            f'<div class="b plate" style="--i:{nxt()}">'
            f"<p class=lede>Deepest cut this week</p>"
            f'<p class=what>{c.e(head["row"]["title"])}</p>'
            f'<p class=figs><span>{c.CHAIN_LABEL[head["chain"]]} '
            f'${c.money(offer["price"])}</span>'
            f'<span class=was>${c.money(offer["wasPrice"])}</span>'
            f'<span>{head["percent"]}% off</span></p></div>'
        )

    for category, rows in c.grouped(payload):
        specials = sum(
            1 for r in rows for o in r["offers"].values() if o.get("onSpecial")
        )
        parts.append(f'<div class="b" style="--i:{nxt()}"><hr>')
        tail = f"{specials} on special" if specials else "nothing on special"
        parts.append(
            f"<h2><b>{c.e(category['label'])}</b><span>{tail}</span></h2></div>"
        )
        for row in rows:
            index = nxt()
            body = [f'<div class="b line" style="--i:{index}">']
            body.append(f'<p class="name">{c.e(row["title"])}</p>')
            for chain in c.CHAINS:
                body.append(_offer_line(row, chain, index))
            if row["note"]:
                body.append(f'<p class="note">{c.e(row["note"])}</p>')
            body.append("</div>")
            parts.append("".join(body))

    parts.append(f'<div class="b" style="--i:{nxt()}"><hr class=solid>')
    parts.append(
        f'<p class="totals"><span>Cheaper more often</span>'
        f'<span>Woolies {stats["wins"]["woolworths"]} · '
        f'Coles {stats["wins"]["coles"]}</span></p>'
    )
    parts.append("<hr>")
    parts.append("<footer>")
    parts.append(
        f'<p>{stats["specials"]} of {len(payload["rows"]) * 2} prices on special. '
        f"Standard shelf prices, no member pricing. In-store may differ.</p>"
    )
    parts.append(
        "<p>To add a line, run <code>python add_item.py</code> with the "
        "product address copied from either shop.</p>"
    )
    if stats["failures"]:
        parts.append(
            f'<p class="broke">{stats["failures"]} lines could not be read</p>'
        )
    parts.append("</footer></div>")

    return (
        "<!doctype html><html lang=en-AU><head><meta charset=utf-8>"
        '<meta name=viewport content="width=device-width,initial-scale=1">'
        "<title>Personal Shopping · Docket</title>"
        f"{FONT}<style>{CSS}</style></head><body>"
        f'<main class="roll">{"".join(parts)}</main>'
        "</body></html>"
    )


if __name__ == "__main__":
    print(c.write("docket.html", render(c.load())))
