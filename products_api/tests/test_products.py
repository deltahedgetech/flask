import unittest
import requests


class ProductsTest(unittest.TestCase):

    def setUp(self):
        self.url = 'http://localhost:5000/'
        self.hdr = {'User-Agent': 'Mozilla/5.0'}

    def test_server_connection(self):
        response = requests.get(self.url, headers=self.hdr, timeout=5)
        self.assertEqual(response.status_code, 200)

    # Requires database
    def test_get_product_by_id(self):
        self.url += 'get_product_by_id/6067181'
        response = requests.get(self.url, headers=self.hdr, timeout=5)
        self.assertEqual(response.status_code, 200)

    # Requires database
    def test_get_product_by_id_not_exists(self):
        self.url += 'get_product_by_id/99999999'
        response = requests.get(self.url, headers=self.hdr, timeout=5)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result['message'], 'No matching records')

    # Requires database
    def test_get_product_by_id_content(self):
        self.url += 'get_product_by_id/6067181'
        response = requests.get(self.url, headers=self.hdr, timeout=5)
        result = response.json()
        self.assertEqual(result['0']['brand'], 'externum')

    # Requires database
    def test_get_cheapest_products(self):
        self.url += 'get_cheapest_products/5'
        response = requests.get(self.url, headers=self.hdr, timeout=5)
        self.assertEqual(response.status_code, 200)

    # Requires database
    def test_get_cheapest_products_content(self):
        self.url += 'get_cheapest_products/5'
        response = requests.get(self.url, headers=self.hdr, timeout=5)
        result = response.json()
        self.assertEqual(len(result), 5)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
