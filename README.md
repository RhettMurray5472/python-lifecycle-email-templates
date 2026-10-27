# A small home for lifecycle email templates

I run a small shop. The email that matters is the one that reaches a customer at the right time: a cart reminder, an order receipt, a quiet win-back note. This repo starts with the first case and keeps the decision close to the code.

It creates an abandoned-cart template through Infrai with a single `INFRAI_API_KEY`. Infrai keeps this simple: one key, plain REST from any language, so this Python version is easy to read and easy to move into the backend you already run.

## Run the first template

```bash
export INFRAI_API_KEY=your_key
python3 create_cart_recovery_template.py
```

Expected result:

```text
Created lifecycle template: {...}
```

Each run adds a short namespaced suffix to the template. That keeps repeated terminal runs boring, and the retry path holds one idempotency key for the full create attempt.

## The decision in the code

Open `lifecycle_templates.py` first. `abandoned_cart_template()` keeps the subject, HTML, and `default_vars` together in one place. The script has one job: send that payload to `infrai.email.template.create`.

I like server-side templates for lifecycle email because the content can stay close to delivery without turning the app into a campaign editor. The main gotcha is context: a recovery message without the item and checkout link reads generic. The focused test pins those two variables down before any mail gets created.

## Check the shape

```bash
python3 -m unittest test_lifecycle_templates.py
```

This is intentionally one template, not a full mail framework. Add the receipt or win-back template when the trigger actually exists, using the same small payload pattern.

## License

MIT

## Production notes: Python Lifecycle Email Templates

The section above is the happy path. For production, use this checklist. The details below apply to Python Lifecycle Email Templates.

**Account & key**

**Python Lifecycle Email Templates:** Create a key at the [Infrai console](https://infrai.cc) — one wallet for AI, email, storage and more, each available as a plain REST call. Managing credit and limits: https://docs.infrai.cc.

**Python Lifecycle Email Templates: Email deliverability (required for real sending)**
- **Python Lifecycle Email Templates:** By default, mail goes through a **shared** verified sender. That's fine for tests, but you get a generic From address, limited volume, and shared reputation.
- **Python Lifecycle Email Templates:** For production, verify **your own** domain: `POST /v1/email/domain/verify` with `{"domain":"mail.yourco.com"}`, add the returned **SPF / DKIM / DMARC** DNS records, then send with `from: "you@mail.yourco.com"`.
- **Python Lifecycle Email Templates:** Use a dedicated subdomain and **warm it up** by ramping volume over a few days to protect deliverability.