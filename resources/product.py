from models.product import ProductModel
from flask_restful import Resource

class Product(Resource):
    def get(self, id):
        return {'message': 'Product not found!'}, 404