# Transferring 00d611-p1 to hello@jevikajoy.com

Researched and cross-checked against current Shopify Help Center pages and the Terms of
Service (verified 2026-08-23). Every claim below survived an independent attempt to refute it
against a primary source, except where marked otherwise.

## The one-line answer

**A frozen store cannot be transferred.** The transfer control lives inside admin, and admin
is inaccessible while frozen. The outstanding bill has to be paid by the *current* owner
before anything else is possible — there is no path where the new owner (hello@jevikajoy.com)
pays it instead, and no way to skip straight to a transfer.

> [help.shopify.com/frozen-store](https://help.shopify.com/en/manual/your-account/manage-billing/billing-charges/frozen-store):
> "If your store is frozen, then you can't access your Shopify admin and customers can't view
> your store," and reactivation is required before "accessing your store information,
> transferring a domain, or beginning to sell again."

## Step 0 — reactivate (blocking, must happen first)

1. Log in to `00d611-p1.myshopify.com/admin` **as the current store owner**. This is a hard
   requirement — no other role can do it.
2. Pay every unpaid invoice, in full, one at a time if there's more than one.
3. **If it's been more than 30 days since the last bill was issued**, reactivation also forces
   you to re-pick a plan and pay the upcoming subscription cycle up front — a second charge on
   top of the arrears.
4. Reactivation usually clears within minutes; if the store is still frozen ~30 minutes after
   payment, contact Shopify Support.

**Deadline that matters:** Shopify's Terms of Service (§5.4) reserve the right to terminate the
account if fees stay unpaid **60 days after the suspension date** — not the friendlier
"2 years" figure that gets quoted for voluntary store closures (that number is real, but it's
the retention window *after* termination, not a safe runway to delay in). Reactivate sooner
rather than later.

There is no grace period Shopify will grant on request — "Shopify doesn't grant extensions or
grace periods for bill payments."

## Step 1 — pre-transfer checklist (do this before initiating)

The transfer moves the **shop object** — catalogue, theme, collections, menus, pages,
policies, the automatic discount, shipping profiles — untouched. It does **not** move
money-and-identity items, all of which the current owner should update first or agree on with
the incoming owner:

- [ ] **Billing card** — stays on the store attached to the old owner until replaced. It can
      keep being charged after transfer if nobody updates it.
- [ ] **Outstanding balance at the moment of transfer** — becomes the new owner's debt if not
      cleared first ("the new owner is responsible for paying any outstanding bills").
      Given this store was just frozen for non-payment, clear it to zero before transferring,
      or agree explicitly who's covering it.
- [ ] **Store email** (Settings → General) and **notification sender email**
      (Settings → Notifications) — two different settings, neither moves with ownership. The
      account/login email is the only thing tied to the owner personally.
- [ ] **Payout/bank details** for every active payment method — this store has **none
      configured**, so nothing to redo here. Genuinely good news: an active Shopify Payments
      account is a documented **hard blocker** on transfer (Capital/Credit block outright; an
      active Balance must be emptied via Support first). Zero payment providers means none of
      that applies.
- [ ] **jevikajoy.shop (the vanity domain)** — does **not** ride along with the ownership
      transfer. It's a separate transaction, blocked while frozen (domains disconnect on
      freeze and must be manually reconnected after reactivation), and if it's a
      Shopify-managed domain there's a 60-day eligibility window for domain transfers
      specifically. Handle this as its own step, after the store transfer.

## Step 2 — the transfer itself

Current path (shipped Dec 2024 — older guides describing "Settings → Users → Transfer
ownership" are describing a moved control):

1. **Settings → General → "Organizations and store transfers" → Manage**
2. **"Transfer store to a new owner outside your business"** → Continue
3. Re-authenticate if prompted (no blanket 2FA mandate for this store — Shopify will ask based
   on how recent your last login was)
4. Enter `hello@jevikajoy.com` → Transfer

Since hello@jevikajoy.com already owns a store elsewhere, **this is the right route** — no
invitation, no staff role needed first. The recipient gets an email, logs in, and chooses to
add the store to an existing organization, start a new one, or keep it standalone.

- **It's cancellable only while pending** ("Cancel transfer" on the same Settings → General
  screen) — once hello@jevikajoy.com accepts, there's no documented undo.
- **The outgoing owner is not removed** — you keep a staff-level login on the store afterward
  unless the new owner deliberately removes you. Owner-level permissions (billing, payout
  info) become restricted to you immediately, though.
- One point I could not verify either way: whether a pending transfer expires after some
  number of days if unaccepted. The commonly repeated "7 days" figure belongs to a different
  Shopify flow (Partner client-transfer) and isn't confirmed on the merchant transfer page.

## What needs zero action

- **Judge.me** — bound to the shop, not the owner. No reinstall, no re-auth. (It only breaks
  on a move to a *different* `.myshopify.com` store, which this isn't.)
- **Offline app access tokens** — scoped to the shop+app pair, survive an owner change.
- **Products, collections, menus, pages, policies, the 15%-off-3 discount, shipping zones,
  the theme** — none of this needs re-creation. The transfer carries the whole store.

## What still needs doing after the transfer

- Email DNS authentication (DKIM/SPF/DMARC) for the sender address — gated behind an *active
  paid plan*, so it can't be set up until after reactivation anyway.
- The incoming owner's own Shopify CLI auth, if they'll be the one pushing theme changes —
  the CLI session used to build this theme doesn't transfer with the store.
- Reconnecting the custom domain once it's separately transferred.

## Backup — what to pull now, while admin still loads (billing screen only)

Admin is documented as inaccessible while frozen, with one exception: you can view and pay
billing history. There is likely nothing else exportable right now. Once reactivated, before
transferring, the fuller export options open up — but most of what a Shopify CSV export
*can't* carry (menus, pages, policies, collection rules, metafield definitions, shipping
config) is **already captured**:

- **`docs/migration/store-snapshot.json`** — a pre-freeze Admin API capture of the shop, theme,
  all 10 products (options, variants, tags, SKU pattern including the known Blue/Black SKU
  collision), all 9 collections with their smart-collection rules, all 3 menus verbatim, both
  pages, the Privacy policy, the 15%-off-3 discount, both shipping zones with real rates, and
  the Judge.me state.
- **`docs/product-copy/descriptions.json`** — all 10 product descriptions.
- **`docs/policies/*.html`** — the 4 unpublished policy drafts (Refund, Shipping, Terms,
  Contact Information).
- **`product-images/JJW-{04,05,06,08,12}/`** — full-resolution masters for the 5 photographed
  products. Confirmed live: `cdn.shopify.com` was still serving these at full resolution while
  the storefront itself returned 402, so nothing is at risk there either.
- **The theme itself** — this git repo, branch `scratch-theme`. Portable as-is; only two
  cosmetic URLs in `config/settings_schema.json` reference the domain.

None of this is required for the transfer to work — the transfer carries everything live on
the store regardless. It's insurance against the 60-day termination clock, in case reactivation
doesn't happen in time.

## Sources

Everything above is drawn from, and cross-checked against:
- [help.shopify.com — Frozen store](https://help.shopify.com/en/manual/your-account/manage-billing/billing-charges/frozen-store)
- [help.shopify.com — Change or transfer ownership](https://help.shopify.com/en/manual/your-account/manage-orgs-and-stores/change-transfer-ownership)
- [help.shopify.com — Billing extensions](https://help.shopify.com/en/manual/your-account/manage-billing/billing-extensions)
- [help.shopify.com — App charges (freeze/unfreeze of recurring charges)](https://help.shopify.com/en/manual/your-account/manage-billing/billing-charges/types-of-charges/third-party-charges/app-charges)
- [help.shopify.com — Deactivate a store](https://help.shopify.com/en/manual/your-account/manage-orgs-and-stores/manage-pricing-plan/deactivate-store)
- [help.shopify.com — Transferring Shopify-managed domains](https://help.shopify.com/en/manual/domains/managing-domain-ownership/transferring-shopify-domains)
- [help.shopify.com — Roles managed by Shopify](https://help.shopify.com/en/manual/your-account/users/roles/roles-managed-by-shopify)
- [shopify.com/legal/terms](https://www.shopify.com/legal/terms) §5.4, §14.4
- [shopify.com/legal/privacy/merchants](https://www.shopify.com/legal/privacy/merchants)
- [judge.me — Migrating reviews between two Shopify stores](https://judge.me/help/en/articles/13045740-migrating-reviews-between-two-shopify-stores)
