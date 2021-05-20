from models.cart import CartModel
from flask_restful import Resource, reqparse

parser = reqparse.RequestParser()


class Cart(Resource):
    """Operations related to carts."""

    def get(self, user_id=None):
        """Returns details of a cart."""
        if user_id:
            carts = CartModel.FindById(user_id)
            if carts:
                return {'cart': [cart.json() for cart in carts]}, 200
            return {'message': 'Cart not found!'}, 404
        else:
            carts = CartModel.FindAll()
            if carts:
                return {'carts': [cart.json() for cart in carts]}, 200
            return {'message': 'Cart not found!'}, 404

    def delete(self, user_id, product_id=None):
        """Deletes cart."""
        if product_id:
            cart = CartModel.DeleteByProductId(user_id, product_id)
            if cart:
                return {'message': 'Cart successfully delete'}, 200
            return {'message': 'Cart not found!'}, 404
        else:
            carts = CartModel.DeleteById(user_id)
            if carts:
                return {'message': 'Cart successfully delete'}, 200
            return {'message': 'Cart not found!'}, 404

    def put(self, user_id, product_id):
        """Updates a cart."""
        parser.add_argument('quantity',
                            type=int,
                            required=True,
                            help='This field is required!')

        data_payload = parser.parse_args()
        cart = CartModel.UpdateById(user_id, product_id, data_payload)
        if cart:
            return {'message': 'Product successfully created'}, 201
        return {'message': 'Product not created!'}, 400

    def post(self, user_id):
        """Creates a new cart."""
        parser.add_argument('quantity',
                            type=int,
                            required=True,
                            help='This field is required!')

        parser.add_argument('product_id',
                            type=int,
                            required=True,
                            help='This field is required!')

        parser.add_argument('coupon_id',
                            type=int,
                            required=False,
                            help='This field is required!')

        data_payload = parser.parse_args()
        cart = CartModel.InsertData(user_id, data_payload)
        if cart:
            return {'message': 'Product successfully created'}, 201
        return {'message': 'Product not created!'}, 400
