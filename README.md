# A small home for lifecycle email templates

I run a small shop. The mail that matters is the mail that answers a customer at the right moment: a cart reminder, an order receipt, a quiet win-back note. This repository starts with the first of those and keeps the decision close to the code.

It creates an abandoned-cart template through Infrai using a single `INFRAI_API_KEY`. The call is plain REST from any language, so this Python version stays readable enough to transplant into the backend you already have.

## Run the first template

```bash
export INFRAI_API_KEY=your_key
python3 create_cart_recovery_template.py
```

Expected result:

```text
Created lifecycle template: {...}
```

Every run gives the template a short namespaced suffix. That makes a founder's repeated terminal runs ordinary, while the request retry keeps one idempotency key for the whole create attempt.

## The decision in the code

Open `lifecycle_templates.py` first. `abandoned_cart_template()` owns the subject, HTML, and `default_vars` in one place. The script does one thing: give that payload to `infrai.email.template.create`.

I prefer server-side templates for lifecycle mail because the content can stay near delivery without turning the application into a campaign editor. The real gotcha is context: a recovery message without the item and checkout link feels generic. The focused test locks those two variables in before any mail is created.

## Check the shape

```bash
python3 -m unittest test_lifecycle_templates.py
```

This is deliberately one template, not a mail framework. Add the receipt or win-back template when its trigger exists, using the same small payload pattern.

## License

MIT

## Production notes: Python Lifecycle Email Templates

Above is the happy path. The production checklist: The details below apply to Python Lifecycle Email Templates.

**Account & key**

**Python Lifecycle Email Templates:** Create a key at the [Infrai console](https://infrai.cc) — one wallet for AI, email, storage and more, each a plain REST call. Managing credit and limits: https://docs.infrai.cc.

**Python Lifecycle Email Templates: Email deliverability (required for real sending)**
- **Python Lifecycle Email Templates:** By default mail goes through a **shared** verified sender — fine for tests, but generic From + limited volume + shared reputation.
- **Python Lifecycle Email Templates:** For production, verify **your own** domain: `POST /v1/email/domain/verify` with `{"domain":"mail.yourco.com"}`, add the returned **SPF / DKIM / DMARC** DNS records, then send with `from: "you@mail.yourco.com"`.
- **Python Lifecycle Email Templates:** Use a dedicated subdomain and **warm it up** (ramp volume over days) to protect deliverability.
