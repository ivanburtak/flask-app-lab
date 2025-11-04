import unittest
from app import app  # Переконайтеся, що імпортували ваш Flask-додаток


class ProductsTestCase(unittest.TestCase):

    def setUp(self):
        """Налаштування клієнта тестування перед кожним тестом."""
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_products_list_page(self):
        """Тест маршруту /products/."""
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Product List", response.data)
        self.assertIn(b"Laptop", response.data)
        self.assertIn(b"Smartphone", response.data)
        self.assertIn(b"Headphones", response.data)


    def test_product_detail_valid_id(self):
        """Тест маршруту /products/<id>, який існує."""
        response = self.client.get("/products/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop", response.data)
        self.assertIn(b"High-performance laptop", response.data)
        self.assertIn(b"$1200", response.data)
        self.assertIn(b"Return to product list", response.data)

    def test_product_detail_invalid_id(self):
        """Тест маршруту /products/<id>, який не існує."""
        response = self.client.get("/products/999")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()