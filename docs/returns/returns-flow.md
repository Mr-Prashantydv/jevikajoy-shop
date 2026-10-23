# Returns flow — audit and plan (2026-10-21)

Store `1uz1hi-01.myshopify.com` (jevikajoy.shop), live theme `164840702191`.
Walked as a customer who has a tee that doesn't fit and wants to send it back.

## 1. The flow today — every dead end

Checked on the live site (HTTP status by `curl`, page content in the browser).

| Step a customer tries | What happens | Verdict |
|---|---|---|
| Scroll to the footer for "Returns" / "Refund policy" | The footer's link columns render **one link: Search**. The `footer` menu on this store holds only Search, and the `footer-legal` menu **does not exist** here, so even Privacy is unlinked. | Dead end |
| Visit `/policies/refund-policy` | **404** | Dead end |
| `/policies/shipping-policy`, `/terms-of-service`, `/contact-information` | **404** each. Only `/policies/privacy-policy` is 200, and nothing links to it. | Dead end |
| Visit `/pages/returns`, `/pages/return-policy`, `/pages/faq`, `/pages/track-order` | **404** | Dead end |
| Search the site for "return" | Nothing on the homepage mentions returns, refunds or exchanges. | Dead end |
| PDP | Badge **"7-day easy exchange"** (`templates/product.json` → `trust_return`). Accordion "Shipping & Returns" (`snippets/product-accordions.liquid:187`, hardcoded): *"Unworn items with tags attached can be returned within 7 days of delivery."* No link to a policy or a way to start one. | Promise with no route |
| Header → account icon (`<shopify-account>`) | Opens Shopify's passwordless sign-in; `/account` 302s to `shopify.com/84225917167/account`. New customer accounts list a shopper's orders, but a **"Request return"** button only appears if *Self-serve returns* is switched on in admin, and it can't be confirmed from outside. Assume it is off. | Order lookup yes, return no |
| Order tracking | No Shiprocket (or other) tracking page. Shopify's own order-status page is the only tracking. | No return entry point |
| Contact page `/pages/contact` | **Works.** Form with order-number field, plus email `botfit41@gmail.com`, phone +91 70112 81878 and the Gurugram address. | The only working route |
| WhatsApp button | Not rendered: `whatsapp-button` has no number set (`sections/footer-group.json`). | Missing |

**What a customer can actually do today:** guess that the contact form is the way, write in, and
wait. Nothing tells them the window, the conditions, who pays for pickup, or how they get their money back.

Also noticed (not returns, but on the same walk):
- The footer prints **"Design: Wonderkind"** and **"Development: Has Merit Studio"** linking to `#`.
  Those are the reference site's credits, still filled into the footer's `credit_*` settings.
  Clear them in the theme editor (footer section). They are other sessions' files, so they are not touched here.
- Every `<title>` reads **"My Store"**: the store name is unset (Settings → General).
- Contact email is a personal Gmail (`botfit41@gmail.com`), and every policy variable resolves to it.

### Do the claims match a policy?

| Where | Says | Draft policy (`docs/policies/refund-policy.html`) |
|---|---|---|
| PDP badge | 7-day easy **exchange** | 7 days from delivery, return **or** exchange, first exchange free |
| PDP accordion | **returned** within 7 days, unworn, tags on | same conditions, plus unwashed, original packaging |
| `main-product` default sub-copy | "Easy 7-day exchanges" | consistent |

The numbers agree. The problem is that **no published policy backs any of them**. The draft also
promises things the store has not set up yet: a free first exchange, with reverse pickup paid by
the store, and a refund in 5–7 business days. Those become true only once the setup below is done.
Publishing the policy is the step that makes the badge honest, so it comes first.

## 2. Target flow, end to end

There are two places a return request can be raised. **Use one, not both**, or requests split across two queues.

- **A. Shiprocket tracking page (recommended).** The tracking link in every shipping SMS, WhatsApp
  message or email carries a *Return* button. Reverse pickup, QC and courier booking happen in the
  same panel that shipped the order. It handles exchanges as well as returns.
  **It needs the forward shipment to go through Shiprocket**, so orders must be fulfilled via Shiprocket.
- **B. Shopify self-serve returns** (Settings → Customer accounts → *Self-serve returns and
  cancellations*). It is free and built in, and the shopper uses the sign-in the header already has.
  But **it cannot do exchanges**, which is the very thing the PDP badge promises, and you would still
  book every reverse pickup by hand in Shiprocket. Keep it **off** if you choose A.

Flow with A:

```
Customer                         Store (you)                        Shiprocket / courier
────────                         ───────────                        ────────────────────
Order delivered ───────────────────────────────────────────────── tracking page link in SMS/email
Finds "Returns" in footer / PDP
  → /pages/returns explains rules,
    links to the tracking page
Opens tracking page → Return/Exchange
  picks item, reason, size (exchange)
                                 Alert → Returns › Return Request
                                 check vs. policy (≤7 days, unworn)
                                 Accept ─────────────────────────── return order created ("New Returns")
                                         or Decline (customer told why)
                                 Schedule pickup, choose courier ── courier collects (QC at door if on;
                                                                     a failed QC = pickup declined)
                                                                    item arrives at your pickup address
                                 Inspect
                                 ├ Exchange: new size ships as a new forward order (Shopify order → Shiprocket)
                                 └ Refund:  Shopify admin → order → Refund
                                            · prepaid → back to original payment method
                                            · COD → collect UPI/bank details from the customer, pay manually
                                            · (Shiprocket can auto-refund only as Shopify *store credit*)
Customer notified (Shopify refund email / Shiprocket SMS)
```

## 3. Shiprocket setup — what the user must do

These steps are **yours**. They grant access to the store, take KYC and bank data, or spend money,
so I will not do them. Menu names are from Shiprocket's help centre and may have moved; follow the panel.

1. **Create or sign in to a Shiprocket account** at app.shiprocket.in. KYC typically asks for PAN
   (and GSTIN if registered) plus identity proof. Enter these yourself.
2. **Install "Shiprocket: eCommerce Shipping"** from the Shopify App Store (developer: Shiprocket,
   Gurugram; free plan plus paid tiers; 3.9★ from about 658 reviews). Approve the permissions in
   Shopify admin. Or connect from Shiprocket → Channels → Shopify. Recent reviews complain about weight-discrepancy
   charges, so declare accurate weights. A folded kids' tee with packaging is roughly 0.2–0.3 kg; weigh one.
3. **Company / pickup profile ("set up the profile"):** you fill in these fields:
   - Company / brand name (Jevika & Joy's World) and brand logo
   - Pickup address nickname, contact name, phone (OTP-verified), email
   - Full pickup address and **pincode**. This is also where returns are delivered unless you add a
     separate return address. The contact page shows 11th Floor, Sector 63, Gurugram 122098. Confirm that it
     is where parcels can actually be collected.
   - GSTIN (if any), PAN
   - Bank account for COD remittance, if COD is enabled
   - Wallet recharge. Shiprocket deducts freight, **including reverse pickups**, from a prepaid wallet.
4. **Turn on returns on the tracking page:** Buyer Experience → Brand Boost → *Returns* toggle → Save.
   Optionally set a custom tracking domain (e.g. `track.jevikajoy.shop`) and note the final tracking-page URL.
   **Send me that URL.** The theme's returns page links to it.
5. **Return settings:** Settings → Return Settings.
   - Return QC: turn on, so the courier checks for an unworn tee with tags at the door.
   - Refund settings: leave *Auto refund (store credit)* off unless you want store credit as the default.
   - Set return reasons and the window to match the published policy (7 days).
6. **Fulfil orders through Shiprocket** from now on. The return button only exists for Shiprocket shipments.
7. **Notifications:** make sure shipping SMS/email go out with the tracking link. That link is the customer's return entry point.

### Shopify admin steps (also yours)

8. **Settings → Policies → Refund policy:** paste `docs/policies/refund-policy.html` after
   confirming the numbers in `docs/policies/README.md`: 7 days, **first exchange free**, refund in 5–7
   business days, 48-hour damage window. Update the *How to start a return* paragraph to the
   tracking-page route (wording below). Also paste Shipping, Terms and Contact while you're there.
9. **Settings → General:** set the store name (fixes "My Store").
10. **Online Store → Pages → Add page** "Returns & exchanges", handle `returns`, template
    `page.returns` once that template is pushed. Body: optional short intro.
11. **Online Store → Navigation:**
    - `footer` menu: add *Returns & exchanges* → `/pages/returns`, *Contact* → `/pages/contact`.
    - Create menu **`footer-legal`**: Refund policy, Shipping policy, Privacy policy, Terms of service.
      The theme already renders both menus.
12. **Settings → Customer accounts:** leave *Self-serve returns* **off** (option A).
13. Decide **COD**: if it is on, write the COD refund route (UPI/bank transfer) into the policy.

Suggested replacement for the draft's *How to start a return*:

> Open the tracking link from your shipping SMS or email (or go to our Returns page) and choose
> **Return / Exchange** within 7 days of delivery. We'll confirm, and a courier will collect the tee
> from your door — please keep it unworn with tags on. Can't find the link? Email {{ email }} with
> your order number.

## 4. Theme changes (proposed — test theme first, live only on your OK)

None of these touch the header, footer or `layout/theme.liquid` files other sessions are editing.
The footer links are **admin menu content** (step 11), not code.

1. **`sections/main-returns.liquid` + `templates/page.returns.json`:** a Returns page with:
   heading and intro from settings, 3–4 **step blocks** (request → pickup → inspect → refund/exchange),
   a conditions list (unworn, tags on, 7 days), a **"Start a return"** button whose URL is a setting
   (the Shiprocket tracking page; the button hides while that is blank), and links to the refund
   policy and contact page. Ink on white / cream per the brand rules. All copy lives in settings or blocks.
2. **`snippets/product-accordions.liquid`:** add one line under the hardcoded text: "Easy 7-day
   returns and exchanges — **how it works**" → `/pages/returns`. It is guarded so it prints only when that page exists
   (`pages['returns'] != blank`), so nothing links to a 404 before admin step 10.
3. **PDP badge:** keep "7-day easy exchange". It is true once the policy is published and step 4 is done.
   If you decide **not** to fund a free first exchange, change it to "7-day returns" in the theme editor.
4. **Contact form:** optional — add "Returns & exchanges" to the help-topic copy.

Nothing should go live before the refund policy is published. Otherwise the new page links to a 404.

## 5. Order of work

1. You: Shiprocket account + KYC, app install, pickup profile, wallet (steps 1–3).
2. You: confirm the policy numbers → publish the refund policy (step 8).
3. Me, on your OK: build theme changes 1–2 on a `shopify theme share` test theme and send the preview link.
4. You: returns toggle + return settings (4–5); send me the tracking-page URL.
5. You: create the Returns page and footer menus (10–11).
6. Me, on your go-ahead: push the theme changes live, then verify every link returns 200.
7. Optional, only if you ask: one test return on a real delivered order you choose. Shiprocket has no
   sandbox for reverse pickups, so a test return books a real courier and costs a real fee.

## Sources

- Shiprocket — enable returns on the tracking page: https://support.shiprocket.in/support/solutions/articles/43000536497
- Shiprocket — process a new return request: https://support.shiprocket.in/support/solutions/articles/43000536509
- Shiprocket — add a return order: https://support.shiprocket.in/support/solutions/articles/43000463528
- Shiprocket — QC for returns: https://support.shiprocket.in/support/solutions/articles/43000658274
- Shiprocket — auto refund (store credit only): https://support.shiprocket.in/support/solutions/articles/43000658284
- Shiprocket Shopify app: https://apps.shopify.com/shiprocket
- Shopify — self-serve returns: https://help.shopify.com/en/manual/orders/return-requests

## 6. Shiprocket account state (checked 2026-10-22)

- **Channels:** the Shopify channel "Jevika and Joy's World" (11127678) is *Disconnected*, last order sync
  29 Aug — that is the old frozen store. Do **not** "Reconnect" it; use **Connect** (Shopify) for
  `1uz1hi-01.myshopify.com`. A WooCommerce channel "BOTFIT ENTERTAINMENT PRIVATE LIMITED" is also
  disconnected (not JJW). Until the live store is connected, Shiprocket receives no JJW orders, so no
  tracking page and no return button exist.
- **Pickup address:** one, "Home", PRIMARY, VERIFIED — Kadarpur, Gurugram 122098 (contact ishant). It does
  not match the Contact page address (11th Floor, Sector 63). Its status switch looked pale; confirm it is on.
- **Return Settings — saved with the owner's go-ahead:** window 7 days; all SKUs returnable; auto-approve
  and auto-assign off; all reasons except "Performance not adequate". Reloaded and confirmed.
- **Exchange Settings is "Coming Soon"** in Shiprocket. Size exchanges are therefore handled as a return
  plus a new order for the new size, not a one-click exchange. The PDP "7-day easy exchange" badge is
  still deliverable that way, but the Returns page's step 1 should not promise an Exchange button on
  the tracking page until Shiprocket ships it.
- **Connected 2026-10-22:** Shopify channel **12664732** (`https://1uz1hi-01.myshopify.com`) shows
  *Connected*, last order sync 22 Oct 09:42 PM; Shopify lists "Shiprocket: eCommerce Shipping" under
  installed apps. The connect only completed when installed from the App Store listing (two installs
  started from Shiprocket's own Connect button never finished). Channel store name was **"My Store"** (now "Jevika & Joy's World" with the JJW logo, saved and re-checked 2026-10-22)
  and will print on labels, SMS, emails and the tracking page — fix it via Edit Channel (and set the
  store name in Shopify Settings → General). No logo uploaded yet. Inventory sync: never.
- **Brand Boost saved 2026-10-22** (reloaded and confirmed): tracking page
  **https://jevikajoy.shiprocket.co/tracking** (returns 200); website jevikajoy.shop; new JJW logo
  (`product-images/_brand/jjw-logo-shiprocket-square.png`); privacy link; support +91 70112 81878 /
  botfit41@gmail.com; **"Allow buyers to initiate return from the tracking page" ON**.
- Returns page (test theme #165506482415 only): "Start a return" now links to that tracking page, and
  step 1 says "choose Return … pick 'Size not as expected'" instead of promising an Exchange button.
