# PDP build log

Working list for the product-page items in the CRO audit. Updated as each one lands.

> **Store status: HTTP 402 Payment Required.** The storefront, the Admin API and
> `shopify theme push` are all frozen on a Shopify billing issue — the CLI returns
> `Error (Code: 402): Unavailable Shop`. Everything below is **written but not pushed**, and
> none of it is live-verified. Resolve the billing issue, then run the push command at the
> foot of this file and work through the verification checklist.

| # | Item | Status |
|---|---|---|
| PDP-1 | Star rating below product title | 🟡 built — blocked on Judge.me app embed |
| PDP-2 | Short description as bullet points | 🟢 written — awaiting push |
| PDP-3 | Payment method icons below ATC | 🟢 written — will render nothing until a gateway is configured |
| PDP-4 | Product trust badges below ATC | 🟢 written — awaiting push |
| PDP-5 | Customer review widget | 🟡 built — blocked on Judge.me app embed |
| PDP-6 | You May Also Like | 🟢 written — awaiting push |
| PDP-7 | Sticky Add to Cart on mobile | 🟢 written — awaiting push |

Legend: 🟢 code complete, unverified · 🟡 code complete, blocked on a merchant action ·
✅ verified rendering on the preview theme.

---

## PDP-1 — Star rating below product title

**Status:** built in Phase 2. Not visible yet.

`snippets/review-stars.liquid` prints `product.metafields.judgeme.badge`, rendered under the
`<h1>` in `main-product.liquid` and on the cards in `main-collection.liquid` and
`snippets/product-card.liquid` (search + drawer).

Suppressed when the badge reports zero reviews — a catalogue-wide grid of "No reviews" reads
worse than no star row at all.

**Blocker (merchant action):** the Judge.me app embed is not enabled in this theme, so its
script never loads and the badge, which ships `display:none`, stays invisible. Theme editor →
Settings → App embeds.

## PDP-2 — Short description as bullet points

**Status:** written. New file `snippets/product-highlights.liquid`, rendered between the title
and the accordions.

Three sources, in order:

1. `product.metafields.custom.highlights` (a `list.single_line_text_field`) — per-product, and
   the only thing that can say something specific about one tee. Not populated on any product
   yet; the API is down, so it could not be seeded.
2. **Derived from the product itself** — colourway count, and the age span read off the size
   values. These count rather than assert, so they cannot drift: add a colour in admin and the
   bullet counts it the same day.
3. The `highlight_fallback` setting — claims true of every tee.

The age scan takes the lowest and highest leading number across all size values rather than
first-and-last, because `giggles-tee` stores its six overlapping ranges out of order
(4-5, 6-7, 9-10, 5-6, 7-8, 11-12).

Nothing here invents a fact: every bullet is either typed by the merchant or counted off the
product.

## PDP-3 — Payment icons below ATC

**Status:** written, and expected to render **nothing** today.

Built on `shop.enabled_payment_types` + the `payment_type_svg_tag` filter, so the icons are
always exactly what this store can actually take — never a stock strip of card logos it
cannot. The store currently reports zero configured gateways, so the row is empty until
payments are set up in admin. That is the correct behaviour, not a bug.

Toggle: `show_payment_icons`. Label: `payment_label`.

## PDP-4 — Trust badges below ATC

**Status:** written. New `trustbadge` block type on `main-product`, four declared in
`templates/product.json`: free shipping over Rs. 999, 7-day easy exchange, 100% organic
cotton, secure checkout.

Each is an inline SVG, not an uploaded image — the house rule is that image-borne text becomes
real text. Icons sit on a Sky Blue disc with a navy stroke (7.5:1).

**Note:** these blocks had to be declared in `product.json`. A section's `presets` block list
only applies when a merchant adds the section through the theme editor — a section declared in
a template gets only the blocks that template names. This has bitten the theme three times.

The old `trust_line` setting was **cleared**: it read "Soft cotton, kind to skin. Easy 7-day
exchanges", which said two of the four badges again in prose directly underneath them.

## PDP-5 — Customer review widget

**Status:** built in Phase 2. Same Judge.me embed blocker as PDP-1.

`product.metafields.judgeme.widget` at the foot of the section, guarded on *content* not
presence — Judge.me stores the literal string `<div></div>` for a product with no reviews,
which is not blank and would otherwise render 60px of empty margin.

## PDP-6 — You May Also Like

**Status:** written.

**Correction to an earlier claim.** I reported that `featured-collection` renders no products
anywhere because no template sets its `collection`. That was wrong — there has always been a
`collections.all` fallback at the top of the file. I checked the schema default and the `if`
but not the top-of-file `assign`, and the curl I "confirmed" it with was hitting the 402 error
page, whose HTTP status I had not checked.

The real defect was smaller and genuine: the carousel had **no relevance and no exclusion**, so
"More From the Squad" on a PDP listed all ten tees *including the one being viewed*.

Now the source resolves: merchant's collection → on a product page, that product's own
character collection (only when it holds more than one product) → all products. And the
product being viewed is skipped.

## PDP-7 — Sticky Add to Cart on mobile

**Status:** written. Phones only (≤749px) — desktop already has a `position: sticky` buy
column, so a second button there would be noise.

- **Not a second `<form>`.** The bar's button submits the real one via the `form` attribute.
  Two forms posting the same variant could double-add, and a duplicated hidden variant input
  is one more thing to keep in sync with the picker.
- Price and disabled state mirror the real button from the existing variant-change handler, so
  the two can never disagree about whether the chosen size is in stock.
- Revealed only once the real Add to Cart has scrolled out of view *downwards*, so it never
  covers the button it stands in for, and never appears above the fold.
- Its own `IntersectionObserver`, not the theme's `.scroll-trigger`: this has to toggle both
  ways, where scroll-reveal fires once and unobserves. Separate IIFE too, because the variant
  script returns early on products with no picker and the bar must still work there.
- `z-index: 9` — above content and above the WhatsApp bubble's 8, below the header overlay's
  10 and far below the cart drawer's 70/71.
- The WhatsApp bubble is lifted clear via `--jjw-sticky-atc-offset`, set on `body:has(...)`
  because the bubble is rendered by `footer-group` and is not a descendant of this section.

---

## When the store is back

Local pre-flight (schema JSON, filters in conditions and render arguments, richtext in `<p>`,
tag balance) passes for all four files:

```bash
python _probe/validate_liquid.py
```

Push — section first, then the template, per the ordering trap:

```bash
rm -rf assets/.claude-flow && shopify theme push --store 00d611-p1.myshopify.com --theme 194587852932 --path . --only sections/main-product.liquid --only sections/featured-collection.liquid --only sections/whatsapp-button.liquid --only snippets/product-highlights.liquid
```

Then, separately:

```bash
shopify theme push --store 00d611-p1.myshopify.com --theme 194587852932 --path . --only templates/product.json
```

Verify by checksum, not by the CLI's success box — a `--only` push has silently kept stale
content twice in this theme.

### Verification checklist (nothing below has been done)

- [ ] Highlight bullets render on all 10 products, and the age span is right on `giggles-tee`
      (should read 4–12 across 6 sizes) and on a normal product (4–12 across 4 sizes)
- [ ] Four trust badges render below the buy button and wrap sensibly at 390px
- [ ] Payment row is absent (expected) — recheck once a gateway is configured
- [ ] "More From the Squad" excludes the current product, and shows the character's
      collection where that character has more than one tee
- [ ] Sticky bar: hidden at page load, appears after scrolling past the button, submits and
      opens the cart drawer, disables on a sold-out size, and does not cover the WhatsApp
      bubble once a number is set
- [ ] Sticky bar absent on desktop
- [ ] Contrast audit over the PDP, and a 44px touch-target sweep on the new controls
