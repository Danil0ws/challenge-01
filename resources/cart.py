from models.cart import CartModel
from flask_restful import Resource


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
        # cart = CartModel.FindById(id)
        # if cart:
        #     return {'cart': cart.json()}, 200
        return {'message': 'Cart not found!'}, 404

    def put(self, user_id):
        # cart = CartModel.FindById(id)
        # if cart:
        #     return {'cart': cart.json()}, 200
        return {'message': 'Cart not found!'}, 404
