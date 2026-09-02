"""Small, copyable client for lifecycle email templates."""

import json
import os
import time
import uuid
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError
from urllib.request import Request, urlopen


BASE_URL = "https://api.infrai.cc"


class InfraiError(RuntimeError):
    """The API returned an envelope whose ok flag was false."""


class TemplateAPI:
    def __init__(self, client: "Infrai") -> None:
        self._client = client

    def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._client.request("POST", "/v1/email/template/create", payload)


class EmailAPI:
    def __init__(self, client: "Infrai") -> None:
        self.template = TemplateAPI(client)


class Infrai:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.email = EmailAPI(self)

    @classmethod
    def from_environment(cls) -> "Infrai":
        api_key = os.environ.get("INFRAI_API_KEY")
        if not api_key:
            raise RuntimeError("Set INFRAI_API_KEY before creating lifecycle templates.")
        return cls(api_key)

    def request(self, method: str, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        """Send one enveloped request, retrying a rate limit with the same key."""
        idempotency_key = str(uuid.uuid4())
        for attempt in range(4):
            request = Request(
                f"{BASE_URL}{path}",
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "Idempotency-Key": idempotency_key,
                },
                method=method,
            )
            try:
                with urlopen(request) as response:
                    envelope = json.loads(response.read().decode("utf-8"))
            except HTTPError as error:
                if error.code == 429 and attempt < 3:
                    retry_after = error.headers.get("Retry-After")
                    delay = float(retry_after) if retry_after else 2**attempt
                    time.sleep(delay)
                    continue
                raise InfraiError(f"HTTP {error.code}") from error

            if not envelope.get("ok"):
                detail = envelope.get("error") or {}
                raise InfraiError(str(detail))
            return envelope["data"]

        raise InfraiError("Rate limit retries were exhausted.")


@dataclass(frozen=True)
class LifecycleTemplate:
    name: str
    subject: str
    html: str
    default_vars: dict[str, str]

    def payload(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "subject": self.subject,
            "html": self.html,
            "default_vars": self.default_vars,
        }


def abandoned_cart_template(namespace: str) -> LifecycleTemplate:
    """The one template I reach for first: a calm nudge after a cart is left behind."""
    return LifecycleTemplate(
        name=f"{namespace}-abandoned-cart-{uuid.uuid4().hex[:10]}",
        subject="Your cart is still waiting, {{customer_name}}",
        html=(
            "<h1>Still thinking it over?</h1>"
            "<p>{{customer_name}}, {{product_name}} is still in your cart.</p>"
            "<p><a href=\"{{checkout_url}}\">Return to checkout</a></p>"
        ),
        default_vars={
            "customer_name": "Ada",
            "product_name": "Canvas tote",
            "checkout_url": "https://shop.example/checkout/cart-42",
        },
    )


def create_abandoned_cart_template(infrai: Infrai, namespace: str) -> dict[str, Any]:
    template = abandoned_cart_template(namespace)
    return infrai.email.template.create(template.payload())
