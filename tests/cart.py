import unittest
import requests


class CartTestCase(unittest.TestCase):

    def test_add_new_cart(self):
        response = requests.post('http://127.0.0.1:5000/carts/1',
                                 json={
                                     'products': [
                                         {
                                             'id': 1,
                                             'quantity': 1
                                         }
                                     ],
                                     'coupon_code': "FIVE"
                                 })
        self.assertEqual(
            {'message': 'Cart successfully created'}, response.json())
        self.assertEqual(201, response.status_code)

    def test_get_all_carts(self):
        response = requests.get('http://127.0.0.1:5000/carts')
        getFirst = response.json()
        self.assertEqual(
            {'id': 1, 'user_id': 1, 'products': [{'id': 1, 'name': 'Remote control car', 'quantity': 1, 'price': 99.99, 'price_unit': 99.99}], 'coupon_code': 'FIVE', 'disconut': 5.0, 'subtotal': 99.99, 'total': 94.99}, getFirst[0])
        self.assertEqual(200, response.status_code)

    def test_get_cart_by_id(self):
        response = requests.get('http://127.0.0.1:5000/carts/1')
        self.assertEqual(
            {'id': 1, 'user_id': 1, 'products': [{'id': 1, 'name': 'Remote control car', 'quantity': 1, 'price': 99.99, 'price_unit': 99.99}], 'coupon_code': 'FIVE', 'disconut': 5.0, 'subtotal': 99.99, 'total': 94.99}, response.json())
        self.assertEqual(200, response.status_code)

    def test_edit_cart_add_new_product(self):
        response = requests.post('http://127.0.0.1:5000/carts/1/products',
                                 json={
                                     'products': [
                                         {
                                             'id': 2,
                                             'quantity': 1
                                         }
                                     ]
                                 })
        self.assertEqual(
            {'message': 'Product successfully added in cart'}, response.json())
        self.assertEqual(200, response.status_code)

    def test_edit_cart_add_edit_add_new_coupon(self):
        response = requests.post('http://127.0.0.1:5000/carts/1/coupons',
                                 json={
                                     'coupon_code': 'TEN10'
                                 })
        self.assertEqual(
            {'message': 'Coupon successfully edited in cart'}, response.json())
        self.assertEqual(200, response.status_code)

    def test_edit_cart_edit_quantity_in_product(self):
        response = requests.put('http://127.0.0.1:5000/carts/1/products/2',
                                json={'quantity': 2})
        self.assertEqual(
            {'message': 'Product successfully edited in cart'}, response.json())
        self.assertEqual(200, response.status_code)

    def test_edit_cart_add_edit_new_coupon(self):
        response = requests.put('http://127.0.0.1:5000/carts/1/coupons',
                                json={'coupon_code': 'TEN10'})
        self.assertEqual(
            {'message': 'Coupon successfully edited in cart'}, response.json())
        self.assertEqual(200, response.status_code)

    def test_delete_product_cart(self):
        response = requests.delete('http://127.0.0.1:5000/carts/1/products/2')
        self.assertEqual(
            {'message': 'Product successfully delete in cart'}, response.json())
        self.assertEqual(200, response.status_code)

    def test_delete_coupon_cart(self):
        response = requests.delete('http://127.0.0.1:5000/carts/1/coupons')
        self.assertEqual(
            {'message': 'Coupon successfully delete in cart'}, response.json())
        self.assertEqual(200, response.status_code)

    def test_delete_cart_by_id(self):
        response = requests.delete('http://127.0.0.1:5000/carts/1')
        self.assertEqual(
            {'message': 'Cart successfully delete'}, response.json())
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    test_order = ["test_add_new_cart",
                  "test_get_all_carts",
                  "test_get_cart_by_id",
                  "test_edit_cart_add_new_product",
                  "test_edit_cart_add_edit_add_new_coupon",
                  "test_edit_cart_edit_quantity_in_product",
                  "test_edit_cart_add_edit_new_coupon",
                  "test_delete_product_cart",
                  "test_delete_coupon_cart",
                  "test_delete_cart_by_id"
                  ]  # could be sys.argv
    loader = unittest.TestLoader()
    loader.sortTestMethodsUsing = lambda x, y: test_order.index(
        x) - test_order.index(y)
    unittest.main(testLoader=loader, verbosity=2)
