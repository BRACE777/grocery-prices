---
name: Woolworths against Coles
description: An Australian shelf-edge price ticket, printed weekly and seated in a grey plastic rail.
colors:
  aisle: "#e4e8e6"
  aisle-deep: "#d3d9d6"
  rail: "#a9b2ae"
  rail-lip: "#8e9994"
  card: "#ffffff"
  card-ink: "#111315"
  card-soft: "#6b7572"
  card-hair: "#e2e6e4"
  ink: "#111315"
  ink-soft: "#555d5a"
  sign: "#111315"
  sign-ink: "#e9edea"
  wool: "#0f8a3f"
  wool-deep: "#0b6b33"
  coles: "#d8121f"
  coles-deep: "#ad0d18"
  flash: "#ffd400"
  flash-ink: "#141414"
  burst: "#c20d19"
  stamp: "#4c1d95"
  focus: "#1b45c4"
  aisle-dark: "#16191a"
  aisle-deep-dark: "#101213"
  rail-dark: "#333b3d"
  rail-lip-dark: "#454e50"
  ink-dark: "#e9edea"
  ink-soft-dark: "#98a29e"
  sign-dark: "#2b3133"
  focus-dark: "#7fa6ff"
typography:
  display:
    fontFamily: "Barlow Condensed, sans-serif"
    fontSize: "2.1rem"
    fontWeight: 800
    lineHeight: 1
    letterSpacing: "-0.005em"
  price:
    fontFamily: "Barlow Condensed, sans-serif"
    fontSize: "2.9rem"
    fontWeight: 800
    lineHeight: 0.86
    letterSpacing: "-0.025em"
  price-flash-lead:
    fontFamily: "Barlow Condensed, sans-serif"
    fontSize: "3.1rem"
    fontWeight: 800
    lineHeight: 0.85
    letterSpacing: "-0.02em"
  headline:
    fontFamily: "Barlow Condensed, sans-serif"
    fontSize: "1.5rem"
    fontWeight: 600
    lineHeight: 1.05
    letterSpacing: "normal"
  sign:
    fontFamily: "Barlow Condensed, sans-serif"
    fontSize: "1.02rem"
    fontWeight: 700
    lineHeight: 1.4
    letterSpacing: "0.16em"
  title:
    fontFamily: "Barlow Condensed, sans-serif"
    fontSize: "0.88rem"
    fontWeight: 500
    lineHeight: 1.08
    letterSpacing: "normal"
  label:
    fontFamily: "Barlow Condensed, sans-serif"
    fontSize: "0.74rem"
    fontWeight: 700
    lineHeight: 1.4
    letterSpacing: "0.15em"
  stamp:
    fontFamily: "Barlow Condensed, sans-serif"
    fontSize: "0.68rem"
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "0.06em"
  body:
    fontFamily: "Barlow, system-ui, -apple-system, sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: "normal"
    fontFeature: "tabular-nums"
  unit:
    fontFamily: "Barlow, system-ui, sans-serif"
    fontSize: "0.82rem"
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: "normal"
  mono:
    fontFamily: "ui-monospace, Cascadia Mono, monospace"
    fontSize: "0.8rem"
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: "normal"
rounded:
  square: "0"
spacing:
  hair: "0.1rem"
  slot-gap: "0.45rem"
  card-pad: "0.55rem"
  page-gutter: "0.7rem"
  flash-pad: "0.85rem"
  pair-gap: "1rem"
  bay-lead: "1.9rem"
  page-tail: "3.5rem"
components:
  ticket:
    backgroundColor: "{colors.card}"
    textColor: "{colors.card-ink}"
    typography: "{typography.price}"
    rounded: "{rounded.square}"
    padding: "0 {spacing.card-pad}"
    height: "10.6rem"
    width: "22rem"
  ticket-proud:
    backgroundColor: "{colors.card}"
    textColor: "{colors.card-ink}"
    rounded: "{rounded.square}"
  ticket-empty:
    backgroundColor: "{colors.aisle}"
    textColor: "{colors.ink}"
    typography: "{typography.stamp}"
    rounded: "{rounded.square}"
    padding: "{spacing.card-pad}"
    height: "10.6rem"
  ticket-fault:
    backgroundColor: "{colors.card}"
    textColor: "{colors.coles-deep}"
    rounded: "{rounded.square}"
    padding: "{spacing.card-pad}"
    height: "10.6rem"
  ticket-fault-soft:
    backgroundColor: "{colors.card}"
    textColor: "{colors.ink}"
    rounded: "{rounded.square}"
    padding: "{spacing.card-pad}"
    height: "10.6rem"
  flash:
    backgroundColor: "{colors.flash}"
    textColor: "{colors.flash-ink}"
    typography: "{typography.headline}"
    rounded: "{rounded.square}"
    padding: "0.75rem {spacing.flash-pad} 0.8rem"
  flash-lead:
    backgroundColor: "{colors.flash}"
    textColor: "{colors.flash-ink}"
    typography: "{typography.price-flash-lead}"
    rounded: "{rounded.square}"
    padding: "0.95rem 1rem 1rem"
  tag-special:
    backgroundColor: "{colors.flash}"
    textColor: "{colors.flash-ink}"
    typography: "{typography.label}"
    rounded: "{rounded.square}"
    padding: "0.12rem 0.38rem"
  tag-half:
    backgroundColor: "{colors.burst}"
    textColor: "{colors.card}"
    typography: "{typography.label}"
    rounded: "{rounded.square}"
    padding: "0.12rem 0.38rem"
  burst:
    backgroundColor: "{colors.burst}"
    textColor: "{colors.card}"
    typography: "{typography.label}"
    rounded: "{rounded.square}"
    padding: "0.08rem 0.4rem"
  stamp:
    backgroundColor: "transparent"
    textColor: "{colors.stamp}"
    typography: "{typography.stamp}"
    rounded: "{rounded.square}"
    padding: "0.1rem 0.34rem"
  bay-sign:
    backgroundColor: "{colors.sign}"
    textColor: "{colors.sign-ink}"
    typography: "{typography.sign}"
    rounded: "{rounded.square}"
    padding: "0.3rem 0.55rem"
  verdict:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    rounded: "{rounded.square}"
    padding: "0 0 0 0.6rem"
    width: "42ch"
---

# Design System: Woolworths against Coles

## Overview

**Creative North Star: "The Aisle Set Before Opening"**

This is one surface pretending to be furniture. The page is a grey supermarket aisle; each tracked product is a pair of white die-cut price tickets seated side by side in a grey plastic rail, one ticket per chain, and each bay of the list is introduced by a black overhead bay sign. Everything is printed: square corners everywhere, no rounded UI, no gradients, no imagery, and no icons of any kind. Density is high and unapologetic, because the whole week's decision has to survive one phone screen in one hand.

The only element that is not shop signage is the rarity stamp: a violet double-ruled strike saying whether this price is genuinely unusual. It is the app's own voice, inked in a hue that belongs to neither chain and is not the focus ring's blue, and it is the reason the page exists rather than a shelf photo.

Chain identity is colour, never a logo: Woolworths green and Coles red arrive as a 5px printed top edge on every slot. Because red is a chain's name here, red can never also mean "discount" — the special vocabulary is built from the chains' own yellow flash instead. The page carries no JavaScript; every state and every motion is CSS, and the finished, readable state is the element's real state.

**Key Characteristics:**
- Printed-ticket material: white card on grey aisle, square corners, hairline rules
- Heavy condensed grotesque throughout, pack price at ticket scale
- Chain colour as the only identity mark, no logos
- Yellow flash for specials, violet stamp for rarity, red only for Coles or a dead pin
- Motion is stagger-and-seat only, out of `@starting-style`, never required to read the page

## Colors

A print palette: two supermarket house colours, one signage yellow, one inspector's violet, and a long grey-green neutral ramp standing in for plastic, laminate and aisle floor.

### Primary
- **Woolworths Green** (`colors.wool`): the chain edge on every Woolworths slot, and via its deeper tone (`colors.wool-deep`) the chain label and the winning unit-price line inside a Woolworths ticket.
- **Coles Red** (`colors.coles`): the chain edge on every Coles slot, with `colors.coles-deep` for its label ink. Doubles, and only doubles, as the fault colour for a dead pin.

### Secondary
- **Signage Yellow** (`colors.flash`): the special. Whole flash cards on the stock-up board, corner tags on tickets, and the text-selection highlight. Its ink is near-black (`colors.flash-ink`).
- **Burst Red** (`colors.burst`): a hotter red used only as a small burst or tag *inside* a yellow flash, for half price. Never a card background.

### Tertiary
- **Inspector's Violet** (`colors.stamp`): the rarity stamp only. At most one mark per ticket.
- **Ticket Blue** (`colors.focus`, and `colors.focus-dark` in dark mode): the focus ring, and nothing else.

### Neutral
- **Aisle** and **Aisle Deep** (`colors.aisle`, `colors.aisle-deep`): page ground, and the recessed tone behind the scrollbar track and inline code.
- **Rail** and **Rail Lip** (`colors.rail`, `colors.rail-lip`): the 4px rail under every pair plus its shadow lip, the hatch strokes of a not-stocked slot, and note and footer rules.
- **Card / Card Ink / Card Soft / Card Hair**: the printed ticket, its price ink, its size, was and unit ink, and the hairline above the unit line.
- **Ink / Ink Soft**: body ink on the aisle, and the read-metadata line.
- **Sign / Sign Ink**: the bay-sign plate and its reversed type.

### Named Rules

**The Reserved Red Rule.** Red means Coles, or a dead pin. It never encodes discount depth, saving size, or urgency. A half-price Woolworths line is a red burst *on yellow card*, never a red card, because a red Woolworths ticket would arrive wearing its rival's colour.

**The Printed Card Rule.** Dark mode darkens the aisle, the rail, the bay sign and the body ink only. The ticket stays white with its own near-black ink, because printed card does not change colour under different light.

**The Two Inks Rule.** The stamp's violet and the focus ring's blue are separate inks and stay separate. The stamp is content; the ring is the browser talking.

**The No Logo Rule.** Chain identity is carried by colour alone. No retailer logo, wordmark or brand asset appears on any surface.

## Typography

**Display Font:** Barlow Condensed (self-hosted, weights 500/600/700/800)
**Body Font:** Barlow (self-hosted, weights 400/600/700, with `system-ui`, `-apple-system`, `sans-serif`)
**Mono Font:** platform mono (`ui-monospace`, `Cascadia Mono`), inline code only

**Character:** A shelf-ticket grotesque. Condensed and heavy for everything the shopper scans — chain, product, price, sign — and upright Barlow, with tabular figures set on the whole document, for everything read in sentences. All seven faces are served from `docs/fonts/` with `font-display: swap`; there is no font CDN, so a blocked request cannot reskin the page.

### Hierarchy
- **Display** (800, 2.1rem, line-height 1, uppercase): the masthead, two lines, one chain name each.
- **Price** (800, 2.9rem, line-height 0.86): the pack price on a ticket, with a 1.1rem/600 dollar sign set as a superior at the top of the figures.
- **Flash price** (800, 3.1rem lead and 2.1rem paired, line-height 0.85): the price on a stock-up board card.
- **Headline** (600, 1.5rem lead and 1.05rem paired, line-height 1.05, uppercase): the product on a flash card.
- **Sign** (700, 1.02rem, 0.16em, uppercase): bay signs. The board heading runs the same face at 1rem/0.18em, the bay count at 0.82rem/500.
- **Title** (500, 0.88rem, line-height 1.08, uppercase): the product name on a ticket; its pack size continues the same line in card-soft at weight 400.
- **Label** (700, 0.74rem, 0.15em, uppercase): the chain name on a ticket. Special tags sit at 0.74rem/0.08em.
- **Body** (400, 15px, line-height 1.4, tabular figures): notes and footer. The verdict is 1rem/1.35 capped at 42ch; the footer caps at 60ch.
- **Unit** (600, 0.82rem): the mandated unit-price line, in card-soft, switching to the chain's deep tone when that ticket is the cheaper one.
- **Stamp** (700, 0.68rem on a ticket and 0.72rem on a flash, 0.06em, uppercase): the rarity phrase.

### Named Rules

**The Pack Price Leads Rule.** On every ticket the pack price is the largest type in the slot and the unit price sits beneath it, small, as the tiebreaker. Price per unit is never promoted to the headline; it is the number that decides but not the number that is recognised.

**The Condensed Scan Rule.** Anything scanned (chain, product, price, sign, tag, stamp) is uppercase Barlow Condensed. Anything read as prose is upright Barlow, mixed case. There is no third voice.

**The One Figure Style Rule.** `font-variant-numeric: tabular-nums` is set on the document, so two prices in a pair align digit for digit.

## Layout

One centred column, `max-width: 46rem`, with a 0.7rem page gutter and a 3.5rem tail. The page reads masthead, verdict, read metadata, stock-up board, then bay sign and pairs repeated per bay.

The rail is the spatial invariant. Each product is a pair; inside it the slot grid is always two columns of `minmax(0, 22rem)`, centre-justified, with four explicit rows — head, mark, price, unit — and a 0.45rem gap. Every slot spans all four rows and re-declares `grid-template-rows: subgrid`, which is what lands the two pack prices on one baseline no matter how many lines the two product names take. Where subgrid is unsupported, a ticket falls back to a flex column with the price block pushed down by `margin-top: auto`, so the price still bottom-anchors. All three slot types — ticket, not-stocked, fault — carry the same `min-height: 10.6rem`, so a pair never collapses asymmetrically.

Responsive behaviour is intrinsic: there are no width media queries in the build. The cap is on the slot, not the container, so at 1440px the two tickets stop at 22rem each and centre, keeping ticket proportion instead of going landscape; the phone layout is the same two columns, narrowed. The board's two secondary cards are a fixed 1fr 1fr at every width. Vertical rhythm: 1rem between pairs, 1.9rem before a bay sign, 0.6rem after it.

### Named Rules

**The Shared Rows Rule.** A pair's two slots inherit the same four subgrid rows. Never give one slot of a pair its own internal row structure; the compared prices must sit on a shared baseline.

**The Capped Slot Rule.** Widening the viewport adds margin, never ticket width. A ticket's maximum is 22rem.

## Elevation & Depth

Depth is physical and shallow: card lifted off a rail, rail casting a lip. It is not ambient UI elevation. Two devices are structural — the rail's 4px bottom border plus its `0 5px 0 -1px` rail-lip offset (the plastic lip), and the bay sign's flat `0 2px 0` lip in the same ink — and the cards themselves carry a short cast shadow.

### Shadow Vocabulary
- **Seated ticket** (`box-shadow: 0 1px 2px rgba(0,0,0,.17)`): a ticket at rest in the rail.
- **Proud ticket** (`box-shadow: 0 8px 15px rgba(0,0,0,.22), 0 2px 3px rgba(0,0,0,.15)` with `translateY(-10px)`): the cheaper ticket of a pair, standing out of the rail. This is the comparison's answer expressed as height.
- **Flash card** (`box-shadow: 0 2px 4px rgba(0,0,0,.2)`, hover `0 6px 12px rgba(0,0,0,.24)`): a board card.
- **Pressed** (`box-shadow: 0 0 0 rgba(0,0,0,0)` with `translateY(3px)`): a ticket seats flush into the rail when pressed.
- **Fault keyline** (`box-shadow: inset 0 0 0 2px`): a 2px inner rule, Coles red for a dead pin and rail grey for a transient read failure.

### Named Rules

**The Proud Means Cheaper Rule.** Vertical lift inside a pair is reserved for the cheaper unit price. Nothing else in the rail may stand proud, so height stays readable as a verdict.

**The Print Depth Rule.** Shadows are short, dark and downward — card on rail. No glow, no coloured shadow, no blur above 15px.

## Shapes

Square, everywhere: no element in the build sets a border radius. Form language is die-cut rectangles differentiated by edge, not by corner. Every slot is identified by a 5px solid top edge in its chain colour. Interior division is by hairline: a 1px card-hair rule above the unit line, a 1px rail-coloured left rule on a pair's note, a 1px footer rule. A not-stocked slot is the aisle showing through a 45-degree hatch (`repeating-linear-gradient(45deg, rail 0 1px, transparent 1px 6px)`) beneath its chain edge, so the chain's rule is still printed over an empty card. Small rotations read as print registration error rather than decoration: the stamp at -1.4 degrees, a half-price burst at -2.

## Components

### Ticket (signature component)
The printed slot, and the centre of the system. A white card with a 5px chain top edge, spanning the pair's four subgrid rows: head (chain label, special tag, product name), mark (rarity stamp), price (pack price), unit (unit price).
- **Shape:** square, 5px chain-coloured top edge, min-height 10.6rem, max width 22rem
- **Padding:** 0.55rem horizontal throughout, 0.3rem above the chain line, 0.5rem below the unit line
- **States:** rest, seated shadow. `proud`/`best` for the cheaper unit price, lift 10px with the unit line recoloured to the chain's deep tone and suffixed "cheaper". Hover, only under `(hover: hover)`, deepens the lift to 14px, or 17px if proud. `:active` seats it to +3px with no shadow.
- **Head row:** a two-column grid, chain left and special tag right in a column of its own, product name spanning both. The tag owns a column specifically so it can never overprint the chain name.
- **Link:** the whole ticket is an anchor to the retailer's listing, `rel="noreferrer"`, no underline, no visited distinction.

### Flash card
The chains' own yellow special card, used on the stock-up board. Yellow ground, near-black ink, 5px chain top edge, board-scale condensed price. The lead card is full width at a 3.1rem price; the remaining two sit in a 1fr 1fr pair at 2.1rem. Half price appears as a burst-red badge rotated -2 degrees; any other discount appears as plain "N% off" in near-black. The card itself never turns red. Hover lifts 3px, press seats 2px.

### Special tag
A small second card laid on the ticket's top corner, pulled up 5px so it overlaps the chain edge: yellow with near-black ink for a normal special, burst red with white ink for half price. The text is the retailer's own promotion label.

### Rarity stamp
The app's own mark and the one non-retailer element on the page: violet uppercase condensed inside a 2px violet rule, multiplied into the card (`mix-blend-mode: multiply`) and rotated -1.4 degrees, so it reads as an overprinted strike rather than a UI chip. At most one per ticket; on a yellow flash card it rotates -1. It carries a phrase about how unusual the price is, never a discount percentage.

### Bay sign
The overhead aisle sign: a full-width near-black plate with reversed sign ink, a 0.16em-tracked uppercase condensed heading left and a specials count right, sitting on a 2px rail-lip shelf.

### State slots
- **Not stocked:** hatched aisle beneath the chain's 5px edge, uppercase condensed caption ("Woolworths does not stock it"), 85% opacity, bottom-aligned.
- **Dead pin:** white card, Coles-red top edge and 2px inset keyline, coles-deep uppercase headline, with a mixed-case card-soft instruction beneath ("repin it").
- **Transient read failure:** the same card with edge, keyline and ink switched to rail grey and body ink. Quiet grey, deliberately not red.

### Verdict
The answer in the first viewport: one sentence, capped at 42ch, on a 3px left edge in the winning chain's colour, the chain name bold.

### Focus
`:focus-visible` is a 3px focus-blue outline at 3px offset, applied globally. It is the only ring in the system.

### Named Rules

**The Missing Is Not Broken Rule.** A chain that does not stock a line is a grey hatched slot. A pin that no longer resolves is a red fault card. A read that failed this run is a grey fault card. Only the middle one is the reader's job, and only the middle one may be red.

**The Layered Motion Rule.** All seven effects are CSS transitions out of `@starting-style`, inside `prefers-reduced-motion: no-preference`, timed on one stagger step (38ms, multiplied by a per-row index capped at 14) and one easing (`cubic-bezier(.16,1,.3,1)`). The seated state is the element's real state, so a browser that runs none of it shows the finished shop. Sequence within a slot: ticket seats in from the left (420ms, translateX -20px, rotate -1.5deg), then the cheaper ticket rises (520ms, +300ms), then the special tag turns over (rotate 380ms and opacity 260ms, +420ms, from rotate -16deg), then the stamp is struck on (transform 260ms and opacity 200ms linear, +560ms, from scale 1.5). On the board the lead flash is stamped down (520ms, +60ms, from scale 1.07 and -10px) and the other two settle (400ms, 320ms plus 90ms each). Bay signs light through `animation-timeline: view()` over `entry 0%` to `entry 70%` where supported, and are simply lit where not.

## Do's and Don'ts

### Do:
- **Do** lead every price slot with the pack price at display scale (800, 2.9rem) and set the unit price small beneath it as the tiebreaker.
- **Do** identify a chain with colour and colour only, as the 5px top edge of the slot.
- **Do** express a special in the chains' yellow flash vocabulary: yellow card, yellow tag, burst red for half price only.
- **Do** keep the ticket white in dark mode and darken only aisle, rail, sign and body ink.
- **Do** give both slots of a pair the same four subgrid rows and the same 10.6rem minimum, so the two prices share a baseline.
- **Do** reserve vertical lift inside a pair for the cheaper unit price.
- **Do** ship any new effect as a transition out of `@starting-style` under `prefers-reduced-motion: no-preference`, on the existing 38ms step and easing.
- **Do** self-host any new face through `docs/fonts/faces.css`.

### Don't:
- **Don't** use red to mean discount, saving, or urgency. Red is Coles, or a dead pin.
- **Don't** place a retailer logo, wordmark or brand asset anywhere.
- **Don't** paint a transient read failure red; it is grey, because red means the reader has work to do.
- **Don't** round a corner. Nothing in this system carries a radius.
- **Don't** add JavaScript to the page, or make any content reachable only after a transition runs.
- **Don't** stretch a ticket past 22rem on a wide screen; add margin instead.
- **Don't** introduce a third type voice or a fourth accent ink. Violet is the stamp, blue is the focus ring, yellow is the special.
- **Don't** promote price per unit to the headline, and don't fall back to a comparison-dashboard card grid.
