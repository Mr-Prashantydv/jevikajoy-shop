# Migration to 1uz1hi-01

Updated 4 October 2026. Destination account: `jevikaandjoy@gmail.com`.

Latest complete recovery export: `../export-1uz1hi-01-20261004/README.md`.
It includes all 80 image masters and a fresh pull of the destination theme after the
approved hero redesign. This older prepared folder is retained as historical input.
Product/content import and domain transfer have **not** been completed. User now explicitly
requests an end-to-end transfer including the domain and prefers **Brave**, not Chrome.

## Completed

- Shopify CLI signed in to the destination account; access verified with `theme list`.
- Uploaded **JJW Migration**, theme ID **164825399535**, as an unpublished theme.
- Uploaded sections/schema first, then templates, section groups and settings.
- Pulled remote homepage settings and character code to a separate temporary folder.
  Homepage settings match the local JSON. Character code and layout match byte for byte.
- Pulled the whole remote theme. 82 files match by bytes or parsed settings; the remaining
  product template differs only by key order and Shopify dropping the unused
  `image_position` setting (the section neither reads nor declares that setting).
- Prepared `JJW-theme.zip`, `products.csv`, `products.json`, `media-manifest.json`
  and `content.json` from local backups. Catalog: 10 products, 172 distinct SKUs;
  media: 80 PNGs; content: seven smart collections, three menus and two pages.

## Remaining

- Check destination products and collections before import; no catalog contents have
  been inspected or changed yet. Only its original live Horizon theme was observed.
- Import products as drafts, upload images and assign one packshot per photographed colour.
- Recreate collections, menus and pages; verify links and gallery grouping.
- Review current inventory, product metafields, policies, shipping, discounts, taxes,
  apps/reviews and payment configuration. None is proven transferred by uploading a theme.
- Verify the assembled storefront, then publish and connect `jevikajoy.shop` through
  the new store's domain-ownership flow. Domain registration remains with GoDaddy.

## Access and recovery limits

The old `bnwvrc-04.myshopify.com` still returns HTTP 402. The structured catalog and
content snapshot originated from the earlier `00d611-p1` store, with subsequent corrected
product payloads and current local theme edits. This is a reconstruction, not a fresh
export of the frozen source. Prices and inventory in these files are historical.

Products CSV deliberately contains no local image paths in Image Src: Shopify requires
public image URLs there. Media are tracked separately by path, colour, alt text and hash.
The five unphotographed products remain unphotographed; Giggles has no Pink/Peach photos.

The destination public URL shows its password/“Opening soon” page, so a successful HTTP
response does not validate the JJW design. Brave briefly connected to the destination
Shopify Themes tab after the user enabled debugging, but its endpoint then closed before
catalog/domain inspection. User was asked to re-enable debugging and leave it on. CLI
theme access is verified. No browser credentials or session cookies are being extracted.

Preview: https://1uz1hi-01.myshopify.com/?preview_theme_id=164825399535

Editor: https://admin.shopify.com/store/1uz1hi-01/themes/164825399535/editor

Rebuild prepared files (does not upload):

```powershell
python docs/migration/prepare_migration.py --destination 1uz1hi-01.myshopify.com
```
