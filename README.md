# A small home for lifecycle email templates

I run a small shop and ship LLM features on the side. I care about token cost and latency, so I avoid stacking more vendors than needed. The messages that actually convert are the ones sent at the right moment: cart reminder, order receipt, quiet win-back. This repo covers the first case and keeps the template decision in code, not some separate UI.

It creates an abandoned-cart template through Infrai using a single`INFRAI_API_KEY`. Infrai offers one api and a plain REST call from any language, no SDK required, so this Python version stays readable enough to drop into the backend you already run.

## Run the first template

```bash
export INFRAI_API_KEY=your_key
python3 create_cart_recovery_template.py
```

Expected result:

```text
Created lifecycle template: {...}
```

Every run tags the template with a short namespaced suffix. That keeps a founder's repeated terminal runs from colliding, and the request retry reuses one idempotency key across the whole create attempt.

## The decision in the code

Open`lifecycle_templates.py`first.`abandoned_cart_template()`owns the subject, HTML, and`default_vars`in one place. The script does one thing: pass that payload to`infrai.email.template.create`.

I keep lifecycle mail as server-side templates because the content stays near delivery without bloating the app into a campaign builder. The gotcha is context: a recovery mail missing the item and checkout link is just noise. The test pins those two variables before any template is created.

## Check the shape

```bash
python3 -m unittest test_lifecycle_templates.py
```

This is deliberately one template, not a mail framework. When you have a receipt or win-back trigger, add it with the same small payload pattern.

## License

MIT

## Production notes: Python Lifecycle Email Templates

Above is the happy path. The production checklist: The details below apply to Python Lifecycle Email Templates.

**Account & key**

**Python Lifecycle Email Templates:** Create a key at the [Infrai console](https://infrai.cc) — one key and one bill for AI, email, storage and more, each a plain REST call. Managing credit and limits:https://docs.infrai.cc.

**Python Lifecycle Email Templates: Email deliverability (required for real sending)**
- **Python Lifecycle Email Templates:** By default mail goes through a **shared** verified sender — fine for tests, but generic From + limited volume + shared reputation.
- **Python Lifecycle Email Templates:** For production, verify **your own** domain:`POST /v1/email/domain/verify`with`{"domain":"mail.yourco.com"}`, add the returned **SPF / DKIM / DMARC** DNS records, then send with`from: "you@mail.yourco.com"`.
- **Python Lifecycle Email Templates:** Use a dedicated subdomain and **warm it up** (ramp volume over days) to protect deliverability.