"""The weekly page: an aisle of shelf-edge tickets.

The pack price leads on every ticket, because that is the number already known
by heart, and the mandated unit-price line sits beneath it as the tiebreaker.
The one mark that is not shop signage is the rarity stamp, which says whether
this price is actually unusual for this product. That is the thing a real shelf
ticket cannot tell you.

Motion is one system: the aisle being set before opening. Everything is layered
onto a page that is already finished, so nothing here is the only route to
seeing the content.
"""

from __future__ import annotations

import html
import pathlib

CHAINS = ("woolworths", "coles")
CHAIN_LABEL = {"woolworths": "Woolworths", "coles": "Coles"}

# The typefaces are served from docs/fonts/ rather than a font CDN. Loading
# them from a third party means a blocked or slow request ships the page in the
# platform's own sans, which is a different design from this one. Run
# fetch_fonts.py to refresh the files and these declarations.
FACES = pathlib.Path(__file__).resolve().parent / "docs" / "fonts" / "faces.css"


def font_faces() -> str:
    try:
        return FACES.read_text(encoding="utf-8").strip()
    except OSError:
        # No local faces yet; the page still renders in the fallback stack.
        return ""


def e(value) -> str:
    return html.escape(str(value if value is not None else ""), quote=True)


def money(value) -> str:
    return "" if value is None else f"{value:,.2f}"


CSS = r"""
:root{
  --aisle:#e4e8e6; --aisle-deep:#d3d9d6; --rail:#a9b2ae; --rail-lip:#8e9994;
  --card:#fff; --card-ink:#111315; --card-soft:#6b7572; --card-hair:#e2e6e4;
  --ink:#111315; --ink-soft:#555d5a;
  --wool:#0f8a3f; --wool-deep:#0b6b33;
  --coles:#d8121f; --coles-deep:#ad0d18;
  --flash:#ffd400; --flash-ink:#141414;
  /* Red says Coles. It never says 'discount', or a Woolworths half price
     would arrive wearing its rival's colour. It is only ever the burst
     inside a yellow flash. */
  --burst:#c20d19;
  /* Aisle furniture, so it can darken in dark mode while the printed
     tickets stay white. */
  --sign:#111315; --sign-ink:#e9edea;
  /* Inspector's violet: the app's own voice, not either chain's, and not
     the focus ring's blue. */
  --stamp:#4c1d95; --focus:#1b45c4;
  --ease:cubic-bezier(.16,1,.3,1); --step:38ms;
  color-scheme:light dark;
}
/* The aisle after close. Printed card does not change colour under different
   light, so the tickets stay white and only the aisle around them darkens. */
@media (prefers-color-scheme:dark){
  :root{
    --aisle:#16191a; --aisle-deep:#101213; --rail:#333b3d; --rail-lip:#454e50;
    --ink:#e9edea; --ink-soft:#98a29e;
    --focus:#7fa6ff;
    --sign:#2b3133; --sign-ink:#e9edea;
  }
}
*{box-sizing:border-box}
html{background:var(--aisle)}
body{
  margin:0; background:var(--aisle); color:var(--ink);
  font-family:Barlow,system-ui,-apple-system,sans-serif;
  font-size:15px; line-height:1.4; font-variant-numeric:tabular-nums;
  -webkit-text-size-adjust:100%; overflow-x:hidden;
}
::selection{background:var(--flash); color:var(--flash-ink)}
:focus-visible{outline:3px solid var(--focus); outline-offset:3px}
::-webkit-scrollbar{width:10px}
::-webkit-scrollbar-track{background:var(--aisle-deep)}
::-webkit-scrollbar-thumb{background:var(--rail); border:2px solid var(--aisle-deep)}
main{max-width:46rem; margin:0 auto; padding:0 .7rem 3.5rem}
.cond{font-family:"Barlow Condensed",Barlow,sans-serif}

/* ---------- masthead ---------- */
.masthead{padding:1.7rem .2rem .9rem}
.masthead h1{
  font-family:"Barlow Condensed",sans-serif; font-weight:800; font-size:2.1rem;
  line-height:1; letter-spacing:-.005em; text-transform:uppercase; margin:0;
}
.masthead .when{
  margin:.5rem 0 0; display:flex; flex-wrap:wrap; gap:.1rem .9rem;
  font-weight:500; text-transform:uppercase; letter-spacing:.07em;
  font-size:.82rem; color:var(--ink-soft);
}
.masthead .when b{color:var(--ink); font-weight:700}
/* The answer, in the first viewport, in the winning chain's own colour. */
.verdict{
  margin:.55rem 0 .1rem; font-size:1rem; line-height:1.35; max-width:42ch;
  border-left:3px solid var(--chain); padding-left:.6rem;
}
.verdict[data-chain=woolworths]{--chain:var(--wool)}
.verdict[data-chain=coles]{--chain:var(--coles)}
.verdict b{font-weight:700}
.stale{color:#fff; background:var(--coles); padding:.05rem .4rem; font-weight:700}

/* ---------- the stock-up board ---------- */
.board{margin:.2rem 0 1.5rem}
.board > h2{
  font-family:"Barlow Condensed",sans-serif; font-weight:700; font-size:1rem;
  text-transform:uppercase; letter-spacing:.18em; margin:0 0 .45rem;
  color:var(--ink);
}
.board > h2 + p{margin:-.35rem 0 .6rem; color:var(--ink-soft);
                font-size:.85rem; max-width:52ch}
.board .rest{display:grid; grid-template-columns:1fr 1fr; gap:.5rem;
             margin-top:.5rem}

/* A flash ticket: the yellow card the chains actually hang on a special. */
.flash{
  display:block; text-decoration:none; background:var(--flash);
  color:var(--flash-ink); padding:.75rem .85rem .8rem; position:relative;
  border-top:5px solid var(--chain);
  box-shadow:0 2px 4px rgba(0,0,0,.2);
  transition:transform 140ms var(--ease),box-shadow 140ms var(--ease);
}
.flash[data-chain=woolworths]{--chain:var(--wool)}
.flash[data-chain=coles]{--chain:var(--coles)}
.flash.lead{padding:.95rem 1rem 1rem}
/* Half price is a burst on the yellow card, never a red card. */
.flash .burst{
  display:inline-block; background:var(--burst); color:#fff;
  font-family:"Barlow Condensed",sans-serif; font-weight:700;
  letter-spacing:.06em; text-transform:uppercase; font-size:.82rem;
  padding:.08rem .4rem; transform:rotate(-2deg);
}
.flash .chain{
  font-family:"Barlow Condensed",sans-serif; font-weight:700; font-size:.76rem;
  letter-spacing:.16em; text-transform:uppercase; display:block;
}
.flash .what{
  font-family:"Barlow Condensed",sans-serif; font-weight:600; line-height:1.05;
  text-transform:uppercase; display:block; margin:.15rem 0 .3rem;
  font-size:1.05rem;
}
.flash.lead .what{font-size:1.5rem}
.flash .row{display:flex; align-items:baseline; gap:.45rem; flex-wrap:wrap}
.flash .now{
  font-family:"Barlow Condensed",sans-serif; font-weight:800; line-height:.85;
  font-size:2.1rem; letter-spacing:-.02em;
}
.flash.lead .now{font-size:3.1rem}
.flash .was{font-weight:600; text-decoration:line-through;
            text-decoration-thickness:1px; opacity:.88}
.flash .cut{font-weight:700; text-transform:uppercase; letter-spacing:.06em;
            font-size:.82rem}
.flash:active{transform:translateY(2px); box-shadow:0 1px 2px rgba(0,0,0,.22)}

/* ---------- bay sign ---------- */
.bay{
  display:flex; align-items:baseline; justify-content:space-between; gap:1em;
  margin:1.9rem 0 .6rem; padding:.3rem .55rem;
  background:var(--sign); color:var(--sign-ink);
  box-shadow:0 2px 0 var(--rail-lip);
}
.bay h2{
  font-family:"Barlow Condensed",sans-serif; font-weight:700; font-size:1.02rem;
  text-transform:uppercase; letter-spacing:.16em; margin:0;
}
.bay .count{
  font-family:"Barlow Condensed",sans-serif; font-weight:500; font-size:.82rem;
  letter-spacing:.08em; text-transform:uppercase; opacity:.85;
  white-space:nowrap;
}

/* ---------- the rail ---------- */
.bayrows{display:flex; flex-direction:column; gap:1rem}
.pair{margin:0}
.slots{
  display:grid; gap:.45rem;
  /* Capped rather than stretched, so a ticket keeps a ticket's proportion on a
     wide screen instead of going landscape. */
  grid-template-columns:repeat(2,minmax(0,22rem));
  justify-content:center;
  /* head / mark / price / unit. Both tickets inherit these four rows, which is
     what puts the two prices on the same line. */
  grid-template-rows:auto auto auto auto;
  align-items:stretch;
  padding-bottom:.45rem;
  border-bottom:4px solid var(--rail);
  box-shadow:0 5px 0 -1px var(--rail-lip);
}
.pair .note{
  margin:.5rem .1rem 0; font-size:.84rem; color:var(--ink-soft);
  padding-left:.7rem; border-left:1px solid var(--rail);
}

/* ---------- a ticket ---------- */
.ticket,.empty,.fault{
  grid-row:span 4;
  display:grid; grid-template-rows:subgrid;
}
.ticket{
  min-height:10.6rem; position:relative;
  background:var(--card); color:var(--card-ink); text-decoration:none;
  border-top:5px solid var(--chain);
  box-shadow:0 1px 2px rgba(0,0,0,.17);
  transition:transform 150ms var(--ease),box-shadow 150ms var(--ease);
}
/* Without subgrid the rows do not lock, so fall back to bottom-anchoring the
   price as before rather than leaving the layout broken. */
@supports not (grid-template-rows:subgrid){
  .ticket{display:flex; flex-direction:column}
  .ticket .t-price{margin-top:auto}
}
.t-head{align-self:start}
.t-mark{align-self:end}
.t-price{align-self:end}
.t-unit{align-self:end}
.ticket[data-chain=woolworths]{--chain:var(--wool); --chain-deep:var(--wool-deep)}
.ticket[data-chain=coles]{--chain:var(--coles); --chain-deep:var(--coles-deep)}
.ticket .chain{
  font-family:"Barlow Condensed",sans-serif; font-weight:700; font-size:.74rem;
  letter-spacing:.15em; text-transform:uppercase; color:var(--chain-deep);
  padding:.3rem .55rem 0;
}
.ticket .name{
  font-family:"Barlow Condensed",sans-serif; font-weight:500; font-size:.88rem;
  line-height:1.08; text-transform:uppercase; padding:.1rem .55rem .3rem;
}
.ticket .size{color:var(--card-soft); font-weight:400}

/* The pack price leads. It is the number the shopper already knows. */
.ticket .price{
  padding:0 .55rem; display:flex; align-items:baseline; gap:.08rem;
}
.ticket .price .cur{
  font-family:"Barlow Condensed",sans-serif; font-weight:600; font-size:1.1rem;
  align-self:flex-start; margin-top:.16rem;
}
.ticket .price .n{
  font-family:"Barlow Condensed",sans-serif; font-weight:800; font-size:2.9rem;
  line-height:.86; letter-spacing:-.025em;
}
.ticket .was{
  padding:.05rem .55rem 0; font-size:.8rem; color:var(--card-soft);
}
.ticket .was s{text-decoration-thickness:1px}
/* The legally mandated unit line, small, and the tiebreaker. */
.ticket .t-unit{
  padding:.2rem .55rem .5rem; font-size:.82rem; font-weight:600;
  color:var(--card-soft); border-top:1px solid var(--card-hair);
  margin-top:.3rem;
}
.ticket.best .t-unit{color:var(--chain-deep)}
.ticket .t-unit b{font-weight:700}

/* The head row: chain on the left, promo flag on the right, product name
   across both. The flag used to be absolutely positioned and overprinted the
   chain name, so it now owns a column of its own. */
.t-head{
  display:grid; grid-template-columns:1fr auto; align-items:start;
  column-gap:.4rem;
}
.t-head .name{grid-column:1/-1}
/* The special flash, a second card laid on the ticket's top corner. */
.ticket .tag{
  grid-column:2; align-self:start; margin-top:-5px;
  background:var(--flash);
  color:var(--flash-ink); font-family:"Barlow Condensed",sans-serif;
  font-weight:700; font-size:.74rem; letter-spacing:.08em;
  text-transform:uppercase; padding:.12rem .38rem; white-space:nowrap;
  transform-origin:top right;
}
.ticket .tag.half{background:var(--burst); color:#fff}

/* The app's own mark, struck on the ticket rather than printed by the shop.
   Violet ink so it is neither chain's colour and not the focus ring's blue; a
   double rule offset by a hair and multiplied into the card so it reads as an
   overprinted strike rather than a crisp UI chip. */
.stamp{
  display:inline-block; justify-self:start;
  font-family:"Barlow Condensed",sans-serif; font-weight:700; font-size:.72rem;
  letter-spacing:.09em; text-transform:uppercase; color:var(--stamp);
  padding:.1rem .34rem; border:2px solid var(--stamp);
  box-shadow:1.5px 1.5px 0 -0.5px color-mix(in srgb,var(--stamp) 35%,transparent);
  mix-blend-mode:multiply;
  transform:rotate(-1.4deg); transform-origin:left center;
}
@supports not (color: color-mix(in srgb,red 50%,blue)){
  .stamp{box-shadow:1.5px 1.5px 0 -0.5px var(--stamp)}
}
.ticket .stamp{
  margin:0 .55rem .45rem; font-size:.68rem; line-height:1.2;
  letter-spacing:.06em;
}
/* On the board the card is already yellow, so the strike sits on that. */
.flash .stamp{margin:.45rem 0 0; transform:rotate(-1deg)}

/* The cheaper ticket stands proud of its neighbour in the rail. */
.ticket.proud{
  transform:translateY(-10px);
  box-shadow:0 8px 15px rgba(0,0,0,.22),0 2px 3px rgba(0,0,0,.15);
}
@media (hover:hover){
  .ticket:hover{transform:translateY(-14px)}
  .ticket.proud:hover{transform:translateY(-17px)}
  .flash:hover{transform:translateY(-3px); box-shadow:0 6px 12px rgba(0,0,0,.24)}
}
/* Pressed tickets seat into the rail. */
.ticket:active{transform:translateY(3px); box-shadow:0 0 0 rgba(0,0,0,0)}
.ticket.proud:active{transform:translateY(-4px)}

/* An empty slot: this chain does not stock the line. */
.empty[data-chain=woolworths]{--chain:var(--wool)}
.empty[data-chain=coles]{--chain:var(--coles)}
.empty{
  min-height:10.6rem; align-content:end; padding:.55rem;
  border-top:5px solid var(--chain);
  background-image:repeating-linear-gradient(45deg,
    var(--rail) 0 1px,transparent 1px 6px);
  font-family:"Barlow Condensed",sans-serif; font-weight:600; font-size:.82rem;
  text-transform:uppercase; letter-spacing:.09em; color:var(--ink);
  opacity:.85;
}
/* A broken pin: the one state that is the reader's job to fix. */
.fault{
  min-height:10.6rem; align-content:end; gap:.2rem; padding:.55rem;
  background:var(--card); border-top:5px solid var(--coles);
  box-shadow:inset 0 0 0 2px var(--coles);
  font-family:"Barlow Condensed",sans-serif; font-weight:700; font-size:.82rem;
  text-transform:uppercase; letter-spacing:.07em; color:var(--coles-deep);
}
.fault span{font-family:Barlow,sans-serif; font-weight:400; text-transform:none;
            letter-spacing:0; color:var(--card-soft)}
/* A read that failed this run, rather than a pin that needs fixing. Red is
   reserved for work the reader has to do. */
.fault.soft{
  border-top-color:var(--rail); box-shadow:inset 0 0 0 2px var(--rail);
  color:var(--ink);
}

/* ---------- footer ---------- */
footer{
  margin-top:1.4rem; padding-top:1rem; border-top:1px solid var(--rail);
  color:var(--ink-soft); font-size:.84rem;
}
footer p{margin:.4rem 0; max-width:60ch}
footer code{
  font-family:ui-monospace,"Cascadia Mono",monospace; font-size:.8rem;
  color:var(--ink); background:var(--aisle-deep); padding:.05rem .25rem;
}

/* ---------- motion: the aisle being set before opening ----------
   Every effect below is layered onto the finished page above. The transitions
   run out of @starting-style, so the seated, readable state is the element's
   real state and a browser that runs none of this still shows the shop. */
@media (prefers-reduced-motion:no-preference){
  .ticket,.empty,.fault{
    transition:
      transform 420ms var(--ease) calc(var(--i,0)*var(--step)),
      rotate 420ms var(--ease) calc(var(--i,0)*var(--step)),
      box-shadow 420ms var(--ease) calc(var(--i,0)*var(--step));
  }
  /* Tickets are pushed into the rail channel, tilting as they seat. */
  @starting-style{
    .ticket,.empty,.fault{transform:translateX(-20px); rotate:-1.5deg}
    .ticket.proud{transform:translateX(-20px) translateY(0)}
  }
  /* The cheaper ticket rises only after both are seated, so the reader sees
     the comparison resolve rather than arriving already decided. */
  .ticket.proud{
    transition:
      transform 520ms var(--ease) calc(var(--i,0)*var(--step) + 300ms),
      rotate 420ms var(--ease) calc(var(--i,0)*var(--step)),
      box-shadow 520ms var(--ease) calc(var(--i,0)*var(--step) + 300ms);
  }
  /* The flash turns over onto the ticket, as a second card laid on top. */
  .ticket .tag{
    transition:rotate 380ms var(--ease) calc(var(--i,0)*var(--step) + 420ms),
               opacity 260ms var(--ease) calc(var(--i,0)*var(--step) + 420ms);
  }
  @starting-style{.ticket .tag{rotate:-16deg; opacity:0}}
  /* The stamp is struck on afterwards. */
  .stamp{
    transition:transform 260ms var(--ease) calc(var(--i,0)*var(--step) + 560ms),
               opacity 200ms linear calc(var(--i,0)*var(--step) + 560ms);
  }
  @starting-style{
    .stamp{transform:rotate(-1.4deg) scale(1.5); opacity:0}
  }
  /* Focal moment: the lead flash ticket is stamped down on the board. */
  .flash.lead{
    transition:transform 520ms var(--ease) 60ms,
               box-shadow 520ms var(--ease) 60ms;
  }
  @starting-style{
    .flash.lead{transform:scale(1.07) translateY(-10px);
                box-shadow:0 18px 30px rgba(0,0,0,.28)}
  }
  .board .rest .flash{
    transition:transform 400ms var(--ease) calc(320ms + var(--j,0)*90ms);
  }
  @starting-style{.board .rest .flash{transform:translateY(-14px)}}
  /* Bay signs light as the aisle is walked. Scroll-linked where supported,
     and simply lit where not. */
  @supports (animation-timeline:view()){
    .bay{
      animation:sign linear both;
      animation-timeline:view();
      animation-range:entry 0% entry 70%;
    }
    @keyframes sign{
      from{background:var(--rail); color:var(--sign-ink); box-shadow:none}
      to{background:var(--sign); color:var(--sign-ink);
         box-shadow:0 2px 0 var(--rail-lip)}
    }
  }
}
"""


def _ticket(row: dict, chain: str, index: int) -> str:
    offer = row["offers"].get(chain)
    label = CHAIN_LABEL[chain]
    if offer is None:
        return (
            f'<div class="empty" data-chain="{chain}" style="--i:{index}">'
            f"{label} does not stock it</div>"
        )
    if offer["error"]:
        # Only a 404 means the pin itself is dead. Everything else is the shop
        # refusing this run, which is not something to go and fix.
        dead = "404" in offer["error"] or "not found" in offer["error"].lower()
        headline = f"{label} pin is dead" if dead else f"{label} would not answer"
        detail = (
            "this product no longer exists, repin it"
            if dead
            else "read failed twice this run, it should return next week"
        )
        klass = "fault" if dead else "fault soft"
        return (
            f'<div class="{klass}" data-chain="{chain}" style="--i:{index}">'
            f"{headline}<span>{detail}</span></div>"
        )

    classes = ["ticket"]
    if row.get("winner") == chain:
        classes += ["proud", "best"]

    tag = ""
    if offer["onSpecial"]:
        text = offer["specialLabel"] or "Special"
        half = " half" if "1/2" in text or "half" in text.lower() else ""
        tag = f'<span class="tag{half}">{e(text)}</span>'

    was = ""
    if offer["wasPrice"]:
        was = (
            f'<span class="was">was <s>${money(offer["wasPrice"])}</s>'
            f'{f" · save ${money(offer['saving'])}" if offer.get("saving") else ""}'
            f"</span>"
        )

    stamp = ""
    if offer.get("notable") and offer.get("rarityPhrase"):
        stamp = f'<span class="stamp">{e(offer["rarityPhrase"])}</span>'

    if offer["comparablePrice"] is not None:
        unit = f'${money(offer["comparablePrice"])}{e(offer["comparableLabel"])}'
        if row.get("winner") == chain:
            unit += " · <b>cheaper</b>"
    else:
        unit = "no unit price"
    size = f' <span class="size">{e(offer["size"])}</span>' if offer["size"] else ""

    # Four rows, always, even when a row is empty. Both tickets in a pair share
    # the rail's rows, which is what lands the two pack prices on one baseline.
    return (
        f'<a class="{" ".join(classes)}" data-chain="{chain}" style="--i:{index}" '
        f'href="{e(offer["url"])}" rel="noreferrer">'
        f'<span class="t-head"><span class="chain">{label}</span>{tag}'
        f'<span class="name">{e(offer["name"] or row["title"])}{size}</span></span>'
        f'<span class="t-mark">{stamp}</span>'
        f'<span class="t-price"><span class="price">'
        f'<span class="cur">$</span>'
        f'<span class="n">{money(offer["price"])}</span></span>{was}</span>'
        f'<span class="t-unit">{unit}</span></a>'
    )


def _flash(entry: dict, lead: bool, position: int) -> str:
    offer = entry["offer"]
    text = (offer["specialLabel"] or "").lower()
    klass = "flash lead" if lead else "flash"
    was = (
        f'<span class="was">${money(offer["wasPrice"])}</span>'
        if offer["wasPrice"]
        else ""
    )
    # Half price is a red burst on the yellow card. The card itself never turns
    # red, because red is how the page says Coles.
    burst = ""
    if "1/2" in text or "half" in text:
        burst = '<span class="burst">Half price</span>'
    elif offer.get("savingPercent"):
        burst = f'<span class="cut">{offer["savingPercent"]}% off</span>'
    return (
        f'<a class="{klass}" data-chain="{entry["chain"]}" style="--j:{position}" '
        f'href="{e(offer["url"])}" rel="noreferrer">'
        f'<span class="chain">{CHAIN_LABEL[entry["chain"]]}</span>'
        f'<span class="what">{e(entry["title"])}</span>'
        f'<span class="row"><span class="now">${money(offer["price"])}</span>'
        f"{was}{burst}</span>"
        f'<span class="stamp rare">{e(entry["phrase"])}</span></a>'
    )


def page(payload: dict) -> str:
    rows = payload["rows"]
    offers = [o for r in rows for o in r["offers"].values()]
    specials = sum(1 for o in offers if o.get("onSpecial"))
    failures = sum(1 for o in offers if o.get("error"))
    wins = {c: sum(1 for r in rows if r.get("winner") == c) for c in CHAINS}
    comparable = sum(1 for r in rows if len(r["offers"]) == 2)
    board = payload.get("stockUp") or []

    categories = {c["id"]: c["label"] for c in payload["categories"]}
    order = [c["id"] for c in payload["categories"]]

    parts: list[str] = ['<main>']

    parts.append('<div class="masthead"><h1>Woolworths<br>against Coles</h1>')

    # The page has to answer its own question where the reader lands, not ask
    # them to subtract two counts at the foot of sixteen screens.
    lead, trail = sorted(CHAINS, key=lambda c: wins[c], reverse=True)
    if not comparable:
        verdict = (
            "Nothing on the list is stocked by both shops, so there is no "
            "comparison to make this week."
        )
    elif wins[lead] == wins[trail]:
        verdict = (
            f"Honours are even this week, {wins[lead]} lines each. "
            f"Go by what is on special."
        )
    else:
        verdict = (
            f"<b>{CHAIN_LABEL[lead]}</b> is cheaper on "
            f"<b>{wins[lead]}</b> of the {comparable} lines you can compare, "
            f"{CHAIN_LABEL[trail]} on {wins[trail]}."
        )
    parts.append(f'<p class="verdict" data-chain="{lead}">{verdict}</p>')

    parts.append('<p class="when">')
    parts.append(f'<span>Read <b>{e(payload["generatedLabel"])}</b></span>')
    parts.append(f'<span><b>{specials}</b> of {len(offers)} prices on special</span>')
    if failures:
        parts.append(f'<span class="stale">{failures} could not be read</span>')
    parts.append("</p></div>")

    if board:
        parts.append('<section class="board">')
        parts.append("<h2>Worth stocking up on</h2>")
        parts.append(
            "<p>Ranked by how unusual the price is over the last three months, "
            "not by the size of the discount.</p>"
        )
        parts.append(_flash(board[0], lead=True, position=0))
        if len(board) > 1:
            parts.append('<div class="rest">')
            for position, entry in enumerate(board[1:], start=1):
                parts.append(_flash(entry, lead=False, position=position))
            parts.append("</div>")
        parts.append("</section>")

    index = 0
    for category in order:
        in_category = [r for r in rows if r["category"] == category]
        if not in_category:
            continue
        count = sum(
            1 for r in in_category for o in r["offers"].values() if o.get("onSpecial")
        )
        tail = f"{count} on special" if count else "nothing on special"
        parts.append(
            f'<div class="bay"><h2>{e(categories[category])}</h2>'
            f'<span class="count">{tail}</span></div>'
        )
        parts.append('<div class="bayrows">')
        for row in in_category:
            index = min(index + 1, 14)
            slots = "".join(_ticket(row, chain, index) for chain in CHAINS)
            note = f'<p class="note">{e(row["note"])}</p>' if row["note"] else ""
            parts.append(f'<div class="pair"><div class="slots">{slots}</div>{note}</div>')
        parts.append("</div>")

    parts.append("<footer>")
    parts.append(
        f"<p>{len(rows)} tracked products. Standard shelf prices read from each "
        f"chain's own listing. No Everyday Rewards or Flybuys member pricing, "
        f"which neither chain publishes without signing in, and in-store "
        f"prices may differ from online.</p>"
    )
    parts.append(
        "<p>Cheaper is decided on price per unit, not the pack price, so a "
        "bigger pack can win while costing more.</p>"
    )
    if payload.get("historyProblem"):
        parts.append(
            "<p>Price history was unavailable this run, so no rarity marks "
            "are shown.</p>"
        )
    parts.append(
        "<p>Add a product with <code>python add_item.py</code> and the web "
        "address of that product at either shop.</p>"
    )
    parts.append("</footer></main>")

    return (
        "<!doctype html><html lang=en-AU><head><meta charset=utf-8>"
        '<meta name=viewport content="width=device-width,initial-scale=1">'
        '<meta name=color-scheme content="light dark">'
        "<title>Woolworths against Coles</title>"
        f"<style>{font_faces()}{CSS}</style></head><body>"
        f'{"".join(parts)}</body></html>'
    )
