# JJW UI consistency pass

4 October 2026. Scope: shared home, collection, product, search and cart UI.
Delivery is an unpublished preview, not a live replacement.

## Clean-UI refinement, 5 October 2026

The user asked for a clean, consistent, good-looking modern UI. The baseline
screens showed oversized header controls, 86–105px section headings, competing
uppercase subheadings, and product navigation/details ahead of the buying controls.

Use the established JJW artwork and brand palette as the visual reference. The
design contract is calmer hierarchy, shared type roles, compact consistent navigation,
and a clear shopping sequence. Keep 14px body copy, at least 44px touch targets,
native inputs at least 16px, and the branded blob CTA; do not replace the character
identity with a generic neutral storefront. No new images or dependencies.

- Shared page/section heading: 32px phone, fluid to 56px desktop.
- Separate campaign hero (34–64px), product title (32–52px), and card title (22–28px).
- Intro/subheading 18–20px; ordinary rich text 14px; primary buttons 18px.
- Smaller desktop header; aligned phone controls; quieter outlined icon buttons.
- Browsing pills use readable Nunito instead of oversized condensed uppercase.
- Reduce unnecessary uppercase and spacing in collection and footer copy.
- Product DOM order: title, purchase block, supporting navigation/highlights/details.
  Preserve one purchase form, all age/colour choices, native disclosures and galleries.
- Keep the scene's narrow-phone type safe zone, all poses, art and one-shot animation.

Work from a fresh pull of preview164840702191; update only scoped CSS/section source.
Do not publish, update payment settings, or overwrite merchant settings/templates.
Fresh baseline: `_probe/clean-ui-before/audit.json` and screenshots.

Preview: https://jevikajoy.shop/?preview_theme_id=164840702191
Live remains `JJW Migration` (164825399535); preview is 164840702191.

## Original pass contract, 4 October

Keep JJW's brand-sheet colours, Baloo 2 / Big Shoulders / Nunito, blob CTAs,
approved warm hero artwork, cast coordinates, and 30%-entry animation.
The existing `DESIGN.md` and rendered store are the reference for this pass;
this is a refinement, not a new visual concept or a copy of another brand.

The shopper should find a tee, read its price and options, and add it to the
cart without fighting navigation or tiny controls.

- One character-colour resolver for featured, collection, search and cart cards.
  A character collection can intentionally prefer its own character on a multi-tag tee.
- Product titles scale with card width (22–34px), not display-heading size.
- Shared 15–24px page gutters, 40–80px section spacing, and 20px card radius.
- Menu, search and cart stay on one phone-header row down to 320px.
- Tabs, size/colour choices and quantity controls have at least 44px tap targets.
- Carousel arrows sit below cards; they never cover garment art or titles.
- Missing photos get an explicitly labelled placeholder, not another garment.
- Pink surfaces use navy text; the blue trust panel uses opaque cream headings.
- The phone cast heading fits above the characters; poses and ground stay unchanged.
- Preserve keyboard focus, native disclosure behavior and reduced-motion support.

Reject: colour/font replacement, invented product photos, character pose changes,
idle bobbing, scroll scrubbing, new checkout promises or invented reviews.

## Verification and release

Baseline: `_probe/ui-before/audit.json` and screenshots. Four public routes at
320 / 768 / 1440 returned 200 with no page errors or document horizontal overflow.
The narrow header still wrapped; the former overflow probe falsely counted
intentional offscreen slides, so it now accounts for clipped ancestors.

Stage from a **fresh remote theme pull**, applying only this pass's changed files.
Preserve live `config/settings_data.json`, templates and section-group configuration;
local versions contain unrelated merchant changes and must not replace them.
Add only the new photo-placeholder translation to the remote locale.

Check real Shopify preview rendering at phone/tablet/desktop widths and around
breakpoints. Exercise menu/search, carousel arrows, product options, size guide,
cart quantities, empty cart, keyboard focus and reduced motion.
Do not complete checkout, change payment credentials or publish automatically.

4 October results:

- 52 route/viewport checks across 13 widths, 320–1920px, passed: no page errors,
  broken loaded images, horizontal page overflow, wrapped header controls, or
  measured picker/header controls below 44px. See `_probe/ui-after-final/audit.json`.
- 40 interaction checks passed at 320 / 390 / 768 / 1440px: menu/Escape/focus,
  predictive search, carousel navigation/colour mapping, keyboard tabs, open
  size guide, variant/gallery updates, and cart 1 → 2 → 1 → empty. Giggles'
  six age choices are preserved. `_probe/ui-interactions/results.json`.
- Open size tables stay within the page and scroll internally. The first test
  wrongly assumed four columns; this merchant's chart has five, all retained.
- Scene checks passed at 320×568, 390×732, 390×844 and 768×900: heading clears
  the cast, entrance lands once, no later scroll-driven movement, identical poses
  at equal width across different phone heights. `_probe/ui-scene/results.json`.
- After the final scene-heading refinement, all 16 phone route/viewport checks
  were repeated at 320 / 360 / 390 / 430px and passed.
  `_probe/ui-after-cast-final/audit.json`.
- Remote re-pull: 22 source/config/artwork hashes matched the staged files;
  merchant settings, home template, footer group, hero and theme.js untouched.
- Theme Check: zero errors, five warnings (remote font hosts, block IDs and PDP
  complexity). `git diff --check` passed, with CRLF conversion notices only.

Tests used isolated desktop Brave at responsive sizes, not physical iOS/Safari
devices or a full screen-reader/axe audit. Shopify's preview toolbar is not part
of the storefront; tests use its native Hide bar control when testing bottom
cart links. No forced clicks, injected layout overrides, checkout or orders.

Before publishing, recheck for newer merchant edits to the live theme and
reconcile any changes to protected settings/templates. Publish this verified
preview only after owner approval; never push the whole dirty local checkout.

Missing product photography, unfinished navigation/page migration, payment
setup, shipping and the advertised discount remain separate launch work.

## Clean-UI verification, 5 October

- Final layout audit: 28 checks across home, collection, product and cart at
  320 / 390 / 749 / 750 / 768 / 1024 / 1440px. All returned 200; no page
  errors, loaded broken images, horizontal overflow or undersized sampled controls.
  `_probe/clean-ui-final/audit.json`.
- Type/structure checks: 30 cases across six routes and five widths. Confirmed
  body/prose14px, primary buttons18px, shared heading scale, card titles22–28px,
  native input sizes, purchase-before-details DOM order, one purchase form,
  all Tech Builder variants and no public pose editor. Checked small-button and
  pill hover contrast; blue+white measures4.59:1. `_probe/clean-ui-contract/results.json`.
- 40 interaction checks passed: menu/Escape/focus, search, carousel, keyboard tabs,
  size guide, variants/gallery, cart quantities/removal and all Giggles sizes.
  `_probe/clean-ui-interactions/results.json`. No orders or checkout submitted.
- Final scene checks passed at320x568,390x732,390x844,768x900: text clears faces,
  entrance remains one-shot, no bob/scrub, same-width poses match across heights.
  `_probe/clean-ui-scene-final/results.json`.
- Fresh remote pull matched all22 hashes:15 scoped source updates and seven
  protected settings/template/script/artwork files. Theme Check: zero errors,
  five existing warnings. `git diff --check` passed (CRLF notices only).

Preview164840702191 remains unpublished; live164825399535 was not replaced.
Tests used isolated desktop Brave, not physical Safari/iOS or a full accessibility audit.
