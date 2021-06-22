import unittest
import requests


class UserTestCase(unittest.TestCase):

    def test_get_all_users(self):
        response = requests.get('http://127.0.0.1:5000/users')
        getFirst = response.json()
        self.assertEqual(
            {'id': 1, 'email': 'admin@exemple.com', 'name': 'admin'}, getFirst[0])
        self.assertEqual(200, response.status_code)

    def test_get_user_by_id(self):
        response = requests.get('http://127.0.0.1:5000/users/1')
        self.assertEqual(
            {'id': 1, 'email': 'admin@exemple.com', 'name': 'admin'}, response.json())
        self.assertEqual(200, response.status_code)

    def test_edit_user_by_id(self):
        response = requests.put('http://127.0.0.1:5000/users/2',
                                json={
                                    'email': 'admin2@exemple.com',
                                    'name': 'admin 2'
                                })
        self.assertEqual(
            {'message': 'User successfully edited'}, response.json())
        self.assertEqual(200, response.status_code)

    def test_add_new_user(self):
        response = requests.post('http://127.0.0.1:5000/users',
                                 json={
                                     'email': 'admin2@exemple.com',
                                     'name': 'admin 2'
                                 })
        self.assertEqual(
            {'message': 'User successfully created'}, response.json())
        self.assertEqual(201, response.status_code)

    def test_delete_user_by_id(self):
        response = requests.delete('http://127.0.0.1:5000/users/2')
        self.assertEqual(
            {'message': 'User successfully delete'}, response.json())
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
