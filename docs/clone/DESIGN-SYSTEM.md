# Partake → JJW Design System

Ground truth measured from `partakefoods.com` live DOM (`getComputedStyle`, 1280px viewport)
plus their 30 downloaded CSS files in `docs/clone/raw/css/`.

Their theme: `Partake (hasmerit.co)` — a **Shopify Dawn derivative**.
Ours: **Dawn 16.0.0**. Same base, same class names, same section architecture.
That is why this is a transplant and not a re-implementation.

Where the Next.js clone at `C:\Users\krish\Desktop\test opencode` disagrees with this
file, **this file wins** — it is measured off the live site.

---

## 1 · Colour

### Partake's raw palette (`assets/theme-styles.css` `:root`)

| Their token | Value | Role |
|---|---|---|
| `--color-beige` | `#FFF6EB` | page canvas |
| `--color-blue-1` | `#00559B` | brand ink — every heading + body |
| `--color-blue-2` | `#82D8E7` | pale product-card field |
| `--color-magenta-1` | `#BE008B` | primary CTA |
| `--custom-light-blue` | `#009EDE` | header pills, Find-Us band |
| `--custom-black` | `#181B48` | button shadow layer |
| `--custom-orange` / `--custom-dark-orange` | `#FFCD78` / `#FF7700` | marquee bar / accent |
| `--custom-green` / `--custom-dark-green` | `#C2E5E2` / `#40BCB5` | hero text-shadow / accent |
| `--custom-pink` / `--custom-dark-pink` | `#EAACD2` / `#BE008B` | pair |
| `--custom-yellow` / `--custom-dark-yellow` | `#FFEBC1` / `#FFB600` | pair |

### JJW mapping — use these, never the Partake hexes

| Role | Partake | **JJW** | JJW token |
|---|---|---|---|
| Canvas | `#FFF6EB` | `#FFF6EB` | `--jjw-cream` *(identical)* |
| Brand ink | `#00559B` | `#1A2F5E` | `--jjw-ink` |
| Pale card field | `#82D8E7` | `#9FDBFF` | `--jjw-light-blue` |
| Primary CTA | `#BE008B` | `#E5377E` | `--jjw-pink` |
| Pill / band | `#009EDE` | `#0F7DAF` | `--jjw-blue` |
| Button shadow | `#181B48` | `#0E1B3A` | `--jjw-ink-deep` *(add)* |
| Marquee bar | `#FFCD78` | `#FFD94C` | `--jjw-yellow` |
| Headline shadow | `#C2E5E2` | `#D3F3DE` | `--jjw-green-bg` |
| Pairs (bg / deep) | — | `#FFD7E6`/`#E5377E`, `#FFE9C2`/`#F6A313`, `#C9E8F7`/`#0F7DAF`, `#D3F3DE`/`#2FA85E`, `#E4DCFF`/`#6E55D6` | pink, gold, blue, green, purple |

### Colour schemes — set these in `config/settings_data.json`

Dawn drives everything through `color-scheme-N`. Partake's five, remapped:

| Scheme | background | text | button | button label | shadow | used by |
|---|---|---|---|---|---|---|
| 1 | `#FFF6EB` | `#1A2F5E` | `#1A2F5E` | `#FFF6EB` | `#1A2F5E` | page default, featured collection, rich text bg |
| 2 | `#1A2F5E` | `#FFF6EB` | `#C9E8F7` | `#1A2F5E` | `#C9E8F7` | product cards, footer |
| 3 | `#E5377E` | `#FFF6EB` | `#FFFFFF` | `#1A2F5E` | `#0E1B3A` | badges, split-content panel |
| 4 | `#0F7DAF` | `#FFF6EB` | `#FFFFFF` | `#1A2F5E` | `#0E1B3A` | Find-Us band |
| 5 | `#FFF6EB` | `#E5377E` | `#E5377E` | `#FFF6EB` | `#0E1B3A` | rich-text statement |

---

## 2 · Type

Partake's three faces are commercial licences we cannot ship. Substitutions:

| Their face | Role | **Ours** | Already loaded? |
|---|---|---|---|
| `Bunch-Bold` | headings | **Baloo 2** 800 | yes — Google Fonts `@import` |
| `Toroka-CondensedBold` | subheads, buttons, nav, captions | **Big Shoulders Display** 700 | yes — Google Fonts |
| `Toroka-Black` | product card titles | **Big Shoulders Display** 900 | add weight 900 |
| `Gilroy-Medium` | body | **Sofia Pro Soft** Medium | yes — `assets/SofiaProSoft-Medium.otf` |

### Scale — the single most important fix

```css
.hxxl { font-size: min(6vw, 106px); line-height: 1; letter-spacing: 0.6px; }
@media (max-width: 749px) { .hxxl { font-size: 10vw; } }
```

At 1280px that computes to **76.8px**. Our `--jjw-display-size` capped at **32px** — this is
why the site reads nothing like theirs. `.jjw-hxxl` is already correct (`min(6vw, 96px)`);
the sections simply don't use it.

Hero headline overrides to `16vw / line-height .9` below 750px.

Other measured values:

```css
--font-size-27: clamp(16px, 4.2vw, 27px);   /* buttons, links, body-large */
--font-size-24: clamp(14px, 3.2vw, 20px);
a { font-family: <condensed>; text-transform: uppercase; letter-spacing: .05em;
    font-size: clamp(16px, 4.2vw, 27px); text-decoration: none; }
```

Body copy: `27px / line-height 1.3` in split-content; `16px / 1.8` default.

---

## 3 · The blob button — Partake's signature element

Two stacked layers inside `.button--wrapper`, both clipped to the same SVG path.
The shadow layer sits offset and slides to zero on hover.

```html
<div class="button--wrapper">
  <div class="button--bg"></div>
  <a class="button button--primary">Label</a>
</div>
```

```css
.button--wrapper { position: relative; display: inline-block; }
.button--bg {
  position: absolute; inset: 0; z-index: 1;
  background: <shadow colour>;
  transform: translate(6px, 6px);
  clip-path: url(#partake-shape-clip);
}
.button--wrapper .button {
  position: relative; z-index: 2;
  min-height: 6rem; padding: 2rem; width: 100%;
  display: flex; align-items: center; justify-content: center;
  font-size: var(--font-size-27); line-height: 1;
  clip-path: url(#partake-shape-clip);
  transition: transform .2s cubic-bezier(.4,0,.2,1);
}
.button--wrapper:hover .button--bg {
  transform: translate(0); transition: transform .3s cubic-bezier(.4,0,.2,1);
}
.button::before, .button::after { display: none !important; }  /* kill Dawn's own */
```

Measured button variants:

| Variant | surface | shadow layer | type |
|---|---|---|---|
| `.button--primary` | `#BE008B` → **`#E5377E`** | `#611055` → **`#7A1240`** | 27px condensed, `#FFF6EB`, ls 1px |
| `.button--secondary` | `#00559B` → **`#1A2F5E`** | `#181B48` → **`#0E1B3A`** | 22px condensed, `#FFF6EB`, ls 1px |

Header pills use the same trick at a **4px** offset, not 6px.

### The clip path — goes in `layout/theme.liquid`

We already ship `#jjw-blob`. Partake's exact path, for reference —
a soft slightly-irregular rounded rectangle, `clipPathUnits="objectBoundingBox"`:

```
M276.099 61.423L10.521 64.37C4.734 64.434 0 60.582 0 55.807V8.56508C0 3.78408
4.74299 -0.0710076 10.537 0.000992371L276.115 3.27602C281.787 3.34602 286.341
7.15898 286.341 11.84V52.859C286.341 57.544 281.778 61.359 276.099 61.423Z
```
with `transform="scale(0.0034843206,0.015384615)"`.

Always pair with an `@supports not (clip-path: url(#…))` fallback to `border-radius`.

---

## 4 · Product card

```css
.card.card--card            { background: var(--product-bg-color, <pale>); border-radius: 20px;
                              display: flex; flex-direction: column; text-align: center;
                              transition: transform .2s var(--ease), box-shadow .2s var(--ease); }
.card__media                { border-radius: 20px 20px 0 0; }
.card__media .media img     { object-fit: contain !important; }   /* PNG on colour, not cropped */
.card__information          { display: flex; flex-direction: column;
                              align-items: center; justify-content: center; padding: 17px 10px; }
.card__heading a            { font-family: <condensed 900>; font-size: clamp(3.2rem, 4.5vw, 40px);
                              line-height: 1; text-transform: none; letter-spacing: 0;
                              color: var(--product-fg-color, <ink>); margin-block-end: .5rem; }
.card-information .caption-with-letter-spacing
                            { font-family: <condensed 700>; font-size: clamp(.75rem, 4vw, 25px);
                              letter-spacing: .05em; text-transform: uppercase;
                              color: var(--product-fg-color, <ink>); }
.card-information .price    { display: none; }                    /* no price on cards */

@media (hover: hover) and (prefers-reduced-motion: no-preference) {
  .card-wrapper:hover .card--card {
    transform: translateY(-8px) rotate(3deg);
    box-shadow: 6px 6px 0 var(--product-fg-color, <ink>) !important;
  }
}
```

Mobile: card title drops to `22px`, caption to `14px`, radius halves.

**`--product-bg-color` / `--product-fg-color` are set per product.** That is how each cookie
gets its own pastel field with matching type. For us: one colour pair per character —
Jevika, Joy, Brutus, Minku, Pinki — from the five JJW pairs in §1.

---

## 5 · Marquee

```css
.marquee          { position: relative; width: 100%; overflow: hidden; white-space: nowrap; }
.marquee__wrapper { display: flex; width: max-content;
                    animation: marquee 24s linear infinite; }
.marquee__content { display: flex; align-items: center; gap: 3rem;
                    flex-shrink: 0; padding-right: 3rem; }
.marquee__text    { font-family: <condensed>; text-transform: uppercase; letter-spacing: .05em; }
.marquee:hover .marquee__wrapper { animation-play-state: paused; }
@keyframes marquee { from { transform: translate(0); } to { transform: translate(-50%); } }
```

Content is repeated **4×** so `-50%` loops seamlessly. Sizes: small `1.5rem`,
medium `clamp(1.5rem, 4vw, 32px)`, large `3rem`, x-large `3.25rem`.
`--slow` 60s, `--fast` 8s. Bar: bg `#FFCD78` → **`#FFD94C`**, padding `4px 0 8px`.
Logo variant (`.marquee__image`) hovers `rotate(5deg)` + `8px 8px 0` hard shadow.

---

## 6 · Header

- `sticky-header.header-wrapper` — `position: fixed`, `z-index: 9999`, height **124px**,
  background **transparent**, `transition: background-color .3s`.
  Goes solid `#FFF6EB` only when a menu is open (`:has(.mega-menu[open])`).
- `pointer-events: none` on `.header`, re-enabled on every interactive child — lets the hero
  photo sit fully under a transparent bar.
- `header.page-width` — `display: grid`, columns `logo | inline-menu | icons`, padding `1vw 1.5vw`.
- Logo hover: `transform: translate(-10px, -10px)`, `.3s cubic-bezier(.4,0,.2,1)`.
- Search pill: `#009EDE` → **`#0F7DAF`**, radius `7.5px`, `box-shadow: 4px 4px 0 <ink>` → `0` on hover.
- Account + cart icons `display: none` on desktop.
- Scrollbars hidden globally (`scrollbar-width: none` + `::-webkit-scrollbar { display: none }`).

---

## 7 · Scroll animation

Dawn's own — we already ship `animations.js` + `animations.css`. Just add the classes:

- `.scroll-trigger.animate--slide-in` → enters from `translateX(-50px)`
- `.scroll-trigger.animate--fade-in`

Enable "reveal on scroll" in theme settings. No GSAP needed for anything except §8.

---

## 8 · Sticky scroll section (`falling-cookies`)

The one section with no Dawn equivalent. Structure:

```css
.falling-cookies-wrapper { height: 150vh; position: relative; background: #fff6eb; }
#fallingCookies-<id>     { position: sticky; top: 0; height: 150vh; overflow: hidden;
                           display: flex; align-items: center; justify-content: center; }
.cookie-stack-container  { background: url(<counter>.png) bottom center / contain no-repeat; }
.cookie-stack-container::before { /* cream → transparent gradient veil, top 0→40% */ }
.cookie   { position: absolute; width: var(--cookie-size, 26vw); opacity: 0; }
.badge-icon { position: absolute; opacity: 0; z-index: 7; transform-origin: center; }
```

Items start `opacity: 0` and are driven by scroll progress within the sticky viewport.
Mobile collapses the wrapper to `97.5vh` and doubles `--cookie-size`.

**Our version:** falling character tees / stickers over a shelf, same mechanic.
Mark it optional — build it last, after the other twelve read correctly.

---

## 9 · Page topology — homepage, in order

Measured heights at 1280px. Document height 6381px.

| # | Section | H | Field | Notes |
|---|---|---|---|---|
| 0 | header | fixed | transparent | overlays hero |
| 1 | stickers ×2 | 0 | — | floating decorative, app-driven, `z-index: 100` |
| 2 | **image-banner** (hero) | 720 | photo | `100vh`; `.hxxl` + hard text-shadow; one button |
| 3 | **marquee** | 51 | `#FFCD78` | 3 words + bullets, ×4 |
| 4 | **featured-collection** | 1047 | `#FFF6EB` | centred `.hxxl`, 4-col slider, round arrows, `n/11` counter, CTA |
| 5 | **find-us** | 707 | `#009EDE` | radius 40px, centred `.hxxl`, logo marquee (180px), CTA |
| 6 | **falling-cookies** | 1080 | `#FFF6EB` | sticky 150vh, §8 |
| 7 | **split-content** | 660 | `#BE008B` panel on `#FFF6EB` | radius 20px, `align-items: flex-end`, image + badges left, copy right |
| 8 | **focus-carousel** | 1019 | — | 3 stacked cards, centre full / sides `scale(.7)`, per-slide colour + `8px 8px 0` shadow, image dots 200px |
| 9 | **rich-text** | 173 | `#FFF6EB` | scheme-5, centred statement |
| 10 | **marquee 2** | 60 | `#FFCD78` | |
| 11 | **social-icons** | 152 | `#FFF6EB` | 4 × 80px circles, gap 15px |
| 12 | **footer marquee** | 51 | `#FFCD78` | |
| 13 | **power-footer** | 529 | `#00559B` | 12-col grid, gap 25.6px, condensed caps links, newsletter, credits row |

### Which are stock Dawn (reuse) vs custom (build)

- **Stock, already in `sections/`:** `image-banner`, `featured-collection`, `rich-text`, `footer`
  — they already emit `.banner__heading`, `.card--card`, `.rich-text__blocks`. Restyle via CSS,
  add the `.button--wrapper` markup.
- **Custom, to build:** `marquee`, `find-us`, `split-content`, `focus-carousel`, `social-icons`,
  `falling-stickers`, `power-footer`.
- **Existing `jjw-*` sections:** `jjw-marquee-ticker` → rework to §5. `jjw-founder-story` →
  `split-content`. `jjw-reviews-carousel` → `focus-carousel`. `jjw-press-logos` → `find-us`.
  `jjw-hero-split` → **retire**, replaced by stock `image-banner`.

---

## 10 · Out of scope — say so plainly

Checkout and the order-status ("thank you") page are Shopify-hosted and **not themeable**.
Shop plan is `Shopify`, not Plus, so the `checkoutBranding` API is unavailable. Those two
pages are brandable only through the Checkout editor in admin — logo, colours, fonts.
This is identical under a headless build; it is not a reason to choose one over the other.
