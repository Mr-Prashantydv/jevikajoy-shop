# Shop policy drafts

The store has **one** policy today: Privacy. The other four below do not exist, so
`/policies/refund-policy`, `/policies/shipping-policy`, `/policies/terms-of-service` and
`/policies/contact-information` all 404, and the footer legal column has a single link.

These could not be created from here — the Shopify connection lacks the
`write_legal_policies` scope, and `shopPolicyUpdate` refuses without it. Paste each file
into **Settings → Policies** in admin instead.

`{{ shop_name }}`, `{{ email }}`, `{{ phone }}`, `{{ address }}` and `{{ last_updated }}`
are Shopify's own policy variables — leave them as-is and Shopify fills them in. The
existing Privacy policy already uses them.

Once the policies exist, add them to the **Footer legal** menu (handle `footer-legal`),
which currently holds Privacy alone. `sections/footer-group.json` already renders that
menu as the second footer column.

## Numbers that are assumptions, not facts

The shipping rates are read from the store's real delivery profile and are correct. These
are not — confirm or change each one before the store takes an order:

| Where | Claim | Confirm |
|---|---|---|
| Shipping | Dispatch within **2 business days** | Is that achievable? |
| Shipping | India Standard **3–7 days**, Express **1–3** | Ask the courier |
| Shipping | International **10–21 days** | Ask the courier |
| Refund | **7-day** return window from delivery | Standard for Indian D2C; yours may differ |
| Refund | **First exchange free** | This is a real cost commitment |
| Refund | Refund issued **5–7 business days** after inspection | |
| Refund | Damage/wrong-item reports within **48 hours** | |
| Terms | Governing law **Haryana, India** | Matches the registered address |

## Also outstanding

The store's contact email is **botfit41@gmail.com**. It is what the Contact page, the
contact form and every policy variable resolve to. A brand address (hello@jevikajoy.shop)
would read very differently to a customer deciding whether to trust a Rs. 599 order.
