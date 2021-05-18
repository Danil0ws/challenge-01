from models.product import ProductModel
from flask_restful import Resource, reqparse


class Product(Resource):
    def get(self, id):
        product = ProductModel.FindById(id)
        if product:
            return {'product': product.json()}, 200
        return {'message': 'Product not found!'}, 404


class ProductList(Resource):
    def get(self):
        products = ProductModel.FindAll()
        if products:
            return {'products': [product.json() for product in products]}, 200
        return {'message': 'Product not found!'}, 404
