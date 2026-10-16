# JJW Design System

The design system as **built**, read off `assets/theme.css` and the section files on
`scratch-theme`. Where this disagrees with `docs/clone/DESIGN-SYSTEM.md`, this file wins —
that one describes the abandoned Dawn build and the reference site, not this theme.

There is **no Dawn underneath this theme.** `layout/theme.liquid`, `assets/theme.css` and
`assets/theme.js` are hand-written. An earlier Dawn-based attempt was abandoned because
inherited `!important` rules kept overriding new work.

`partakefoods.com` contributes **layout, structure and motion — never colour.**

4–5 October UI refinements are staged in an **unpublished preview**, not the live
theme. See [the UI pass contract](docs/ui-consistency.md) for scope and evidence.

---

## 1 · Colour

Every colour comes from the JJW brand sheet (WhatsApp, 30 Jul 2026) or is a documented
alias of one of its anchors. There are no invented tints.

### Canvas and ink

| Token | Hex | Sheet name |
|---|---|---|
| `--cream` | `#fff7e8` | Indoor background |
| `--white` | `#ffffff` | Pure White — cards on cream |
| `--warm-white` | `#f8f8f6` | Warm White |
| `--ink` | `#1a2f5e` | Navy Blue |
| `--ink-soft` | `rgba(26, 47, 94, 0.75)` | — |
| `--ink-deep` | `#10244a` | Night navy — every button shadow |

### Accents

| Token | Hex | Sheet name |
|---|---|---|
| `--pink` | `#ff4f8b` | Heart Pink |
| `--blue` | `#0f7daf` | Adventure Blue |
| `--sky` | `#59c8f6` | Sky Blue |
| `--gold` | `#f6a313` | Sunshine Gold |
| `--yellow` | `#ffd94c` | Star Yellow |
| `--green` | `#4faf4b` | Outdoor Green — Mint is too light to carry text |
| `--candy` | `#ff5fa2` | Candy Pink |
| `--mint` | `#73d78d` | Mint Green |
| `--lavender` | `#a88bff` | Lavender |
| `--purple` | `#7259ff` | Space Purple |

`--pink-deep` is `#10244a`, not a dark pink: the sheet defines no pink shadow and the
reference shadows every button navy.

### Character fills — aliases, not tints

These were once five pastels we mixed ourselves (`#ffd7e6` / `#c9e8f7` / `#ffe9c2` /
`#d3f3de` / `#e4dcff`) — the one standing invention in the palette. Every one is now a
colour the sheet names outright:

| Character | Token | Resolves to | `--ink` contrast |
|---|---|---|---|
| Jevika | `--pink-bg` | Candy Pink `#ff5fa2` | 4.55:1 |
| Joy | `--blue-bg` | Sky Blue `#59c8f6` | 6.77:1 |
| Brutus | `--gold-bg` | Star Yellow `#ffd94c` | 9.39:1 |
| Minku | `--green-bg` | Mint Green `#73d78d` | 7.27:1 |
| Pinki | `--purple-bg` | Lavender `#a88bff` | 4.79:1 |

They are **saturated, not pale.** Eight sections consume these five tokens, so changing one
reaches the whole theme at once.

> **Never tint text with its own card's solid — always `--ink` on the fill.**
> The reference does tint, and copying it put Heart Pink type on a Candy Pink card at
> **1.10:1**, Sunshine Gold on Star Yellow at 1.50, Outdoor Green on Mint at 1.56. Carousel
> titles and every mega-menu character label were effectively invisible. Colour coding lives
> in the fill; the type stays navy. `--card-fg` / `--mc-shadow` survive only to colour offset
> shadows, where contrast does not apply.

Audit programmatically after any change to these five — walking every element whose computed
background is one of the fills, then every descendant that renders text, found eight header
failures a page-by-page eyeball had missed.

**Deliberate exceptions:** the hero field `#034CA2` / `#012F66` matches colour baked into the
hero artwork, and PDP colour swatches (`#2563eb`, `#e3d0ac` for Sand) depict physical garment
colours, not brand UI.

Tokens live in three places that must stay in sync: `assets/theme.css` `:root`,
`config/settings_schema.json` defaults, and `config/settings_data.json` values — the settings
win at runtime via `layout/theme.liquid`.

---

## 2 · Type

`html` is `62.5%`, so **1rem = 10px**. Rem values port directly from the React source.

| Role | Face | Token |
|---|---|---|
| Display headings | Baloo 2 800 | `--font-heading` |
| Condensed caps, buttons, nav | Big Shoulders Display 700 | `--font-accent` |
| Body | Nunito | `--font-body` |

All three load from one `@import` in `assets/theme.css`. The reference's Bunch, Toroka and
Gilroy are commercial licences we cannot ship.

> **Do not re-add `SofiaProSoft-*.otf`.** Those were Fontspring *demo* builds — demo licences
> forbid web embedding, and the builds are crippled: 96 glyphs, of which 29 including
> `& ' " - / ! @ ( ) 4` share the `.notdef` outline. Every apostrophe, ampersand and hyphen in
> body copy rendered as tofu on the live PDP.

```css
.hxxl { font-family: var(--font-heading); font-weight: 800;
        font-size: var(--heading-size); line-height: 1.08; letter-spacing: 0.01em;
        text-wrap: balance; margin: 0; }
/* --heading-size: 32px on phones; fluid 32–56px on wider screens. */

.accent-caps { font-family: var(--font-accent); font-weight: 700;
               text-transform: uppercase; letter-spacing: 0.05em; }
```

Product-card titles use the shared `--card-title-size`: 22–28px scaled by card
width, with a viewport-based fallback. They are not display headings. The phone
cast heading has its own 26–40px safe-zone scale, leaving all poses unchanged.

Default body text uses `--text-base: 1.4rem` (14px at the default browser font
setting), with a 1.5 line height, on desktop and mobile. Introductory text,
headings and controls retain their separate type sizes.

The clean-UI preview uses named roles, not independent section font sizes:

| Role | Phone | Larger screens |
|---|---|---|
| Campaign hero | 34–44px | 36–64px |
| Page/section heading | 32px | Fluid, up to 56px |
| Product title | 32px | Fluid, up to 52px |
| Intro/subheading | 18px | 18–20px |
| Ordinary prose, including product descriptions | 14px | 14px |
| Primary CTA | 18px | 18px |
| Native text input | At least 16px | At least 16px |

The scene's narrow-phone copy keeps its 26–40px safe-zone exception; character
poses, ground and entrance logic are unchanged. Supporting product navigation
and details now follow price, size/colour selection and the single purchase form
in the DOM, so reading and keyboard order agree with the visual hierarchy.

---

## 3 · Layout and shape

```css
.page-width { max-width: 1440px; margin-inline: auto; padding-inline: 2.16rem; }
@media (max-width: 749px) { .page-width { padding-inline: 1.5rem; } }

--radius: 1.6rem;
--ease: cubic-bezier(0.4, 0, 0.2, 1);        /* UI transitions */
--ease-out-slow: cubic-bezier(0, 0, 0.3, 1);
```

`--ease` is Material's UI-transition curve. It is **wrong for looping idle animation** — it
eases hard at both ends, so anything on `infinite alternate` dwells at each extreme and snaps
through the middle. Use a multi-point keyframe path on `linear` instead; see `falling-scroll`.

The `#jjw-blob` clipPath is defined once in `layout/theme.liquid`. Reference it with
`clip-path: url(#jjw-blob)`; never redefine the geometry. Always pair with an
`@supports not (clip-path: url(#jjw-blob))` fallback to `border-radius`.

---

## 4 · The button

Two stacked layers on one clip path; the shadow slides to zero on hover.

```html
<div class="btn-wrap">
  <span class="btn-shadow"></span>
  <a class="btn">Label</a>
</div>
```

```css
.btn-wrap   { position: relative; display: inline-block; }
.btn-shadow { position: absolute; inset: 0; z-index: 1;
              background: var(--btn-shadow-color, var(--ink-deep));
              transform: translate(4px, 4px);
              clip-path: url(#jjw-blob);
              transition: transform 0.3s var(--ease); pointer-events: none; }
.btn        { position: relative; z-index: 2;
              display: flex; align-items: center; justify-content: center;
              width: 100%; min-height: 5.2rem; padding: 1.4rem 2.4rem;
              font-family: var(--font-accent); font-weight: 700;
              font-size: var(--button-text-size); line-height: 1.2;
              letter-spacing: 0.05em; text-transform: uppercase;
              background: var(--btn-bg, var(--pink));
              color: var(--btn-fg, var(--ink-deep));
              clip-path: url(#jjw-blob);
              transition: transform 0.2s var(--ease); }
```

Offset is **4px** on buttons and menu controls, **2px** on selected browsing pills.

> Button label is **night navy, not cream**. Pink on cream is 2.92:1, and the clamp floor
> (16px bold) sits below the 18.66px large-text cutoff, so it needs the full 4.5:1. Night navy
> on Heart Pink is 4.91:1 and passes at every step of the clamp. **Any override that swaps
> `--btn-bg` for a dark fill must swap `--btn-fg` back to cream.**

---

## 5 · Shared classes

| Class | Purpose |
|---|---|
| `.page-width` | Page gutter, 1440px cap |
| `.hxxl` | Display heading |
| `.accent-caps` | Condensed uppercase label |
| `.btn-wrap` / `.btn-shadow` / `.btn` | The signature button |
| `.jjw-pill` | Solid Sky Blue nav pill, 5.4rem min-height |
| `.jjw-card` / `.jjw-grid` | Product card and its grid |
| `.rte` | Admin-authored rich text |
| `.marquee` / `.marquee__track` / `.marquee__group` | 24s linear, content repeated so `-50%` loops |
| `.scroll-trigger` + `.animate--fade-in` / `.animate--slide-in` | Reveal on scroll |
| `.visually-hidden` | Screen-reader-only |

`.jjw-card` / `.jjw-grid` / `.jjw-pill` are **unscoped on purpose** — `.jjw-pill` renders on
both `/search` and the collection page, so section-scoped rules would not reach both.

The prose class is **`.rte`, not `.jjw-rte`**: Shopify's policy pages already emit
`class="rte"`, so one rule set styles both those and `main-page`. Anything rendering
admin-authored rich text should use it, and must sit on `--white` — `--blue` links are 4.34:1
on cream (fails AA) and 4.59:1 on white.

---

## 6 · Section conventions

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
  })();
</script>

{% schema %} ... {% endschema %}
```

All human-visible copy comes from settings or blocks. Never hardcode it in markup.

**Responsive overrides must come after the base rule.** Media queries add no specificity, so a
plain rule later in the file silently wins.

**A `richtext` setting must never be emitted inside a `<p>`.** It brings its own `<p>`, and the
nested one closes the outer tag early, so the copy escapes the class styling it. Use a `<div>`
plus `:where(p) { margin: 0 }`.

---

## 7 · Character colour pairs

Derived from the `character:` tag by `snippets/character-pair.liquid`.

| Character | bg / fg |
|---|---|
| Jevika | `--pink-bg` / `--pink` |
| Joy | `--blue-bg` / `--blue` |
| Brutus | `--gold-bg` / `--gold` |
| Minku | `--green-bg` / `--green` |
| Pinki | `--purple-bg` / `--purple` |

Default to blue when no tag matches. Where a product carries several `character:` tags, prefer
the one matching the collection being viewed — taking the last tag makes everything blue, since
tags arrive alphabetically.

---

## 8 · Page topology

| Template | Sections, in order |
|---|---|
| `index` | hero, marquee-banner, featured-collection, find-us, falling-scroll, split-content, focus-carousel, rich-text, social-marquee, social-icons |
| `product` | main-product, bundle-banner, fabric-story, split-content, featured-collection |
| `collection` | main-collection, product-trust |
| `cart` | main-cart, bundle-banner, featured-collection |
| `search` | main-search |
| `page` | main-page |
| `page.contact` | main-page (title only), contact-form |
| `404` | main-404 |
| `list-collections` | main-list-collections |

`cart-drawer` is rendered from `layout/theme.liquid`, not a section group, so the Section
Rendering API can address it as `cart-drawer`. `whatsapp-button` lives in `footer-group.json`.

**Sections declared in a template get only the blocks that template specifies.** A section's
`presets` block list applies only when a merchant adds it through the theme editor — forgetting
this leaves marquees and carousels rendering as empty bands.

---

## 9 · Snippets

| Snippet | Role |
|---|---|
| `character-pair` | The one place the character → colour mapping lives; outputs a single word, meant to be `capture`d |
| `product-card` / `collection-card` | Grid cards |
| `product-accordions` | The white PDP info card — three rows split by a 2px `--sky` rule |
| `product-highlights` | Bullet summary between title and price; metafield → derived from option values → settings fallback |
| `header-card` | One character card, rendered by **both** the desktop mega panel and the mobile drawer |
| `review-stars` | Judge.me badge; renders nothing when the metafield is absent |
| `size-guide` | `<details>` inside the Size fieldset |

---

## 10 · Out of scope

Checkout and the order-status page are Shopify-hosted and not themeable on this plan —
brandable only through the Checkout editor in admin. Equally true of a headless build.

**Do not build `templates/customers/`, and do not link to `/account`.** The store runs
`NEW_CUSTOMER_ACCOUNTS`, under which classic customer templates are never rendered. Use
Shopify's `<shopify-account>` web component, styled through its custom properties
(`--shopify-account-color-accent` and friends), which inherit through the shadow boundary.
Accent is `--blue`, not `--pink`: the sheet uses 14–16px button text, where pink on cream is
about 2.9:1 and misses AA.

**`templates/policy.liquid` is never rendered** — Shopify serves `/policies/*` itself and
injects `.shopify-policy__container` markup into the theme layout. Style those classes,
scoped under `#MainContent` to win on specificity.
