# Customer flow check — 2026-10-23

Walked the live store (jevikajoy.shop, `1uz1hi-01`) as a shopper in Edge, signed in as the
customer who placed order **#1004** (Brutus Boxer Tee, 4-5 Y / White, Cash on Delivery,
₹978, placed 23 Oct 12:41, status Confirmed / unfulfilled). Nothing was submitted, cancelled
or returned.

## Order, cancel, return

| Step | What a shopper finds | Kind |
|---|---|---|
| Sign in | Works (`<shopify-account>` sheet → shopify.com sign-in). Page is headed **"My Store"**. | Admin: store name |
| Order list / detail | #1004 shows correctly: item, ₹599 + ₹379 shipping, COD pending, address. | — |
| Cancel | **No cancel option anywhere.** Order page has only "Buy again". The refund policy says to email before dispatch. | Shopify limitation (new customer accounts have no self-serve cancel) |
| Return (Shopify) | No "Request return" on the order page. Shopify only offers it after fulfilment, and only if self-serve returns are on (Settings → Customer accounts / Returns rules). | Admin setting, untested until shipped |
| Return (Shiprocket) | `jevikajoy.shiprocket.co/tracking` finds order 1004 ("Order is under processing"). A **Return** link exists in the page but stays hidden — presumably until delivery. | Untestable until delivered |

## Problems

1. **Shipping charged ₹379 on a ₹599 domestic order** (New Delhi). The rate is named
   **"मानक"** (Hindi for "Standard") even though the account page is in English. 63% of the
   item price is likely to stop COD buyers; check the rate in Settings → Shipping and delivery.
   Free shipping is advertised over Rs 999 — confirm that rate exists.
2. **Refund policy has a blank phone number** — it ends "Email jevikaandjoy@gmail.com or call ."
   (admin: Settings → Policies).
3. **Three different contact identities.** Refund policy: `jevikaandjoy@gmail.com`. Contact page
   and Shiprocket: `botfit41@gmail.com`, +91 70112 81878. Shiprocket page title:
   "BOTFIT ENTERTAINMENT PRIVATE LIMITED". Pick one support address and use it everywhere.
4. **Footer has no policy or help links** — only "Search" and "Shop All Tees". The `footer` /
   `footer-legal` menus appear not to exist on this store (admin: Navigation).
5. **Footer credits "Design: Wonderkind" and "Development: Has Merit Studio"** — the
   reference site's agencies, linking to `#`. Defaults in `sections/footer.liquid` (theme fix).
6. **404s:** `/policies/shipping-policy`, `/policies/terms-of-service`,
   `/policies/contact-information` (drafts in `docs/policies/`), `/pages/returns` and
   `/pages/how-its-made` (templates exist; pages not created in admin).
7. **Store name never set** — "My Store" in every tab title and on the sign-in and account pages.

## Works

- Refund policy is live, dated 23 Oct 2026, and matches the PDP's 7-day returns note.
- Contact form has name, email, phone, order number and message.
- Shiprocket tracking finds the order by number.

## Not checked

- Mobile layout of the account and Shiprocket pages.
- The actual return and cancel submissions (need a shipped / delivered order, and the owner's go-ahead).
