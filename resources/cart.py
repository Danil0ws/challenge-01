from models.cart import CartModel
from flask_restful import Resource

class Cart(Resource):
    def get(self, id):
        return {'message': 'Cart not found!'}, 404