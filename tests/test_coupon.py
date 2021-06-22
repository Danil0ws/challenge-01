import unittest
import requests


class CouponTestCase(unittest.TestCase):

    def test_get_all_coupons(self):
        response = requests.get('http://127.0.0.1:5000/coupons')
        getFirst = response.json()
        self.assertEqual(
            {'id': 1, 'active': 1, 'type': 'percentage', 'code': 'TEN10', 'quantity': 10, 'value': 10.0}, getFirst[0])
        self.assertEqual(200, response.status_code)

    def test_get_coupon_by_id(self):
        response = requests.get('http://127.0.0.1:5000/coupons/1')
        self.assertEqual(
            {'id': 1, 'active': 1, 'type': 'percentage', 'code': 'TEN10', 'quantity': 10, 'value': 10.0}, response.json())
        self.assertEqual(200, response.status_code)

    def test_edit_coupon_by_id(self):
        response = requests.put('http://127.0.0.1:5000/coupons/1',
                                json={'id': 1, 'active': 1, 'type': 'percentage', 'code': 'TEN10', 'quantity': 10, 'value': 10.0})
        self.assertEqual(
            {'message': 'Coupon successfully edited'}, response.json())
        self.assertEqual(200, response.status_code)

    def test_add_new_coupon(self):
        response = requests.post('http://127.0.0.1:5000/coupons',
                                 json={'active': 1, 'type': 'percentage', 'code': 'TEN10', 'quantity': 10, 'value': 10.0})
        self.assertEqual(
            {'message': 'Coupon successfully created'}, response.json())
        self.assertEqual(201, response.status_code)

    def test_delete_coupon_by_id(self):
        response = requests.delete('http://127.0.0.1:5000/coupons/3')
        self.assertEqual(
            {'message': 'Coupon successfully delete'}, response.json())
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
