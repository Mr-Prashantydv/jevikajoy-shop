# Sunlit playground hero — 4 October 2026

The user rejected the royal-blue studio concept and asked for an entirely new concept.
The new campaign shows two children wearing the yellow Tech Builder and peach Wander
tees in a warm, sunlit handmade playground. Cream, mint, coral and sunshine gold replace
the blue field. The existing headline and shop button remain editable HTML.

## Artwork and implementation

## Current live status — 4 October 2026

User approved the campaign and explicitly requested publication on jevikajoy.shop.
Theme164825399535 is now live, domain HTTPS works, and the password page was disabled
by the user. The requested full-width fix replaces desktop `contain` with top-anchored
`cover`, removes the empty image strip, and fills the opening wide-screen viewport.
Tablet navigation clearance and phone image/copy flow are preserved. The hero renders
immediately instead of waiting for scroll-reveal callbacks. Character animation is unchanged.
Frontend UI Engineering guided the responsive sizing and visible-content checks.
An isolated **Brave** fixture passed12sizes320–1920, including1536×748 and1920×720.
Screenshots375/768/1536 were visually inspected; a separate live Shopify screenshot
confirms actual header, image fill and no pose-controller overlay. Local screenshots are
in OS Temp/jjw-hero-v3-layout-L1TdKU; live evidence is _probe/hero-live-after-fill.png.
Earlier generation/deployment notes below describe the historical unpublished version.

Generated with the **built-in image-generation tool**, using saved garment photographs
as design references. These are AI-generated campaign images, not untouched product
photographs. Merchant review of small garment lettering is still required before publication.

- Desktop: `assets/jjw-hero-v3-desktop.png`, 1586 × 992, 1,831,143 bytes.
- Mobile: `assets/jjw-hero-v3-mobile.png`, 1086 × 1448, 1,705,645 bytes.
- Original and v2 images retained; no artwork was overwritten.

The redesign skill guided hero-only typography, spacing and responsive layout changes:
navy headline, small sunshine shadow, cream background, header clearance, full desktop
artwork with contain, and phone copy in normal flow below a square image window. The
portrait's empty lower quarter is cropped; the children's faces, prints and shoes remain
visible. No change to the character animation, its tuned coordinates, homepage template,
other sections, or merchant image/tag controls.

Only `sections/hero.liquid` and the two v3 PNGs were uploaded to **JJW Migration**
(theme **164825399535**, **1uz1hi-01.myshopify.com**), which remains **unpublished**.
A preflight pull confirmed the remote hero matched the previous local hero and the remote
homepage hero settings were empty, so no merchant override was replaced.

## Verification limits

- All three uploaded files were pulled back and their SHA-256 hashes matched local
  files. Remote verification folder:
  `C:/Users/krish/AppData/Local/Temp/jjw-hero-v3-verify-d29368e7b6a74d989665189e0e098bac`.
- Shopify Theme Check reports no hero offenses. The overall theme check still fails on
  an untouched HTML nesting error in `snippets/size-guide.liquid`; five unrelated warnings
  remain in the layout and product section. They were not changed for this request.
- `_probe/verify_hero_v3.cjs` renders the real hero CSS/default artwork and copy branches
  in an isolated Chrome fixture, not a complete Shopify/Liquid storefront.
- Ten viewport checks passed: 320×568, 360×640, 375×812, 390×844, 430×932, 749×1024,
  768×1024, 1024×768, 1440×900 and 1920×1080. Image loading/source selection, horizontal
  overflow, CTA bounds, following-section flow and phone copy separation were asserted.
- Screenshots at 375, 768 and 1440 pixels were visually inspected. Latest local evidence:
  `C:/Users/krish/AppData/Local/Temp/jjw-hero-v3-layout-QiwNHB`.
- Full Shopify storefront rendering/header interaction remains unverified: the existing
  Chrome browser-harness daemon was not running. The isolated fixture omits the full header,
  other sections, reveal behavior and shared SVG button clip path.

Preview: [Unpublished theme](https://1uz1hi-01.myshopify.com/?preview_theme_id=164825399535).

## Reference roles

1. `product-images/JJW-08/mustard/JJW-08-mustard-04-packshot-stickers.png`:
   exact yellow tee garment/print reference; not its poster background or external stickers.
2. `product-images/JJW-12/peach/JJW-12-peach-02-back-lifestyle.png`:
   peach tee print and fit reference; not its blue set.
3. Generated desktop v3: composition/identity/style reference for the mobile counterpart.

## Desktop prompt

Use case: ads-marketing.
Asset type: landscape Shopify homepage hero artwork for Jevika & Joy's World children's cotton tees.
Primary request: an entirely NEW creative concept: a warm sunlit imaginary playground with real children, not a studio still-life or a recoloured product arrangement.
Input images: Image 1 is the exact yellow Tech Builder tee GARMENT PRINT reference; ignore its navy poster backdrop and stickers. Image 2 is the peach Wander tee worn by a child, a GARMENT PRINT and fit reference only, not the composition or blue background to recreate.
Scene/backdrop: a premium handmade play-world in a cream seamless indoor set (#fff7e8), warm natural sunlight entering from upper left. At the far right, a low mint-green play tunnel with a rounded opening, a large golden paper sun behind it, and one restrained coral paper hill form. Tactile painted wood and cut-paper textures, joyful but uncluttered.
Subjects: two happy Indian children around 7-9 years old playing together on the RIGHT half. A smiling boy nearer camera wearing the yellow Tech Builder cotton tee, olive shorts and everyday canvas sneakers, torso mostly frontal so the exact Level Up character graphic reads clearly. A girl a little behind to his right wearing the peach Wander tee and denim shorts, in a natural three-quarter back pose preparing to throw a cream paper plane, so the back print is visible. She turns her head slightly toward her friend. Natural candid action with believable anatomy, feet touching the cream floor and realistic contact shadows. Entire children including shoes remain in frame.
Composition: wide 16:10 landscape. Leave LEFT 45% almost entirely uninterrupted warm cream negative space for live navy headline and shop button. Children and play props occupy x52-96%, y19-90%; main yellow shirt at x64-77%, girl at x80-91%. Top 15% calm to fit fixed site navigation. Never cover the blank left headline area with body parts, props or busy shadows. Wide editorial kidswear campaign, not a website screenshot.
Lighting/materials: beautiful soft angled sunlight, gentle long shadows, visible cotton knit and believable folds, natural skin texture, bright joyful expressions, clean high-end fashion editorial realism.
Garment constraints: faithfully preserve yellow tee graphic including vertical LEVEL UP., existing Joy cartoon character and small printed marks from Image 1. Preserve peach back wording NOT ALL WHO WANDER ARE LOST., compass and mountain outline from Image 2. Do not transfer external poster stickers onto clothes. Do not invent a different logo or print.
Avoid: blue background, blue studio platform, hanging or floating shirts, pedestal product arrangement, extra people, extra toys, excessive confetti, baked-in headline, UI, buttons, separate slogans, badges, borders or watermark. No text except the existing garment prints.

## Mobile prompt

Use case: compositing.
Asset type: mobile Shopify homepage hero, portrait 3:4.
Input image 1 is the DESKTOP CAMPAIGN to adapt. Preserve its two children, identities, yellow Tech Builder tee with Level Up print, peach Wander back-print tee, outfits, handmade mint and coral playground and golden paper sun, warm sunlit photographic style and cream #fff7e8 ground. No blue background.
Primary request: recompose this same campaign for a MOBILE screen, not a screenshot or a website mockup. Reserve top 15% calm empty warm cream for navigation. Place the two full children, their shoes, paper plane and restrained playground backdrop together in the middle upper frame at x8-92%, y17-62%. Children are naturally playing and have believable contact with the ground, no anatomical distortion, no extra children. Keep every face and garment graphic visible, no limb or shoe cropped. The boy slightly in front at left, girl at right in three-quarter back pose. Preserve the reference garment designs and existing wording; don't simplify or replace prints.
Entire bottom 33% (y67-100%) is uninterrupted light warm cream negative space for live navy HTML headline and pink shop button, free of props, feet, long shadows, plants or printed text. Lighting fades naturally to flat cream in the bottom area. Top of sun must be below the navigation space.
Natural cotton fabric, candid joy, premium editorial kidswear campaign. No heading, button, UI, badge, separate text, watermark or border; only existing garment prints.
