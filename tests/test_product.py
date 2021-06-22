import unittest
import requests


class ProductTestCase(unittest.TestCase):

    def test_get_all_products(self):
        response = requests.get('http://127.0.0.1:5000/products')
        getFirst = response.json()
        self.assertEqual(
            {'id': 1, 'name': 'Remote control car', 'quantity': 2, 'price': 99.99}, getFirst[0])
        self.assertEqual(200, response.status_code)

    def test_get_product_by_id(self):
        response = requests.get('http://127.0.0.1:5000/products/1')
        self.assertEqual(
            {'id': 1, 'name': 'Remote control car', 'quantity': 2, 'price': 99.99}, response.json())
        self.assertEqual(200, response.status_code)

    def test_edit_product_by_id(self):
        response = requests.put('http://127.0.0.1:5000/products/1',
                                json={
                                    'name': 'Remote control car',
                                    'quantity': 2,
                                    'price': 99.99
                                })
        self.assertEqual(
            {'message': 'Product successfully edited'}, response.json())
        self.assertEqual(200, response.status_code)

    def test_add_new_product(self):
        response = requests.post('http://127.0.0.1:5000/products',
                                 json={
                                     'name': 'Headset',
                                     'quantity': 10,
                                     'price': 199.99
                                 })
        self.assertEqual(
            {'message': 'Product successfully created'}, response.json())
        self.assertEqual(201, response.status_code)

    def test_delete_product_by_id(self):
        response = requests.delete('http://127.0.0.1:5000/products/5')
        self.assertEqual(
            {'message': 'Product successfully delete'}, response.json())
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
