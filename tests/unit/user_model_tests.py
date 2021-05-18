import sys
sys.path.append('../..')
from models import user
import unittest

class UserModelTests(unittest.TestCase):

    def setUp(self):
        self.user_model = user.UserModel(1, 'test@test.com', 'Test')

if __name__ == '__main__':
    unittest.main(verbosity=2)