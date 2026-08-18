# Asset Manifest — every image slot on the homepage

The hard rule: **slot-for-slot**. Every image slot Partake fills, we fill — same dimensions,
same aspect ratio, same treatment. Nothing gets dropped or simplified away.

Status legend: ✅ have · ⚠️ have a stand-in · ❌ missing, blocks the section

---

## Blocker first

**All 12 products have zero images.** Shopify returns `featuredMedia: null` on every one.

This matters more than anything else here. Partake's product card *is* the product PNG —
`object-fit: contain`, transparent background, sitting on a flat pastel field. Without art,
our featured-collection renders as twelve empty coloured rectangles. No amount of CSS fixes that.

**Needed:** 12 tee shots, **transparent PNG**, square (2000×2000), tee centred with even margin.
Partake uses a second image per product for the hover swap — a different angle. Optional but
it's a measured behaviour (`.media--hover-effect`, opacity cross-fade `.4s`).

---

## Slot table

| # | Section | Slot | Spec | Status |
|---|---|---|---|---|
| 1 | header | logo | SVG preferred, ~300×83 | ⚠️ `jjw-logo.png` — PNG. SVG would be sharper |
| 2 | hero | full-bleed photo | 2048×1152, `object-fit: cover`, `100vh` | ⚠️ `jjw-desktop.jpg` / `kids-sky.jpg` — need a chosen hero |
| 2b | hero | *(alt)* video | `hero-bg.mp4` + `hero-bg-mobile.mp4` exist in the reference repo | ✅ available if you want a video hero |
| 3 | stickers | 2–4 floating decorations | transparent PNG, ~120–200px | ❌ character cut-outs or doodles |
| 4 | featured-collection | 12 × product PNG | 2000×2000 transparent | ❌ **blocker** |
| 4b | featured-collection | 12 × hover PNG | second angle | ❌ optional |
| 5 | find-us | logo marquee, 5+ marks | ~180px tall, mono or full-colour | ❌ retailer/press/certification marks — BIS, OEKO-TEX, organic-cotton certs would fit |
| 6 | falling-stickers | 3 falling items + shelf + badges | transparent PNG; shelf `bottom center / contain` | ❌ optional section, build last |
| 7 | split-content | founder / brand photo | portrait ~964×1133, `object-fit: contain` | ⚠️ `cast-group.jpg` works as a stand-in |
| 7b | split-content | 2 × badge overlays | square transparent, ~436px, sits at ~30% scale | ❌ e.g. BIS certified, 100% organic |
| 8 | focus-carousel | 3 dot images | **200×200 transparent** — these are the pagination | ✅ character faces — jevika, joy, brutus, minku, pinki |
| 9 | social-icons | 4 × 80px circles | round crops or icons | ⚠️ theme has `icon-instagram.svg`, `icon-facebook.svg` |
| 10 | footer | payment / trust marks | small marks | ⚠️ Shopify renders these itself |

---

## What I cannot copy, and why

Not a technical limit in either case — this is the same under a Liquid or a headless build.

**Fonts.** `Bunch-Bold`, `Toroka-CondensedBold`, `Toroka-Black`, `Gilroy-Medium` are commercial
licences. Substitutes, matched on weight and proportion:

| Theirs | Ours |
|---|---|
| Bunch-Bold — rounded geometric display | **Baloo 2** 800 |
| Toroka-CondensedBold — condensed caps | **Big Shoulders Display** 700 |
| Toroka-Black — heavy condensed | **Big Shoulders Display** 900 |
| Gilroy-Medium — geometric sans | **Sofia Pro Soft** Medium *(licensed, in `assets/`)* |

**Images.** Their cookie photography, badges, retailer logos, founder portrait and wordmark are
their brand assets and trademarks. Every one is a slot we fill with our own equivalent — which is
what you wanted regardless, since we sell tees with our characters, not cookies.

---

## What to make, in priority order

1. **12 product PNGs, transparent, 2000×2000 square.** Unblocks the biggest section on the page.
2. **Hero image** — one wide shot, 2048×1152, with room on the left third for the headline
   (their copy sits in a 670px box, left-aligned, vertically centred).
3. **Founder / brand portrait** for split-content, roughly 3:4.
4. **2 badge marks** — BIS certified, 100% organic cotton — square, transparent.
5. **5 certification / trust marks** for the Find-Us band marquee.
6. **Logo as SVG.**
7. *(optional)* Sticker cut-outs and falling-section art.

Character faces for the carousel dots are already in `assets/` — nothing needed there.
