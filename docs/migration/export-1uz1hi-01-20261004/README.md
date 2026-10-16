# JJW recovery export and transfer status

Updated 4 October 2026. Destination: **1uz1hi-01.myshopify.com**, account
**jevikaandjoy@gmail.com**. Connected domain: **jevikajoy.shop**; registration stays
with GoDaddy. Do not transfer the registration to another registrar.

## Catalog and domain live; remaining settings transfer incomplete

The old **bnwvrc-04.myshopify.com** still returns HTTP 402. This is a recovery from saved
data, not a fresh full export of that frozen store. Unknown remote-only data is not proven
preserved. The structured catalog originated in the earlier **00d611-p1** store and includes
later SKU and size-order fixes. Historical prices and stock require review before launch.

`JJW-store-export.zip` contains the catalog CSV/JSON, all 80 image masters, media labels
and hashes, collection/menu/page definitions, historical shipping and discount reference,
policy drafts, and `JJW-theme.zip`. The theme ZIP was built from a fresh CLI pull of the
unpublished destination theme **164825399535**, including the approved sunlit hero and
current merchant editor settings. The historical root ZIP was left unchanged.

Verified export contents: **10 products, 172 unique variant SKUs, 80 photos, 20 colour
packshots, seven smart collections, three menus, two pages and 88 theme files**. CSV SKUs
match JSON; every saved photo hash and colour-first alt label matches. ZIP entries were
CRC-tested and compared against the source files. Products remain draft/unpublished in
the import files. Five products and Giggles Pink/Peach have no saved photos.

## Required next steps

1. Finish the Boys/Girls collections, navigation, pages and reviewed store settings.
   Reconnect apps;
   payment credentials, app subscriptions and billing do not migrate with a theme.
2. Verify shipping rates, the advertised automatic discount, payment authorization and
   reviewed policies before accepting orders. Verify the assembled storefront and checkout.
   Merchant-only billing, payment authorization and unreviewed legal commitments still
   require the merchant. Never mark a file export as a completed remote migration.

Not captured reliably: orders/customers, all metafield definitions/values, redirects,
markets/taxes/duties, notification templates, other Content Files, app/review state, and
remote-only changes since the snapshot. Policy drafts are not confirmed published policies.

## Live progress, 4 October 2026

Brave access confirmed the destination account and initially empty product catalog/file library.
All 80 product photos were uploaded and original CDN PNG dimensions checked against masters.
A one-product canary import was verified before importing the remaining nine without overwrite.
All 10 products are now ACTIVE and published to Online Store only: 172 variants, 80 photos,
20 colour packshots and 88 variant image bindings. Anonymous storefront comparison passed
with zero differences for handles, titles, descriptions, vendor/type/tags, SKU sets, prices,
size/colour option order, media alt labels and featured packshots. See `live-catalog-audit.json`
and `../audit_live_catalog.py`. Historical inventory is 5 per variant; physical stock is unverified.
Five products and Giggles Pink/Peach remain without photos, as in the recovery source.
The five character collections are saved and publicly checked against exact tag memberships:
Jevika 4, Joy 6, Brutus 1, Minku 1, Pinki 1. Boys/Girls and menus/pages/settings are unfinished.
One native product export was requested but no file was received; no native export comparison
is claimed. This verified public catalog comparison does not verify checkout or payment setup.
GoDaddy automatic connection completed; destination `shopify_verification` TXT is `UPUYUNCM`.
`jevikajoy.shop` is the new store's primary domain with working HTTPS. Theme **164825399535**
is now live at the user's explicit request; Horizon retained unpublished. User saved Private
mode off. Anonymous root requests return HTTP 200 without redirect to `/password` and report
our theme ID. Approved hero and cast render. At the user's request, the pose controller was
restricted to `request.design_mode` (theme editor only); public markup/scripts verified absent.
The ZIP is an immutable pre-transfer export; live status changes are outside its packaged README.

Shopify's domain procedure: https://help.shopify.com/en/manual/domains/add-a-domain/connecting-domains/verify-domain-ownership
