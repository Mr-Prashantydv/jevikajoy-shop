# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A **from-scratch Shopify Liquid theme** for Jevika & Joy's World (JJW), a kids' t-shirt
store selling character tees organised by Character / Age / Colour / Gender.

The design language is deliberately modelled on `partakefoods.com`. That site is itself a
Dawn derivative, which is why its CSS maps cleanly onto ours — but **this theme has no Dawn
underneath it**. `layout/theme.liquid`, `assets/theme.css` and `assets/theme.js` are hand-written.
An earlier attempt built on Dawn and was abandoned because inherited `!important` rules kept
overriding new work; that history lives on `master`, this build lives on `scratch-theme`.

`README.md` is Dawn's original README, left over from that base. **It does not describe this
theme** — ignore it.

## Stores and themes

The shop has moved twice. Only the third store is alive:

| Store | State |
|---|---|
| `bnwvrc-04.myshopify.com` | First store. Returns HTTP 402. |
| `00d611-p1.myshopify.com` | **Frozen** for unpaid billing — "This store is currently unavailable" (checked 2026-10-16). Admin, storefront and API are all closed. See `docs/migration/ownership-transfer-runbook.md`. |
| **`1uz1hi-01.myshopify.com`** | **Current.** Catalogue migrated 4 October 2026 (`docs/migration/`). Serves `jevikajoy.shop`. Shopify account `jevikaandjoy@gmail.com` per the migration notes (`jevikajoychatgpt@gmail.com` is the other candidate the owner named) — log the CLI in with whichever holds it. |

Themes on `1uz1hi-01`, read from the storefront's `Shopify.theme` on 2026-10-16:

| Theme | ID | Role |
|---|---|---|
| JJW Migration | `164825399535` | **main — live to shoppers** |
| JJW UI consistency preview | `164840702191` | unpublished — the working target |

**Never push to `164825399535` without an explicit go-ahead in chat.** It is the live store.

**The local source has not been diffed against either theme since the move.** The preview
holds the October UI pass (`docs/ui-consistency.md`), and the Weekend Picnic hero went
straight to live (`design.md`). Pull both into scratch folders and compare before the first
push, or a push may silently undo work that only exists remotely.

**Facts below that were measured before October 2026 came from `00d611-p1`.** They describe
this theme's code correctly, but anything about *store* state has to be re-checked on
`1uz1hi-01` before it is relied on: the automatic discount's ID, threshold and minimum
quantity; the free-shipping rate; the Search & Discovery filters; whether Judge.me is
installed; which menus exist; the customer-accounts version, plan and the shop ID in the
sign-in URL; the `queries` corpus; product IDs and SKUs. Known already: **the new store's name
was never set**, so every page `<title>` reads "My Store" (Settings → General in admin).

The Shopify connector in Claude may still be authorised against the frozen store, in which case
every call answers *"This shop is unavailable for API access"*. Reconnect it to `1uz1hi-01`
before any Admin API work.

## Commands

```bash
# Push to the preview theme (the working target)
shopify theme push --store 1uz1hi-01.myshopify.com --theme 164840702191 --path .

# Push specific files only
shopify theme push --store 1uz1hi-01.myshopify.com --theme 164840702191 --path . \
  --only sections/hero.liquid --only assets/theme.css

# Pull remote state (useful when the theme editor has been used)
shopify theme pull --store 1uz1hi-01.myshopify.com --theme 164840702191 --path <dir>

# List themes
shopify theme list --store 1uz1hi-01.myshopify.com

# Create a shareable snapshot (uploads a NEW unpublished theme, returns a preview URL)
shopify theme share --store 1uz1hi-01.myshopify.com --path .
```

Preview: `https://1uz1hi-01.myshopify.com?preview_theme_id=164840702191` — it redirects to
`jevikajoy.shop` and keeps the preview parameter.

**Always use the permanent `.myshopify.com` domain with the CLI.** `jevikajoy.shop` is only the
store's primary domain, and the CLI rejects it with a confusing "not authorized to use the CLI
to develop in this store".

### Setting up a machine

- **Node.js 22.12+ and Git 2.28+** (Shopify CLI 4.x requirements), then
  `npm install -g @shopify/cli@latest`. CLI 4.x upgrades itself after that.
- On Windows, a default PowerShell execution policy blocks the `npm.ps1` / `shopify.ps1`
  shims with "running scripts is disabled on this system". Call `npm.cmd` / `shopify.cmd`,
  or work from Git Bash.
- If git refuses with "detected dubious ownership", the folder was created under another
  Windows account. `git config --global --add safe.directory D:/projects/JEVIKAJOY.SHOP`
  clears it.
- **There is no git remote.** Commits on `scratch-theme` exist only on this disk.

There is no build step, no test suite, and no linter wired up. `.theme-check.yml` and
`.prettierrc.json` are Dawn leftovers.

## Four push traps that will cost you time

**0. `assets/.claude-flow/` fails the entire push.**
Shopify allows no subfolders under `assets/`, and the claude-flow plugin writes
`neural/stats.json` and `policy/state.json` there. Every push then errors out. It is
gitignored and regenerates freely, so just `rm -rf assets/.claude-flow` before pushing.
`.shopifyignore` does **not** help — the CLI validates the folder structure before it
applies ignore rules. This cost ~20 minutes once.

**0b. `{% schema %}` rejects unknown top-level keys.**
Only `name, tag, class, limit, settings, blocks, max_blocks, presets, default, locales,
enabled_on, disabled_on` are allowed. Adding e.g. a `"comment"` key fails the push. Put
notes in a Liquid comment above the schema instead.

Never pipe a push through `grep -c` — it swallows the error text and you learn only that
something failed. Filter with `grep -v` on the noise instead.


**1. Schema and `templates/*.json` must be pushed in that order, separately.**
Shopify validates template blocks against the schema it has *at that moment*. Push a new block
setting and the template that uses it in one command, and Shopify **silently drops the setting**
— no error, the blocks just arrive incomplete. Push the section first, wait, then the template.

**2. Changing a template's extension needs two full pushes.**
Shopify refuses to hold both `product.liquid` and `product.json`. A scoped `--only` push cannot
delete the stale one. Run a full `shopify theme push` twice — the "Cleaning your remote theme"
step removes it on the second pass.

## Architecture

### Brand colours — the only colour authority

**Reference sites (partakefoods.com or any other) contribute layout, structure and
motion — never colour.** Every colour must come from the JJW brand sheet or be a
documented tint/shade of one of its anchors. When cloning a reference section, take its
measurements and swap every colour role for the JJW equivalent before writing CSS.

| Sheet name | Hex | Token |
|---|---|---|
| Adventure Red | `#F52A2A` | *(unused so far — no token yet)* |
| Adventure Blue | `#0F7DAF` | `--blue` |
| Sunshine Gold | `#F6A313` | `--gold` |
| Sky Blue | `#59C8F6` | `--sky` |
| Mint Green | `#73D78D` | `--mint`, `--green-bg` *(too light for text; `--green` uses Outdoor `#4FAF4B`)* |
| Coral Orange | `#FF7A45` | *(no token; split-content uses a darkened shade for text)* |
| Lavender | `#A88BFF` | `--lavender`, `--purple-bg` |
| Candy Pink | `#FF5FA2` | `--candy`, `--pink-bg` |
| Star Yellow | `#FFD94C` | `--yellow` |
| Heart Pink | `#FF4F8B` | `--pink` |
| Magic Cyan | `#46D8FF` | *(no token)* |
| Space Purple | `#7259FF` | `--purple` |
| Navy Blue | `#1A2F5E` | `--ink` |
| Night navy | `#10244A` | `--ink-deep`, `--pink-deep` (all button shadows) |
| Indoor background | `#FFF7E8` | `--cream` |
| Pure White | `#FFFFFF` | `--white` (cards on the cream canvas) |
| Warm White | `#F8F8F6` | `--warm-white` |

**The `*-bg` character fills are sheet colours, not tints. Do not mix new ones.** They used to
be `#ffd7e6` / `#c9e8f7` / `#ffe9c2` / `#d3f3de` / `#e4dcff` — five pastels we invented,
because the sheet has no tint ramp. They are now aliases onto colours the sheet names:

| Character | Token | Sheet colour | `--ink` on it |
|---|---|---|---|
| Jevika | `--pink-bg` | Candy Pink `#FF5FA2` | 4.60:1 |
| Joy | `--blue-bg` | Sky Blue `#59C8F6` | 6.83:1 |
| Brutus | `--gold-bg` | Star Yellow `#FFD94C` | 9.48:1 |
| Minku | `--green-bg` | Mint Green `#73D78D` | 7.34:1 |
| Pinki | `--purple-bg` | Lavender `#A88BFF` | 4.84:1 |

They are saturated, not pale, which changes what may sit on them — see the contrast note
below. Eight sections consume these five tokens, so a value change here reaches the whole
theme at once.

Known, deliberate exceptions: the hero field `#034CA2`/`#012F66` matches the colour baked
into the hero artwork (changing it needs new art), and PDP colour swatches (`#2563eb`,
`#e3d0ac` for Sand, etc.) depict physical garment colours, not brand UI.

**Every Colour option value needs a swatch entry** in `assets/theme.css`
(`[data-swatch='<handle>']`). A value with no entry falls back to `--ink-soft` and renders a
navy dot — which is how a Sand colourway briefly showed up as navy. Add the hex when you add
the colour. The map lived scoped inside `main-product.liquid` until the collection page's
colour filter began drawing the same dots; it is unscoped now so one list serves both, and the
PDP rules that used to win on `#MainProduct-<id>` specificity were deleted rather than left to
shadow it.

**Never tint text with its own card's solid — always `--ink` on the fill.** The reference does
tint, and copying it put gold on its pale-yellow card at roughly **1.5:1**. When the fills went
from pastel to sheet colours this turned fatal: Heart Pink type on a Candy Pink card measured
**1.10:1**, Sunshine Gold on Star Yellow 1.50, Outdoor Green on Mint 1.56 — the carousel titles
and every mega-menu character label were effectively invisible. All of them are navy now, and
`--card-fg` / `--mc-shadow` survive only to colour offset shadows, where contrast does not
apply. Colour coding lives in the fill; the type stays readable.

Audit after any change to these five tokens. Walking every element whose computed background
is one of the fills, then every descendant that renders its own text, found the eight header
failures that a page-by-page eyeball had missed. The floor across home, collection, PDP, cart
and search is now 4.60:1 over 78 pairs.

Tokens live in three places that must stay in sync: `assets/theme.css` `:root`,
`config/settings_schema.json` defaults, and `config/settings_data.json` current values —
the settings values win at runtime via `layout/theme.liquid`.

### Design system

`assets/theme.css` is the single source of tokens and shared classes. Sections should reuse
these rather than redefining them:

- `.page-width`, `.hxxl`, `.accent-caps`, `.visually-hidden`
- `.btn-wrap` / `.btn-shadow` / `.btn` — the signature button: two stacked layers on one SVG
  clip path, shadow offset `6px 6px` collapsing to zero on hover
- `.marquee` / `.marquee__track` / `.marquee__group` — 24s linear, content repeated so the
  `-50%` translate loops seamlessly
- `.scroll-trigger` + `.animate--fade-in` / `.animate--slide-in`, driven by `assets/theme.js`

**`IntersectionObserver` alone strands content invisible.** It fires only on a *change* of
intersection state, so a jump that lands past an element — a hash link, a browser-restored
scroll position, a full-page screenshot — takes it from "not intersecting, below" to "not
intersecting, above" with no intersecting frame between, the callback never runs, and it
keeps `opacity: 0` for the life of the page. Three `/collections` cards were permanently
invisible this way and it read as a section bug, not a theme-wide one.
`initScrollReveal()` now also reveals on `!isIntersecting && boundingClientRect.bottom <= 0`
and sweeps on a passive, rAF-throttled `scroll` listener that unbinds itself once nothing is
left hidden. Anything new using `.scroll-trigger` inherits the fix; do not reimplement it.

`html` is `62.5%`, so **1rem = 10px**. Rem values port directly from the React source.

The `#jjw-blob` clipPath is defined once in `layout/theme.liquid`. Reference it with
`clip-path: url(#jjw-blob)`; never redefine the geometry. Always pair with an
`@supports not (clip-path: url(#jjw-blob))` fallback to `border-radius`.

### Section conventions

Every section follows the same shape:

```liquid
{%- style -%}
  #Name-{{ section.id }} .thing { ... }   /* always scoped to the section id */
{%- endstyle -%}

<section id="Name-{{ section.id }}"> ... </section>

<script>
  (function () {
    var root = document.getElementById('Name-{{ section.id }}');
    if (!root || root.dataset.someInit) return;   /* guard theme-editor re-render */
    root.dataset.someInit = '1';
    ...
  })();
</script>

{% schema %} ... {% endschema %}
```

All human-visible copy comes from settings or blocks. Never hardcode it in markup.

**Responsive overrides must be placed after the base rule.** Media queries add no specificity,
so a plain rule later in the file silently wins. This has already caused one bug.

**`scroll-snap-type: x mandatory` can freeze a carousel solid.** Snap points sit at each
card's `scroll-snap-align` edge. In `fabric-story` those were 0 / 474 / 948, while the track
only scrolled 473px in total — so every point except 0 was unreachable and the browser pinned
`scrollLeft` back to 0 on every attempt, arrows and swipe alike. It looks exactly like broken
JavaScript. Use `proximity`, and give the last card `scroll-snap-align: end` so the end of the
track is a reachable point at all. Any track showing N-of-M cards has this problem.

**Do not pass `behavior: 'smooth'` to `scrollBy`.** The options object overrides the element's
`scroll-behavior`, so a `prefers-reduced-motion` rule that sets `scroll-behavior: auto` is
ignored. Omit it and let CSS decide. It also makes the scroll testable — see the preview-pane
note under "Verifying changes".

**Padding cannot inset an absolutely positioned child, and `inset` cannot size an image.**
Two failed attempts at putting an even frame around the `featured-collection` packshot:
padding on the positioned parent did nothing, because an absolutely positioned child resolves
`inset: 0` against the parent's *padding box*, which already includes that padding. Moving the
inset onto the image as `inset: 2.6rem` then broke differently — an `<img>` is a **replaced**
element, so `width: auto` takes its intrinsic width and the opposing offset is ignored, leaving
the picture hanging 26px off the right edge. What works is `padding` on the `<img>` itself:
`object-fit` draws into the content box, so padding both shrinks the drawing area and keeps it
centred. One variable drives all four sides.

**Never hang carousel button state solely off the `scroll` event.** One missed event leaves a
button `disabled`, a disabled button swallows the next click, and the track is stranded at that
end permanently. `fabric-story` re-syncs on a timer after each click as well.

Shared snippets:

- `snippets/product-accordions.liquid` — the white info card on the PDP (20px radius, rows
  split by a 2px `--sky` rule). Four hardcoded rows; make them blocks if a fifth is ever needed.
- `snippets/header-card.liquid` — one character card, rendered by **both** the desktop mega
  panel and the mobile drawer (`style: 'drawer'` switches the class set). Art resolves
  merchant image → `<character>-face.png` from assets → label only. Keeping one snippet is
  what stops the two surfaces drifting apart.

### The two big sections

**`main-product.liquid`** carries more than a PDP usually does:

- character **tabs** under the h1, one per character collection, auto-selected from the
  product's `character:` tag; each panel lists that collection's products
- a tilted **badge rail** left of the packshot — real type, not PNGs, per the house rule that
  image-borne text becomes editable text. Badges are blocks with a "show for character"
  setting, so the rail changes per character
- one **gallery per colour**, chosen by the alt-text convention above: featured packshot, a
  2:1 banner, then two squares. On mobile these become a scroll-snap carousel with dots
- accordions, then the buy block

**`header.liquid`** — the drawer and mega panel are children of `.hdr-bar`, *not* siblings.
That matters: see the stacking-context note under "Verifying changes". It also owns the
**search panel**, a third child with its own `data-search` state — the menu (`data-open`)
and search close each other but share the one overlay, so the overlay only hides when both
are shut.

### Search

Three files: the panel and its behaviour in `header.liquid`, results markup in
`sections/predictive-search.liquid` (no schema, fetched with `&section_id=predictive-search`),
and the results page in `sections/main-search.liquid`.

**Prefix matching only works through a trailing `*`.** Shopify's documented
`options[prefix]=last` is measurably inert on this store — `/search?q=adven&options[prefix]=last`
returns 0 while `/search?q=adven*` returns 4. `assets/theme.js` appends the star on submit for
every `form[role="search"]`, and the header's fetch appends it too. Sections echo the terms back
through `remove_last: '*'` so the star never reaches the heading or the field. Shopify's own
`<title>` still shows it; that is not themeable from here.

**Filtering is Shopify's, not ours.** Liquid cannot read arbitrary query parameters, so
`search.filters` is the only honest route. Search & Discovery is already configured on this
store with **availability, Size, Color, and one product-tag filter labelled "Character"** —
which is why `filter.p.tag=character:Brutus` narrows correctly. Two things about that tag
filter are admin-side content, not theme bugs: it also carries the `gender:` values (Boys,
Girls) and a stray `Adventure Squad`, and **Minku is missing from it**. Only `list` filters are
drawn; a price range needs two inputs and is skipped rather than half-rendered.

Do not be tempted to filter by appending a character name to `q` instead. `q=joy*` returns all
ten products, because the vendor string "Jevika and Joy's World" is indexed.

The drawer is two columns, suggestions then products, matching the reference. **Shopify's
`queries` resource is built from what shoppers have actually searched**, so on this store it is
nearly empty — only `tee`, `smart tech` and `boxer tee` exist today; `adven` and `bru` return
none. Collections render below the queries in the same column so it is never blank, and they
drop down the list on their own as the query corpus grows. `styled_text` marks the part that
matched, so lightening `.psearch-item span` is what leaves the completion reading bold.

`snippets/character-pair.liquid` is the one place the character → colour mapping lives; it
outputs a single word and is meant to be `capture`d. `product-card.liquid` and the drawer's
thumbnails both go through it. The older copies in `main-collection`, `main-product`,
`main-cart` and `falling-scroll` have not been migrated.

`.jjw-card` / `.jjw-grid` / `.jjw-pill` in `theme.css` are unscoped on purpose — `.jjw-pill`
renders on both `/search` and the collection page, so section-scoped rules would not reach
both. `main-collection.liquid` uses the shared pill but still has its own copy of the card
rules.

### Cart drawer

`sections/cart-drawer.liquid` is rendered from **`layout/theme.liquid`** with
`{% section 'cart-drawer' %}`, not from a section group. That is deliberate: it makes the
section addressable as `cart-drawer` by the Section Rendering API, which is how `/cart/add.js`
and `/cart/change.js` hand back freshly rendered line items in the same round trip. The drawer
never rebuilds a line item in JavaScript.

**It is a sibling of the header, never a child.** The header already owns two panels whose
state lives on `#Header-<id>` *inside* `.hdr-bar`. A third panel hung off that root would
inherit the bar's stacking context — the exact bug that once buried the logo and close
button. The drawer carries its own overlay at `z-index: 70` and panel at `71`, clear of the
header section's sticky `50` and its pinned `60`. The two coordinate by event only:
`jjw:cart-open` and `jjw:header-open`, each closing the other's panels.

Four API facts that are easy to get wrong, all confirmed against the docs:

- **`/cart/add.js` does not return the cart.** Its body is `{"items": [...]}` — no
  `item_count`, no totals. Reading `item_count` off it yields `undefined`; re-fetch `cart.js`.
  `/cart/change.js` *does* return the full cart.
- **Identify lines by `key`, never index.** `/cart/change.js` takes `id` *or* `line`, never
  both. An index shifts the moment an earlier line is removed, silently editing the wrong row,
  and two lines can hold the same variant with different properties. The cart *page* still
  uses positional `updates[]` and `url_to_remove`; the drawer does not.
- **Scripts inside section-rendered HTML do not execute** when inserted via `innerHTML` or
  `DOMParser`. All drawer behaviour is delegated from a listener outside the replaced region.
- **Never hardcode `/cart/add.js`.** Use `window.Shopify.routes.root + 'cart/add.js'`; the
  root carries the locale/market prefix and a hardcoded path 404s the day a second market
  opens.

Refresh swaps `[data-cd-body]`, `[data-cd-foot]` and `[data-cd-count]` only — never the whole
section, which would take the root element, the open state and the `<style>` block with it.

**Do not send `Accept: application/json` with `?sections=`.** On a product URL that header
makes Shopify answer with the *product* resource and ignore the sections parameter entirely —
the body comes back as `{"product": {...}}` with no section HTML, so the refresh silently does
nothing and the drawer keeps showing a stale cart. The same URL without the header returns
`{"cart-drawer": "<html>"}`. The Section Rendering API already replies with JSON whenever
`?sections=` is present; asking for JSON on top of it picks the wrong resource. This cost a
real bug that only surfaced when the cart was changed outside the drawer's own JavaScript.

**`cart.total_price` is already net of discounts — never label it "Subtotal" above a
discount row.** Doing that printed `Subtotal Rs. 1,527.45` and `−Rs. 269.55` underneath, which
reads as Rs. 1,257.90 while checkout charges Rs. 1,527.45 — understating the price to the
shopper on the exact 3-item cart the bundle nudge is pushing them toward. Use
`cart.original_total_price` for the gross line, then the saving, then `cart.total_price` as
the total, so the three numbers reconcile.

**The drawer must never open over `/cart`.** `main-cart.liquid` edits quantities with a
*positional* `updates[]` array, and the drawer only re-renders itself. Remove a line in the
drawer while the cart page is underneath and that form is left holding three values against a
two-line cart, so the next quantity typed there is applied to the wrong product. The opener is
gated on `template.name == 'cart'` and simply lets the link navigate.

**Opening order matters for the scroll lock.** The drawer used to lock `body` overflow and
*then* dispatch `jjw:cart-open`; the header's listener closed its own panels, and its
`lockScroll()` saw both header states false and cleared the lock — unlocking the page behind
an open drawer. Dispatch first, write `overflow` last, so the drawer's write is the survivor.

The cart **page** and the drawer show the same three rows, built the same way. Two rules
keep the numbers reconciling whichever kind of discount admin is running:

- **Name discounts from `cart.discount_applications`, never `cart_level_discount_applications`.**
  A product discount ("15% off any 3 tees" can be one) is line-level and never appears in the
  cart-level list, so the row came out unnamed. One row per application, using
  `total_allocated_amount`; the amounts sum to `cart.total_discount`.
- **A discounted line shows its full price struck through beside `final_line_price`.** A
  product discount is already inside `final_line_price`, so without the struck figure the
  lines add up to less than the full-price subtotal printed under them. The two prices carry
  visually hidden labels from `sections.cart.*` in the locale file.

**Two settings must be kept in step with admin or the store lies to the shopper.**
`free_shipping_threshold` has to match the real shipping rate (today: Rs. 0 domestic standard
at or above **Rs. 999**), and `bundle_quantity` has to match the automatic discount's minimum
(**15% off at 3+** on the old store, `DiscountAutomaticNode/1831669891204` there — the ID
differs on `1uz1hi-01`). The same discount is
advertised by `bundle-banner` on the PDP and cart page, so a change in admin has to move
three things.

The header cart icon stays an `<a href="{{ routes.cart_url }}">` and checkout stays a real
form POST, so with JS off both degrade to the cart page rather than dead controls.

### Data model — build for this, not for assumptions

10 products. Every one has exactly two options: **Size** and **Color**.

- Sizes are normally `4-5 Y`, `6-7 Y`, `8-9 Y`, `10-12 Y`. **`giggles-tee` is the exception**:
  six overlapping ranges (`4-5`, `5-6`, `6-7`, `7-8`, `9-10`, `11-12`) whose extra variants have
  null SKUs. Do not assume four sizes.
- Colour sets differ per product (3 to 6 values) — a real source of off-by-one bugs in variant
  matching. Values in use: Blue, Yellow, Black, White, Pink, Peach, **Sand**.
- Tags carry taxonomy: `character:Pinki`, `gender:Boys`, `gender:Girls`. A product may carry
  **more than one** `character:` tag — `brutus-boxer-tee` is both Brutus and Joy. Code that
  derives a colour pair must decide deliberately which one wins (see below).
- **Descriptions are written for all 10.** They were empty on 9 of 10 until Phase 2. The
  house voice is the `wander-tee` copy; drafts live in `docs/product-copy/descriptions.json`.
  They deliberately claim only what the site already claims — organic cotton, BIS, OEKO-TEX
  inks, ages 4-12 — and never fabric weight, origin, wash durability or popularity. Products
  with no photography describe the character and the make, never a print, because there is no
  way to know what is on a shirt nobody has photographed.
- **5 of 10 products have images**, 4-per-colourway plus a 16:9 banner: `tech-builder-tee` (15),
  `adventure-tee`, `brutus-boxer-tee`, `giggles-tee`, `wander-tee` (16 each). The other five
  have none, and descriptions are empty across the board. Anything reading
  `product.description`, `product.images` or metafields must still degrade to nothing or to a
  settings default — never a broken `<img>` or an empty box.

**Product media alt text is load-bearing.** Shopify stores one featured media per variant, not
a gallery, so there is no API-level "these four shots are the black ones". The PDP recovers the
grouping by matching the **first word** of each media's alt against the Colour option values —
so every uploaded shot is alted `"<Colour> <Product> …"`. Two consequences:

- Match on the first word only. A substring match reads the *background* out of
  `"in navy, flat lay on yellow"` and files a navy tee under Yellow.
- Media whose alt starts with no known colour is treated as belonging to *every* colour, so a
  rewritten alt degrades to "shown too often", never to "lost".

Known SKU defect: several products give Blue and Black variants the **same** SKU because both
were abbreviated `BL` (e.g. `JJW-TB-BL-4`). New variants added since use `BK` for Black. Worth
fixing store-wide; not yet done.

### Character colour pairs

Sections derive a colour pair from the `character:` tag. Used by product cards, the PDP
gallery fallback, cart thumbnails and the falling-scroll cast:

| Character | bg / fg tokens |
|---|---|
| Jevika | `--pink-bg` / `--pink` |
| Joy | `--blue-bg` / `--blue` |
| Brutus | `--gold-bg` / `--gold` |
| Minku | `--green-bg` / `--green` |
| Pinki | `--purple-bg` / `--purple` |

Default to blue when no tag matches. Where a product carries several `character:` tags, prefer
the one matching the collection being viewed — `main-collection.liquid` does this so Brutus
Boxer Tee reads gold on `/collections/brutus` and blue on `/collections/joy`. Taking the last
tag instead makes it blue everywhere, since tags arrive alphabetically.

**Character collections are smart collections keyed on the tag** (`character:Joy` →
`/collections/joy`), as are `boys` / `girls` on `gender:`. Adding a product to a character
category is a `tagsAdd`, never a collection edit.

### Size guide and reviews

The size guide is `snippets/size-guide.liquid`, a `<details>` rendered inside the **Size**
fieldset on the PDP — at the moment the size is chosen, not buried below. Rows come from one
pipe-separated `textarea` setting on `main-product`, first line the header. A textarea rather
than blocks because a size chart changes as a whole, and eight size rows in the theme editor's
block list next to the badge blocks would be worse to edit, not better.

**Its numbers are a general Indian kidswear standard, not measurements taken from a JJW
garment.** Prashant chose that knowingly over shipping it empty. The note under the table says
so on the page and must keep saying so until real measurements replace them.

`product-accordions.liquid` used to carry a fourth row, Size Guide, with its own hardcoded
table. It was removed rather than kept alongside: two tables on one page disagreed on
convention (accordion measured chest circumference in cm, the new one flat width in inches),
and the accordion's four hardcoded sizes were simply wrong on `giggles-tee`, which has eight.
The snippet is three rows now.

**Judge.me is installed and syncing** — it writes `product.metafields.judgeme.badge` (the star
badge, for cards) and `.widget` (the full review block, for the PDP). `snippets/review-stars.liquid`
prints the badge and renders nothing when the metafield is absent, which is every product but
`wander-tee` today. ⚠️ **The Judge.me app embed is not enabled in this theme**
(`config/settings_data.json` has no app embed blocks at all), so its script never loads and the
badge — which ships `display:none` and relies on that script to reveal it — stays invisible.
Turning it on is one toggle in the theme editor under Settings → App embeds, and nothing
Judge.me-related will appear until someone does.

⚠️ Shopify's product search **silently mis-filters tags containing a colon**:
`query: "tag:'character:Minku'"` returns only some of the matching products. Filter in code
against the full product list instead of trusting that query.

### Page composition

Templates are JSON and compose sections; `header-group.json` / `footer-group.json` wrap them.

- `templates/index.json` — hero, marquee-banner, featured-collection, find-us, falling-scroll,
  split-content, focus-carousel, rich-text, social-marquee, social-icons
- `templates/product.json` — main-product, fabric-story, split-content (reused as the feature
  panel), featured-collection (as related products)
- `templates/collection.json` — main-collection, product-trust

### Collection filtering

`main-collection.liquid` carries two different things that look alike and must not be confused:
the **character pills** at the top are navigation *between* collections (each is a link to
`/collections/<handle>`), and the **filter bar** below the heading narrows *within* the current
one. They were originally drawn with the same solid Sky Blue `.jjw-pill` and the page read as
one wall of blue with no way to tell a link from a control. Filters are now outlined —
white fill, 2px navy ring, filling navy when active. Keep that distinction if either is
restyled.

Filtering is Shopify's `collection.filters`, the same route `main-search.liquid` uses. Four
filters exist on this store: Availability, Size, Color and a product-tag filter labelled
"Character". Notes that cost time to establish:

- **Size values arrive in numeric order already** — `4-5 Y … 11-12 Y`, not alphabetical.
  Verified live. Do not add a sort on the assumption that `10-12 Y` would lead.
- Size is relabelled **"Age"** through a setting, because the values *are* ages and parents
  shop by age. `hidden_filters` takes a comma-separated list of Shopify's own labels for
  anything a merchant wants dropped.
- **Values with `count == 0` are skipped, unless active.** Everything is in stock today, so
  otherwise the Availability filter would offer an "Out of stock" pill that returns nothing.
  The `unless active` half matters: without it the pill you just clicked disappears under you.
- **The sort form must carry active filters as hidden inputs.** It is a GET submit, so without
  them the query string is rebuilt from the form alone and every applied filter is silently
  dropped. Clearing filters likewise preserves `sort_by` when it is not the default.
- The empty state distinguishes "this collection has nothing" from "your filters matched
  nothing" — only the second has a way out, and it gets a clear-all link.

The **Character** filter is admin-side content, not a theme bug: its values also include the
`gender:` tags and the three theme tags (`Adventure Squad`, `Street & Sports`, `Tech & Smart`).
Minku is present — an earlier note here said it was missing, and that is no longer true.

`product-trust` (the nine curved-text badges) was swapped off the PDP for `fabric-story` and
now renders **only** on the collection page. The section file stays for that reason.
- `templates/cart.json` — main-cart, bundle-banner, featured-collection (as recommendations)
- `templates/search.json` — main-search (no blocks; filters come from Shopify)

`bundle-banner` announces the store's automatic discount and is declared on **both**
`product.json` and `cart.json`; the copy lives in settings so the same section carries
whatever the offer becomes. Clearing its heading switches it off everywhere at once. The
discount itself is a Shopify automatic discount — **15% off any 3 tees**, min quantity 3,
`DiscountAutomaticNode/1831669891204` on the old store — so the banner is only advertising,
never enforcing.
Change one and the other has to follow, or the store promises a price it will not charge.

`whatsapp-button` lives in `footer-group.json`, which renders on every template just before
`</body>`. It returns nothing until a number is entered, so it ships hidden rather than
behind a checkbox. It sits at `z-index: 8`, deliberately below the header overlay's 10, so
opening the menu or search covers it instead of leaving it floating over the scrim.

- `templates/page.json` — main-page
- `templates/page.contact.json` — main-page (title only) + contact-form
- `templates/404.json` — main-404
- `templates/list-collections.json` — main-list-collections

`blog` and `article` remain placeholder `.liquid` files printing "This page is not built
yet." The store's only blog is Shopify's default *News* with **zero** articles, so there is
nothing to render; build them when there is. `templates/customers/` is empty on purpose.

**`templates/policy.liquid` is never rendered on this store — do not write one.** Shopify
serves `/policies/*` itself and injects its own markup into the theme layout:

```
.shopify-policy__container > .shopify-policy__title > h1
.shopify-policy__container > .shopify-policy__body  > .rte
```

One was written, uploaded, and confirmed byte-identical on the remote by checksum; the live
page still came back as Shopify's container, so the file was deleted rather than left as
dead code. Style the classes above instead — they live in `theme.css`. Shopify also injects
`policy-<hash>.css`, whose rules are plain and the same specificity as ours
(`.shopify-policy__container { max-width: 65ch }`), and load order is not ours to control;
the rules are scoped under `#MainContent` to win on specificity rather than with the
`!important` this theme was rebuilt to be rid of.

That is also why the shared prose class is **`.rte`, not `.jjw-rte`** — Shopify's policy
body already carries `class="rte"`, so one rule set styles both the policy pages and
`main-page` instead of 26 duplicated selectors. Anything rendering admin-authored rich text
should use it, and must sit on `--white`: `--blue` links are 4.34:1 on cream (fails AA) and
4.59:1 on white.

**Neither a `{% render %}` argument nor an `{% if %}` condition takes a filter chain.**
`face: handle | append: '-face.png'` and `if line | strip != blank` both fail the push with
*Expected end_of_string but found pipe*. `assign` it first — each of these cost a push cycle.
Worse, the CLI reports this as a per-file error inside a wall of `--only` pattern warnings, so
a `| tail -8` shows the success box of the run and hides it — the section silently stayed at
its old version through two pushes. Filter pushes with
`grep -iE "^\W+(error|success)|Liquid syntax"`, never by line count.

**A `--only` push can print the success box and not apply the file.** It has happened twice:
`main-list-collections.liquid` and `product-accordions.liquid` both reported success while the
remote kept the previous version, and the second one was only caught because the rendered page
still showed a row that had been deleted. A full `shopify theme push` fixed both. The success
box is not evidence — verify with the Admin API and compare checksums:

```bash
python -c "import hashlib,pathlib;d=pathlib.Path('snippets/x.liquid').read_bytes();print(len(d),hashlib.md5(d).hexdigest())"
```

then read `theme.files(filenames: [...]) { nodes { size checksumMd5 } }` and require both to
match. This is the same check the product-image uploader runs on its signed policies, and for
the same reason: a silent no-op is worse than an error.

**A `richtext` setting must never be emitted inside a `<p>`.** It brings its own `<p>`, and a
nested one closes the outer tag early, so the copy escapes the class that was styling it and
lands unstyled with browser-default 1em margins. It renders — which is why it survives a
glance — but at the wrong size and colour. Four sections shipped this before it was caught
(`main-404`, `main-list-collections`, `contact-form`, `size-guide`). Use a `<div>` and add
`:where(p) { margin: 0 }` so the wrapper keeps owning the spacing. Grep for it with:

```bash
grep -nE '<p[^>]*>\{\{ *section\.settings\.[a-z_]+ *\}\}</p>' sections/*.liquid
```

**`nil == 0` is false in Liquid.** `collections['minku'].all_products_count == 0` does not
guard against a deleted collection — it yields nil and the test passes through, rendering an
empty tile. Test `== blank` first.

The footer nav is wired: `footer.liquid` loops over `menu` blocks, and `footer-group.json`
declares two — `footer` (shop and help) and `footer-legal`. Both menus exist in admin.
`footer-legal` holds **only Privacy**, because it is the store's only policy; the drafts for
the other four are in `docs/policies/` and have to be pasted into admin by hand, since the
Shopify connection lacks `write_legal_policies` and `shopPolicyUpdate` refuses without it.

Not yet built from the reference: the collection page's full-bleed banner strip, its wide
feature panel, and the "sweet treat" marquee band.

**Inside a `{% liquid %}` tag every line is a separate statement.** A filter chain wrapped
across lines parses as unknown tags — `assign x = y` then a line starting `| remove: '+'`
fails with *Unknown tag*. Keep the chain on one line. And never write percent-brace markup
inside a `liquid`-tag `comment`: the literal braces close the tag early, which reports as
*'comment' tag was never closed*. Both cost a push cycle each in `whatsapp-button`.

**Sections declared in a template get only the blocks that template specifies.** A section's
`presets` block list applies only when a merchant adds it through the theme editor. Forgetting
this leaves marquees and carousels rendering as empty bands — it has happened three times.

## Reference material

- `docs/clone/DESIGN-SYSTEM.md` — measured ground truth from the reference site
  (type scale, button anatomy, card spec, colour-role mapping, page topology). Where any other
  source disagrees with this file, this file wins.
- `docs/clone/ASSET-MANIFEST.md` — every image slot and what still needs supplying.
- `docs/clone/raw/` — the reference site's own CSS, downloaded for measurement. **Gitignored on
  purpose**; it is third-party code and must not be committed.

## Fonts

The reference uses Bunch, Toroka and Gilroy — all commercial licences we cannot ship.
Substitutes, wired through `--font-heading` / `--font-accent` / `--font-body`:

| Role | Ours |
|---|---|
| Display headings | Baloo 2 (Google) |
| Condensed caps, buttons, nav | Big Shoulders Display (Google) |
| Body | Nunito (Google) |

All three come from one `@import` in `assets/theme.css`; `--font-heading` /
`--font-accent` / `--font-body` are the only things sections reference.

**Do not re-add SofiaProSoft-*.otf.** Those files were Fontspring *demo*
builds. Demo licences forbid web embedding, and the builds are deliberately
crippled: 96 glyphs, of which 29 — `& ' " - / ! @ ( ) 4` among them — share
the `.notdef` outline. Every apostrophe, ampersand and hyphen in body copy
rendered as a tofu box on the live PDP. If a licensed face is bought later,
swapping it in means one `@font-face` block and one token.

## Verifying changes

The Chrome DevTools MCP (`.mcp.json`) is the reliable instrument. The in-app preview pane
**fires no scroll events for programmatic scrolling and misreports images as unloaded** — it
produced six false diagnoses during this build, twice nearly causing working code to be
"fixed". Use `mcp__chrome-devtools__*` for anything involving scroll, animation or image state.
Chrome DevTools MCP refuses to attach while the user's own Chrome is running on the same
profile; if it is, fall back to the pane and treat its output with the cautions below.

When measuring, query the **exact element**, not a substring class match. Shopify wraps every
section in its own `<div>`, so `[id*="section_name"]` returns the wrapper — which is
transparent and zero-height — not the styled inner element.

### Measurement traps that produced wrong answers here

**Geometry does not prove visibility.** `getBoundingClientRect` plus `display`/`visibility`
only says an element *occupies space*. It reported the header logo, close button and search
icon all "visible" while the user was looking at a blank bar — they were painted underneath an
open drawer. Use **`document.elementFromPoint(cx, cy)`** at the element's centre and check the
hit result is the element (or a descendant). That is the only check that catches occlusion.

**A z-index only competes inside its own stacking context.** The drawer is a *child* of
`.hdr-bar`. Giving the bar `z-index` while open made it a stacking context, and within it a
positioned descendant (drawer, `z-index: 15`) paints above unpositioned content — which is
what `.hdr-grid` was. Fix was to give the row its own layer, not to raise the bar further.

**A transparent container satisfies `elementFromPoint` without hiding anything.** On the
falling-scroll heading the hit test returned `.hdr-grid` — the header's full-width grid, which
has `z-index: 30` but no background. Nothing was actually obscured. The check that found the
real collision was comparing the title's rect against the rects of the header's *painted*
controls (`.hdr-logo`, `.hdr-menu-wrap`, `.hdr-cta`, `.hdr-icon`), which caught Find In Store
sitting across the word "Every" at 1311px. Hit-testing catches occlusion by opaque things;
box intersection against the elements that actually paint catches the rest.

**Kill the orphaned MCP Chrome before assuming DevTools is unavailable.** The refusal message
names `~/.cache/chrome-devtools-mcp/chrome-profile`, which is the MCP's *own* profile, not the
user's browsing session — so a stale instance from an earlier run is usually what holds the
lock. Filter `Win32_Process` for `chrome.exe` whose command line contains `chrome-devtools-mcp`
and stop just those; nothing of the user's is touched. This unblocked the only tool that can
actually screenshot the site.

**Re-running a toggle without reloading inverts it.** A second "open the menu and measure"
script on a page where the menu was already open silently *closes* it and measures nothing.
Reset to a known state first.

**`getBBox()` lies for `textPath`.** Chrome returns the straight-line box, not the box along
the path, so every curved-text badge reported an identical bogus radius. Compare
`getComputedTextLength()` against `path.getTotalLength()` instead.

**`textContent` concatenates without separators.** A title and its price read as
`"Brutus Boxer TeeRs. 599.00"` even though the price is `display: block` on its own line.
Check the two rects, not the string.

**Don't prefix-match CSS selectors when patching.** `s.index('.hdr-mega-links .btn')` matched
`.btn-wrap` first and edited the wrong rule. Use exact-context edits.

## Product image pipeline

Masters live in `product-images/JJW-<NN>/<colour>/` as
`JJW-<NN>-<colour>-<NN>-<shot>.png`, four shots per colourway (packshot-stickers,
hero-lifestyle, back-lifestyle, hero-banner-16x9). Upload is
`stagedUploadsCreate` → HTTP POST to each target → `productCreateMedia` →
`productVariantAppendMedia`.

Each drop gets a `_upload.py` in its folder. Two things that matter:

- The signed policy differs between targets **only by the object key**, so it is rebuilt from a
  template and checked byte-for-byte against the one policy Shopify returned before anything is
  sent. A mismatch means the signatures would not verify — abort rather than fire 16 doomed
  requests.
- **Upload sequentially with retries.** At four threads a run lost 4 of 16 to local connection
  aborts (`Errno 10053`). Staged targets stay valid ~24h, so a retry pass recovers them, but
  sequential is simply cleaner.

`productVariantAppendMedia` accepts **one media id per variant** — a variant has a single
featured image, not a gallery. Passing a list fails with `TOO_MANY_MEDIA_PER_INPUT_PAIR`.

`assets/jjw-ground.webp` is the clearing the cast lands on in `falling-scroll`. Two things
about it are worth knowing before regenerating it:

- **Check the source has a real alpha channel.** The first export looked transparent but was
  mode RGB with the checkerboard *painted into the pixels*; the second was a scene rendered on
  solid black. Neither carries alpha, so both had to be keyed. `Image.open(p).mode` settles it
  in one line, and is worth running before any other work.
- Black-backed art keys on brightness, but **do not divide the colour by that brightness**.
  That is the un-premultiply for genuine additive glow and it bleaches painted artwork — the
  grass and mushroom went yellow. Take alpha from brightness and leave the colour alone.

The ground is sized by **height**, never width. Its grass line has to meet feet that land at a
percentage of the stage *height*, so width-based sizing held on desktop and dropped the grass
361px below the cast on a portrait phone. Height-based, the horizon reduces to a pure fraction
of the stage — `1 - ground_offset - 0.43 x ground_height` — and holds everywhere; `object-fit:
cover` crops the outer mushrooms on narrow screens and keeps the path and beam.

`assets/jjw-ground.png` is the clearing the cast lands on in `falling-scroll`. It is the
merchant's own cut-out — 2080x627 with a real alpha channel — and must be used **as supplied**.
Two earlier exports were not: one was mode RGB with the transparency checkerboard *painted
into the pixels*, the other a scene rendered on solid black. Both needed keying, and keying a
painted checkerboard is not recoverable cleanly — `Image.open(p).mode` settles which kind you
have in one line, and is worth running before any other work.

The ground is sized by **width**, never cropped, on desktop: `background-size: 100% auto`
anchored `bottom center`, so the whole strip shows edge to edge. Below 750px that flips to
`auto 34%`. The strip is 3.3:1, so full-width on a 390px screen resolves to a 118px sliver —
14% of the stage — and the two tallest characters landed at 73% with nothing under them.
Scaling by height keeps it a floor and crops the sides instead, which is what the reference
does. Landed feet run 75.7-89.6% on desktop against a ground top of 51.8%, and 72.7-91.8%
against 66% on a phone.

`product-images/_universal/` is the exception to all of the above: product-agnostic macro
shots (weave, collar, shoulder seam, hem) that belong to no SKU, so they ship as **theme
assets** rather than product media. The masters are 2048px PNGs at ~6 MB each; they go into
`assets/` resized to 1000px JPEG q82, which took 24 MB down to 528 KB. Reference them with
`asset_img_url: '800x'` — `image_url` does not work on theme assets, only on Shopify-hosted
media. `sections/fabric-story.liquid` offers them through a `select`, not a free-text
filename, so a block can never point at an asset that is not there.

## Out of scope

Checkout and the order-status ("thank you") page are Shopify-hosted and not themeable on this
plan. They are brandable only through the Checkout editor in admin (logo, colours, fonts).
This is equally true of a headless build; it is not a reason to change architecture.

**Customer accounts — do not build `templates/customers/`, and do not link to `/account`.**

The store runs `NEW_CUSTOMER_ACCOUNTS` (`shop.customerAccountsV2.customerAccountsVersion`).
Classic templates — `login`, `register`, `account`, `order`, `addresses`, `reset_password`,
`activate_account` — are **never rendered** under that setting, and Shopify deprecated legacy
customer accounts in Feb 2026: they are "no longer available to new stores and existing stores
not using it", and theme developers are told to stop shipping the Liquid files. Switching back
is not an option here. The folder is empty on purpose.

A plain `<a href="{{ routes.account_url }}">` 302s the shopper to
`shopify.com/authentication/<shop-id>/login` (`100517019780` on the old store) — an unbranded page with a purple *Continue
with shop* button. That page is **not** brandable on this plan: `checkoutBranding` /
`checkoutBrandingUpsert` require Plus and the store is on `Shopify`
(`shop.plan.shopifyPlus: false`), so the API answers *"Access denied … the shop must be on a
Plus plan"*.

**Use `<shopify-account>` instead.** It is Shopify's own web component, needs no script tag in
a theme, and opens a sign-in sheet **on the storefront** so the shopper never leaves JJW —
passwordless, Sign in with Shop and social providers included. The header renders it twice,
once in `.hdr-icon--account` and once in `.hdr-drawer-account`, because a third pill does not
fit the phone bar (see below); a `max-width: 749px` rule and its exact `min-width: 750px`
complement keep precisely one of the two visible.

Style it through its custom properties, which inherit through the shadow boundary so JJW
tokens resolve directly: `--shopify-account-color-accent`, `-background`, `-text`, `-border`,
`-card-background`, `--shopify-account-font-body`, `-heading`, `--shopify-account-radius-*`,
`--shopify-account-avatar-size`, `--shopify-account-signed-in-avatar-*`, and
`--shopify-account-dialog-position-top` (set to 9rem so the sheet clears the bar). The
`signed-out-avatar` slot takes our own person SVG, which is what keeps it looking like the
search and cart pills. Accent is `--blue`, not `--pink`: the sheet uses 14–16px button text,
where pink on cream is about 2.9:1 and misses AA, while blue on white is 4.6:1.

Shopify owns the sheet's layout and can change it independently of the theme. Those properties
are the whole extent of our control — do not expect it to become a JJW-designed page.

**Why the account pill is not in the phone bar.** `.hdr-grid` is `1fr auto 1fr`, and those two
`1fr` tracks are equal, so the menu column always reserves whatever the actions column needs.
At 360px three 5rem pills demand 150px a side, which with the 110px logo is 430px of appetite
inside 342px — the row wraps to 137px tall. Shrinking the pills does not rescue it at the 44px
touch-target floor. Two pills fit only because the grid gap is trimmed to 0.6rem there; at
1rem the column landed 2px short and wrapped. Below ~340px the sums stop working whatever the
gap.
