"""Create a namespaced abandoned-cart email template."""

from lifecycle_templates import Infrai, create_abandoned_cart_template


if __name__ == "__main__":
    infrai = Infrai.from_environment()
    created = create_abandoned_cart_template(infrai, "mystore")
    print(f"Created lifecycle template: {created}")
