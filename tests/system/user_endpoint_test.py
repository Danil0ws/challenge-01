import unittest
import requests
import json
import os
from database import CreateDatabase


class UserEndpointsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if os.path.exists('../../db/datacart.db'):
            os.system('rm ../../db/datacart.db')
        CreateDatabase('../../db/datacart.db')
        cls.uri = 'http://127.0.0.1:5000'

if __name__ == '__main__':
    unittest.main(verbosity=2)