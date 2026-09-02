import unittest

from lifecycle_templates import abandoned_cart_template


class AbandonedCartTemplateTest(unittest.TestCase):
    def test_template_keeps_the_checkout_context(self) -> None:
        template = abandoned_cart_template("mystore")
        payload = template.payload()

        self.assertTrue(payload["name"].startswith("mystore-abandoned-cart-"))
        self.assertIn("{{checkout_url}}", payload["html"])
        self.assertEqual(payload["default_vars"]["product_name"], "Canvas tote")


if __name__ == "__main__":
    unittest.main()
