"""Sample C: The Pocket Timetable Slide Rack.

Prices as a departure table. One type size for the whole page, so rank has to
be carried by weight, case, reversal and rule instead of scale. Slides are
seated in a raked rack with flat baselines, a tick rail shows position and
extent, and state is a mark in a fixed cell: filled holds the cheaper rate,
hollow does not.

Two translations, both named rather than silent. The world's bottle green and
vermilion are mapped onto the pinned chain colours, green for Woolworths and
red for Coles. And the rack travels vertically rather than laterally, because
a phone scrolls down and the task is reading a list.

Motion: one light travels the bed along the rake, once, passing over the slides
in sequence so it reads as a single light rather than 23 separate entrances.
Vermilion strikes draw after the light has passed. Reduced motion parks the
light at full illumination.
"""

from __future__ import annotations

import common as c

FONT = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?'
    "family=Archivo+Narrow:wght@400;500;600;700&display=swap"
    '" rel="stylesheet">'
)

CSS = """
:root{
  --bed:#d8b552; --bed-lit:#f0d98a; --glass:#48525c; --carbon:#17181a;
  --ivory:#f4efe2; --ivory-dim:#e4dcc8;
  --wool:#14543a; --coles:#c23a17;
  --size:14px; --rake:11deg; --lift:.85rem;
  --ease:cubic-bezier(0.16,1,0.3,1); --step:30ms;
  color-scheme:light dark;
}
/* The light table switched off. The stock keeps its tint; only the bed dims. */
@media (prefers-color-scheme:dark){
  :root{
    --bed:#2a2b26; --bed-lit:#4a4634; --glass:#9aa6b0; --carbon:#f4efe2;
    --ivory:#22242a; --ivory-dim:#1b1d22;
    --wool:#5fcf92; --coles:#ff9270;
  }
}
*{box-sizing:border-box}
body{
  margin:0; color:var(--carbon);
  background:
    radial-gradient(120% 60% at 50% -10%,var(--bed-lit) 0%,transparent 60%),
    var(--bed);
  background-attachment:fixed;
  font-family:"Archivo Narrow",system-ui,sans-serif;
  font-size:var(--size); line-height:1.45; font-variant-numeric:tabular-nums;
  -webkit-text-size-adjust:100%;
}
::selection{background:var(--carbon); color:var(--ivory)}
:focus-visible{outline:2px solid var(--carbon); outline-offset:2px}

.bed{max-width:40rem; margin:0 auto; padding:1.4rem .8rem 3rem;
     display:grid; grid-template-columns:var(--lift) 1fr; column-gap:.5rem}

/* Tick rail: one tick per category, its height the extent of that block. */
.rail{position:relative; border-right:1px solid var(--glass)}
.rail ol{list-style:none; margin:0; padding:0; height:100%;
         display:flex; flex-direction:column; gap:2px}
.rail li{
  background:var(--glass); opacity:.34; position:relative;
  flex-grow:var(--extent,1); min-height:1.1rem;
  clip-path:polygon(0 0,100% var(--skew),100% 100%,0 calc(100% - var(--skew)));
  --skew:4px;
}
.rail li.hot{opacity:.8}
.rail b{position:absolute; width:1px; height:1px; overflow:hidden; clip-path:inset(50%)}

.rack{min-width:0}
h1{
  font-size:inherit; font-weight:700; text-transform:uppercase;
  letter-spacing:.24em; margin:0 0 .15rem;
}
.stamp{display:flex; flex-wrap:wrap; gap:.15rem 1.1rem; margin:0 0 .9rem;
       text-transform:uppercase; letter-spacing:.08em; font-weight:500}
.stamp span{color:var(--carbon); opacity:.72}

/* One element per screen goes to an opaque reversed plate. */
.plate{
  background:var(--carbon); color:var(--ivory); padding:.6rem .75rem .65rem;
  margin:0 0 1rem;
  clip-path:polygon(0 0,100% 10px,100% 100%,0 calc(100% - 10px));
}
.plate p{margin:0; text-transform:uppercase; letter-spacing:.06em}
.plate .lede{font-weight:700; letter-spacing:.2em}
.plate .figs{display:flex; gap:1.1em; flex-wrap:wrap; font-weight:500}
.plate s{opacity:.6}

/* A slide: raked container, flat baselines, opaque ivory prose pane. */
.slide{
  background:var(--ivory); margin:0 0 .55rem; padding:.55rem .75rem .6rem;
  clip-path:polygon(0 0,100% 9px,100% 100%,0 calc(100% - 9px));
}
/* The light travelling the bed: each slide is lit as it passes. It dims the
   stock rather than hiding it, so the rack is legible with no motion at all. */
@keyframes light{
  from{background-color:var(--ivory-dim); filter:brightness(.88) saturate(.72);
       transform:translateY(6px)}
  to{background-color:var(--ivory); filter:none; transform:none}
}
@keyframes strike{from{transform:scaleX(0)} to{transform:scaleX(1)}}
@media (prefers-reduced-motion:no-preference){
  .slide{animation:light 520ms var(--ease) both;
         animation-delay:calc(var(--i,0)*var(--step))}
  a.dep.struck .ut::after{
    transform:scaleX(0);
    animation:strike 240ms var(--ease) both;
    animation-delay:calc(var(--i,0)*var(--step) + 420ms);
  }
}
.slide > h2{
  font-size:inherit; font-weight:700; text-transform:uppercase;
  letter-spacing:.18em; margin:0 0 .4rem; padding-bottom:.3rem;
  border-bottom:1px solid var(--glass);
  display:flex; justify-content:space-between; gap:1em;
}
.slide > h2 em{font-style:normal; font-weight:400; letter-spacing:.04em;
               text-transform:none; opacity:.7}

.run{margin:0 0 .5rem}
.run:last-child{margin-bottom:0}
.run > p.what{margin:0; font-weight:700; text-transform:uppercase;
              letter-spacing:.02em}
.run > p.note{margin:.1rem 0 0; padding-left:1.4em; opacity:.7}

/* One departure. State is the mark in the fixed first cell. */
a.dep{
  display:grid; grid-template-columns:1.4em 4.6em 1fr auto; align-items:baseline;
  column-gap:.5em; text-decoration:none; color:inherit;
}
a.dep .mk{font-weight:700}
a.dep .co{text-transform:uppercase; letter-spacing:.1em; font-weight:500}
a.dep .pk{opacity:.7}
a.dep .ut{font-weight:700; text-align:right; position:relative;
          white-space:nowrap}
a.dep[data-chain=woolworths]{--c:var(--wool)}
a.dep[data-chain=coles]{--c:var(--coles)}
a.dep.holds .mk,a.dep.holds .co,a.dep.holds .ut{color:var(--c)}
a.dep:hover .co{text-decoration:underline; text-underline-offset:3px}
a.dep:active{background:var(--carbon); color:var(--ivory)}
a.dep:active .mk,a.dep:active .co,a.dep:active .ut,a.dep:active .pk{color:inherit}

/* Vermilion strikes the rate it cancels, drawn after the light has passed. */
a.dep.struck .ut{opacity:.62}
a.dep.struck .ut::after{
  content:""; position:absolute; left:-.15em; right:-.15em; top:52%;
  border-top:1px solid var(--coles); transform-origin:right;
}

.hold{font-weight:700; text-transform:uppercase; letter-spacing:.08em;
      color:var(--c)}
/* Not stocked: the cell is hollow and dithers to half density. */
.void{
  display:grid; grid-template-columns:1.4em 1fr; column-gap:.5em;
  position:relative; isolation:isolate;
}
.void::before{
  content:""; position:absolute; inset:0; z-index:-1; opacity:.45;
  background-image:repeating-linear-gradient(var(--rake),
    var(--glass) 0 1px,transparent 1px 5px);
}
.void > *{opacity:.72}
.void .co{text-transform:uppercase; letter-spacing:.1em}
.fault{color:var(--coles); font-weight:700; text-transform:uppercase;
       letter-spacing:.06em; box-shadow:inset 0 0 0 1px var(--coles);
       padding:0 .35em}

footer{margin-top:1.4rem; background:var(--ivory); padding:.6rem .75rem .7rem;
       clip-path:polygon(0 0,100% 9px,100% 100%,0 calc(100% - 9px))}
footer p{margin:.25rem 0; opacity:.78}
footer code{font-family:ui-monospace,monospace; opacity:1; font-weight:600}

"""


def _dep(row: dict, chain: str, index: int) -> str:
    state = c.offer_state(row, chain)
    short = c.CHAIN_SHORT[chain]
    if state == "missing":
        return (
            f'<div class="void" data-chain="{chain}">'
            f'<span aria-hidden="true">○</span>'
            f'<span><span class="co">{short}</span> no service</span></div>'
        )
    offer = row["offers"][chain]
    if state == "failed":
        return (
            f'<div class="void" data-chain="{chain}">'
            f'<span aria-hidden="true">!</span>'
            f'<span class="fault">{short} fault — repin</span></div>'
        )

    holds = c.cheaper(row) == chain or c.only_stockist(row) == chain
    classes = ["dep"]
    if holds:
        classes.append("holds")
    if state == "dearer":
        classes.append("struck")
    mark = "●" if holds else "○"
    unit = (
        f'{c.money(offer["comparablePrice"])}{c.e(offer["comparableLabel"])}'
        if offer["comparablePrice"] is not None
        else "—"
    )
    hold = ""
    if offer["onSpecial"]:
        hold = f' <span class="hold">{c.e(offer["specialLabel"] or "Special")}</span>'
    return (
        f'<a class="{" ".join(classes)}" data-chain="{chain}" style="--i:{index}" '
        f'href="{c.e(offer["url"])}" rel="noreferrer">'
        f'<span class="mk" aria-hidden="true">{mark}</span>'
        f'<span class="co">{short}</span>'
        f'<span class="pk">{c.money(offer["price"])}{hold}</span>'
        f'<span class="ut">{unit}</span></a>'
    )


def render(payload: dict) -> str:
    stats = c.stats(payload)
    head = c.headline(payload)
    blocks = c.grouped(payload)
    step = 0

    rail = ['<div class="rail"><ol>']
    for position, (category, rows) in enumerate(blocks):
        hot = " class=hot" if position == 0 else ""
        rail.append(
            f'<li{hot} style="--extent:{len(rows)}">'
            f'<b>{c.e(category["label"].split(" ")[0])}</b></li>'
        )
    rail.append("</ol></div>")

    rack: list[str] = ['<div class="rack">']
    rack.append("<h1>Woolworths / Coles</h1>")
    rack.append(
        f'<p class="stamp"><span>{c.e(payload["generatedLabel"])}</span>'
        f'<span>{stats["rows"]} runs</span>'
        f'<span>{stats["specials"]} held down</span></p>'
    )

    if head:
        offer = head["offer"]
        rack.append(
            f'<div class="plate"><p class="lede">Deepest cut this week</p>'
            f'<p>{c.e(head["row"]["title"])}</p>'
            f'<p class="figs"><span>{c.CHAIN_LABEL[head["chain"]]} '
            f'${c.money(offer["price"])}</span>'
            f'<s>${c.money(offer["wasPrice"])}</s>'
            f'<span>{head["percent"]}% off</span></p></div>'
        )

    for category, rows in blocks:
        specials = sum(
            1 for r in rows for o in r["offers"].values() if o.get("onSpecial")
        )
        step = min(step + 1, 24)
        slide = [f'<section class="slide" style="--i:{step}">']
        tail = f"{specials} held down" if specials else "none held"
        slide.append(f'<h2>{c.e(category["label"])}<em>{tail}</em></h2>')
        for row in rows:
            slide.append('<div class="run">')
            slide.append(f'<p class="what">{c.e(row["title"])}</p>')
            for chain in c.CHAINS:
                slide.append(_dep(row, chain, step))
            if row["note"]:
                slide.append(f'<p class="note">{c.e(row["note"])}</p>')
            slide.append("</div>")
        slide.append("</section>")
        rack.append("".join(slide))

    rack.append(
        f"<footer><p>A filled mark holds the lower rate, or the only rate "
        f"there is. Vermilion strikes the "
        f"rate it cancels. Woolworths holds "
        f'{stats["wins"]["woolworths"]} runs, Coles '
        f'{stats["wins"]["coles"]}.</p>'
        f"<p>Standard shelf prices, no member pricing, in-store may differ.</p>"
        f"<p>Add a run with <code>python add_item.py</code> and a product "
        f"address.</p></footer>"
    )
    rack.append("</div>")

    return (
        "<!doctype html><html lang=en-AU><head><meta charset=utf-8>"
        '<meta name=viewport content="width=device-width,initial-scale=1">'
        "<title>Personal Shopping · Timetable</title>"
        f"{FONT}<style>{CSS}</style></head><body>"
        f'<main class="bed">{"".join(rail)}{"".join(rack)}</main>'
        "</body></html>"
    )


if __name__ == "__main__":
    print(c.write("timetable.html", render(c.load())))
