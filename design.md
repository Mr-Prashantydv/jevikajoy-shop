# JJW storefront design review

Updated: 6 October 2026. Working project: `D:/projects/JEVIKAJOY.SHOP`.

This is the new section-by-section decision log. The user says the shop looks good but is inconsistent and not clean, and wants to direct improvements to each section. Record those instructions here as they arrive. Specific spacing values have **not** been chosen yet.

The previous design system is preserved unchanged in [the earlier design document](docs/design-system-before-review-2026-10-06.md). It contains the brand colours, fonts, shared components and implementation conventions. [The previous UI pass](docs/ui-consistency.md) describes work already staged in an unpublished theme. Historical specifications and tests are context; newly requested decisions and current measurements must be labelled separately.

## Current review target

| Target | Verified on 6 October |
|---|---|
| [Live storefront](https://jevikajoy.shop/) | `JJW Migration`, theme **164825399535**, role `main`; HTTP 200 |
| [Earlier UI preview](https://jevikajoy.shop/?preview_theme_id=164840702191) | `JJW UI consistency preview`, theme **164840702191**, role `unpublished`; HTTP 200 |
| Local source | Custom Shopify Liquid theme; current folder contains changes beyond the live theme |

Review the live storefront by default. A decision based on the preview must name that preview explicitly. The review began with documentation only. The user subsequently selected Weekend Picnic artwork and requested the header over the image; both changes are now live and verified.

## How each instruction is recorded

For every section, keep the user's requested outcome and a concrete specification together:

- Top and bottom **padding inside the section**, recorded separately.
- Top and bottom **margin outside the section**, including the gap to neighbouring content.
- Left/right gutters, content maximum width and alignment.
- Heading-to-copy, heading-to-cards, card-to-card and content-to-button gaps.
- Image size/crop, card padding, button placement and section height where relevant.
- Desktop, tablet and mobile values or behaviour; never silently apply a desktop decision to phones.
- Source file and selector, agreed value versus a proposed value, and status: `requested`, `specified`, `implemented`, `verified`.

Use CSS pixels for measurements and identify the actual styled element. An outer Shopify wrapper with zero padding does not imply zero internal spacing. Record verbal directions such as “reduce the gap” immediately; leave the numeric value pending until specified or clearly proposed. Do not turn a proposal into an approved rule.

## Verified baseline

Fresh captures use isolated Brave at **1440x900 desktop** and **390x844 mobile**, with reduced motion. These are observations, not selected design targets. Full metrics, padding/margin arrays and screenshots are in [_probe/design-review-20261006](./_probe/design-review-20261006).

| Element on live shop | Desktop | Mobile |
|---|---|---|
| Header height | 113px | 80px |
| Common content side gutter | 21.6px | 15px |
| Hero heading size | 74.16px | 39px |
| Main section heading size | Mostly 86.4px | Mostly 40px |
| Product section inner top / bottom padding | 28.6px / 55px | 24px / 40px |
| Product heading bottom margin | 25px | 25px |
| Product carousel card gap | 40px | 12px |
| Blue standards card top / bottom padding | 36px / 16px | 27px / 12px |
| Blue standards heading top margin | 92px | 67px |
| Character scene height / bottom margin | 1080px / 15px | 624px / 15px |
| Story split section top / bottom padding | 60px / 60px | 45px / 45px |
| Testimonials top / bottom padding | 60px / 60px | 60px / 60px |
| Testimonials heading top / bottom margin | 50px / 30px | 50px / 30px |
| Closing text section fixed height | 183px | 183px |
| Closing text inner top padding / heading top margin | 40px / 20px | 30px / 20px |

The unpublished preview already has an 81px desktop header, 56px section headings and 24px side gutters. Its shared section-space token spans 40–80px, but some sections still use independent values. Those refinements are not live. No horizontal document overflow was observed at the two measured live widths; this is not a full functional or accessibility audit.

## Section queue

The header and hero changes below are live; the remaining sections await the user's direction. The order follows the home template plus shared header/footer sections.

| Section | Visible identifier | Source | Decision status |
|---|---|---|---|
| Header | Logo, menu, Find in Store, search/account/cart | `sections/header.liquid`; hero spacing in `sections/hero.liquid` | Transparent over homepage image at every viewport; live verified |
| Hero | Tees Every Kid Can Call Their Own | `sections/hero.liquid` | Weekend Picnic selected and live; responsive artwork verified |
| Benefits ticker | Organic cotton / certification band | `sections/marquee-banner.liquid` | Awaiting direction |
| Product carousel | Every Hero Has a Tee | `sections/featured-collection.liquid` | Awaiting direction |
| Standards / store card | Made to a Standard You Can Check | `sections/find-us.liquid` | Awaiting direction |
| Character scene | Room for Every Kind of Kid | `sections/falling-scroll.liquid` | Awaiting direction |
| Story panel | Heroes Made for Every Kid | `sections/split-content.liquid` | Awaiting direction |
| Testimonials | Loved by Little Humans | `sections/focus-carousel.liquid` | Awaiting direction |
| Closing message | Made for Play, Built to Last | `sections/rich-text.liquid` | Awaiting direction |
| Social photo strip | Declared locally; no visible section in live capture | `sections/social-marquee.liquid` | Review if needed |
| Social links | Declared locally; no visible section in live capture | `sections/social-icons.liquid` | Review if needed |
| Footer ticker | Benefits / shipping band | `sections/footer-marquee.liquid` | Awaiting direction |
| Footer | Logo, links, Join the JJW crew | `sections/footer.liquid` | Awaiting direction |

Product, collection, search, cart and drawers can be added when the user reaches them. Preserve the existing artwork, brand and working shopping interactions as the baseline for this spacing review.

## Decision log

| ID | User instruction | Specification | Status |
|---|---|---|---|
| D001 | Improve consistency and cleanliness; discuss each section | Record spacing, margins and layout decisions here | Review log prepared |
| D002 | Generate ten high-quality9:16 hero options with creative freedom | First batch generated without actual product/character inputs | Rejected by user for invented merchandise |
| D003 | Check what we sell and use our character references | Supply actual catalog garment images and inspected local character assets to every generation; preserve prints, colourway, front/back orientation and identity | Ten replacement portraits generated and visually reviewed; provisional |
| D004 | Also generate16:9 images, full landscape | Ten full-bleed desktop landscape counterparts, with the same merchandise and character references; preserve room for editable text | Ten landscapes generated and visually reviewed; provisional |
| D007 | Header is part of the image; header is transparent | Homepage image starts at top behind transparent navigation at every viewport; keep editable tablet/desktop copy below controls and phone copy after picture | Live on theme164825399535; preview9 and live6 responsive checks plus menu/search/Escape passed |
| D008 | Mobile text should be on the image, not below it | Absolute bottom overlay for phone headline/CTA; retain full portrait and transparent header; soft cream fade for readability | Live on theme164825399535; preview9 and live6 sizes plus menu/search/CTA checks passed |
| D006 | THIS IS GOOD USE THIS AS HOME PAGE (attached Weekend Picnic portrait) | Use exact selected941x1672 portrait on mobile and matching1672x941 landscape on desktop; preserve all three tee prints, editable headline/CTA and current live merchant settings | Live on theme164825399535; preview9 and live6 responsive checks passed |
| D005 | Likes JJW Cloud World with the actual five friends and merchandise; show more clothes and generate55 fresh16:9 variations | All five canonical friends in unchanged outfits, six displayed tees from three actual reference designs per image; vary ecosystem, scenery, lighting and staging; keep room for editable hero text |55 new landscape candidates generated and visually reviewed; final selection pending |

The current set is [the reference-based gallery](docs/hero-concepts/2026-10-06/catalog-corrected/gallery.html): ten corrected portraits plus ten landscapes. [The ZIP](docs/hero-concepts/2026-10-06/catalog-corrected/JJW-reference-based-20-hero-images.zip) includes all20 PNGs, actual reference copies, full prompts and provenance. Original generic concepts remain separately marked **rejected**, not candidates.

Verified source garments: yellow Tech Builder FRONT/Joy LEVEL UP; pink Adventure BACK/Pinki squirrel and compass; blue Giggles BACK/Minku monkey and WILD AT HEART; blue Brutus Boxer BACK/Joy and brindle boxer; peach Wander BACK/quotation and compass. The character references are Joy, Jevika, Pinki, Minku and Brutus from the actual local assets. Printed source wording, including LIVE ADVANTAGES, was not editorially corrected.

Native outputs are941x1672 portrait and1672x941 landscape, approximately9:16 and16:9. No resizing/upscaling was applied. Main print identity, colour and garment-side placement were visually checked; exact print geometry and tiny lettering remain provisional. Joy's canonical lightning costume in garden option09 was repaired before its landscape counterpart was generated. Studio option06 desktop includes the actual cast as a creative variant; its portrait is product-only.

The user prefers the Cloud World concept direction. The next set is [55 new landscape variations](docs/hero-concepts/2026-10-06/cloud-world-55/gallery.html), grouped into11 Cloud,11 Nature,11 Discovery,11 Adventure and11 Wonder worlds. [Download all55 with references and prompts](docs/hero-concepts/2026-10-06/cloud-world-55/JJW-cloud-world-55-landscapes.zip). Each uses the five canonical friends and three actual garment reference styles, with larger displays of repeated stock. Six hanging tees were requested; some candidates have a seventh or a different stock mix, as recorded in the [visual review](docs/hero-concepts/2026-10-06/cloud-world-55/visual-review.md). All native files are1672x941, approximately16:9, copied unchanged. Clear environmental-signage errors in01/19 and distant extra people in31 were repaired; originals are preserved locally. Tiny lettering and exact print geometry remain provisional. Some layouts reduce clear headline space or hide lower bodies behind clothing displays; their per-image notes identify this.

The gallery loads55 distinct files on desktop and mobile, with11 ready images per family, no horizontal overflow, working modal navigation/Escape and a self-contained offline snapshot. Checks and hashes are in the deliverable folder. The user subsequently selected the Weekend Picnic portrait (option07 from the20-image set) and requested it on the homepage. It is now live at https://jevikajoy.shop/ using the exact selected portrait on phones and matching landscape on desktop. Only the hero section and two new untouched image assets were uploaded. A fresh live-theme baseline and preflight preserved merchant settings and homepage template. The unrelated UI preview was not published. These campaign scenes do not establish new global character/world canon.


### Current hero measurements (D006 artwork, D007 transparent header, D008 mobile overlay)

These values were implementation choices to preserve the selected artwork, not separately dictated numeric targets.

| Treatment | Implemented value | Purpose/status |
|---|---|---|
| Desktop from991px | Top padding0; native1672/941 media ratio; imagecontain/right top | Full landscape and all3teeprints preserved; verified |
| Tablet750-990px | Section top padding0; copy inner top padding112px | Image starts behind transparent navigation; heading clears controls; verified |
| Phone below750px | Section top padding0; portrait941/1672 ratio; imagecontain/center top | Entire selected portrait behind transparent navigation, including blue tee; verified |
| Desktop copy | Max widthmin(560px,40vw); top/bottom padding40px; left paddingclamp(20px,5vw,80px) | Editable copy uses blanket space beside products |
| Phone copy | Absolute layer within image, aligned bottom; padding24px all sides; max width480px | Headline/CTA overlay selected photograph; soft cream fade behind copy |
| CTA | Top gap24px desktop/tablet,16px phone; button horizontal padding36px | Existing Shop the Squad link to /collections/all preserved |
| Typography | Desktop44-76px retained; phone clamp(30px,8vw,40px), line height1.08 | Compact phone heading fits over image without reaching navigation |

Validation on6October2026: Shopify preview164913742063 passed9viewports320-1920px; fresh public live context confirmed theme164825399535 and passed6viewports, no page errors/overflow, correct image sources and CTA navigation. Three uploaded files re-pulled byte-identically; homepage template and merchant settings unchanged. Evidence: [_probe/hero-picnic-20261006](./_probe/hero-picnic-20261006). Theme Check has no hero offenses; an existing unchanged size-guide HTML issue and5unrelated warnings remain. Fine generated garment lettering remains provisional.

D007 validation on 6 October 2026: removed the previous 112px tablet and 84px phone outer hero spacers. The header itself was already transparent, so only `sections/hero.liquid` was uploaded. The image starts at y=0 and the closed header background is transparent at all tested widths. Preview passed nine sizes; fresh live passed six sizes, with menu/search opening, Escape closing and Shop the Squad navigation verified. Hero source matches the remote file byte-for-byte; header source, homepage template and merchant settings are unchanged. Evidence: [_probe/header-overlay-20261006](./_probe/header-overlay-20261006). The browser verifier now waits for repaint after Escape; an immediate style read in the first live run was transiently stale.

Follow-up visibility check, 6 October: user reports old artwork/header spacing. Fresh plain-home live visit again passed six sizes. Reproduced preview persistence: opening preview164840702191 then the plain homepage keeps the old hero and unpublished theme despite the address showing only `jevikajoy.shop/`. Visiting `https://jevikajoy.shop/?preview_theme_id=` clears that preview and restores live164825399535, the picnic desktop image and image top0. This is a confirmed reproduction, not direct inspection of the user's in-app browser. Screenshots/script in `_probe/header-overlay-20261006/check-preview-session.cjs` and `plain-home-after-preview.png` / `exit-preview.png`. No further storefront code change was necessary.

D008 correction on 6 October: the earlier mobile layout intentionally stacked editable copy below the photograph, but the user confirmed it must overlay the image. This supersedes D006/D007 phone copy placement. Phone hero height now equals the portrait height, with no extra text panel. Image pixels/framing stay unchanged; the lower photograph fades behind text. Nine preview widths and six fresh-live widths passed image/copy bounds, header clearance, correct sources, no overflow, menu/search/Escape and CTA navigation. Only hero source uploaded; remote hero matches staged bytes and header/template/settings are unchanged. Evidence: [_probe/mobile-hero-overlay-20261006](./_probe/mobile-hero-overlay-20261006). Restore that folder's `live-before/sections/hero.liquid` to revert this specific overlay.

## Project quality and housekeeping

**Verdict:** substantial useful theme and artwork; cluttered workspace and inconsistent documentation.

- Keep the active theme: **88 source/artwork files, about 24.6 MiB**, with shared brand/type tokens, reusable product snippets, keyboard/reduced-motion support and locale-aware cart code.
- Keep photography masters (`product-images/`, about 507 MiB) and migration recovery material. Archives are useful but do not belong in the day-to-day working surface.
- `docs/` is about 541 MiB; `_probe/` was about 290 MiB before this review. They mix valuable evidence with old exports and experiments.
- `jjw/` is a separate Shopify app starter, not the storefront theme; its demo route provides no demonstrated storefront value.
- Root HTML/JSON downloads, numeric filenames and zero-byte files are debugging clutter. Four root text files are cookie jars; treat them as private scratch data during any future cleanup. Values are not included here.
- `README.md` still describes Dawn. `AGENTS.md` includes old store/theme commands and conflicting historical facts. The preserved design document also contains an outdated gutter example. Verify current targets before future uploads.
- The working tree contains substantial pre-existing edits. A future implementation must reconcile remote merchant settings with scoped changes; this review did not clean up files or upload the checkout.
