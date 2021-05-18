import os
import sys
sys.path.append('../')
from system.database import CreateDatabase
import unittest

class BaseIntegrationTest(unittest.TestCase):

    def setUp(self):
        if os.path.exists('./db/datacart.db'):
            os.system('rm ./db/datacart.db')
        CreateDatabase('./db/datacart.db')

    def tearDown(self):
        os.system('rm ./db/datacart.db')
        
if __name__ == '__main__':
    unittest.main()