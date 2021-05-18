from models.cart import CartModel
from flask_restful import Resource
from flask import jsonify, request


class Cart(Resource):
    def get(self, user_id):
        # cart = CartModel.FindById(id)
        # if cart:
        #     return {'cart': cart.json()}, 200
        return {'message': 'Cart not found!'}, 404

    def delete(self, user_id):
        # cart = CartModel.FindById(id)
        # if cart:
        #     return {'cart': cart.json()}, 200
        return {'message': 'Cart not found!'}, 404

    def post(self, user_id):
        req = request.get_json()
        # cart = CartModel.FindById(id)
        # if cart:
        #     return {'cart': cart.json()}, 200
        return {'message': 'Cart not found!'}, 404

    def put(self, user_id):
        # cart = CartModel.FindById(id)
        # if cart:
        #     return {'cart': cart.json()}, 200
        return {'message': 'Cart not found!'}, 404

class CartComplete(Resource):
    def get(self, user_id):

        return {'message': 'Cart not found!'}, 404