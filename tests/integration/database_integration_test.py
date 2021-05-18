  
import sys
sys.path.append('../..')
from base_test import BaseTest
from models.user import UserModel
from models.product import ProductModel
from models.cart import CartModel
from models.cupon import CuponModel
import os
os.chdir('../..')
import unittest


class DataBaseIntegrationTests(BaseTest):

    def test_user_model_crud(self):
        self.user_model = UserModel()

    def test_product_model_crud(self):
        self.user_model = ProductModel()
    
    def test_cupon_model_crud(self):
        self.user_model = CuponModel()

    def test_cart_model_crud(self):
        self.user_model = CartModel()

if __name__ == '__main__':
    unittest.main()