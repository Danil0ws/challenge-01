from models.cart import CartModel
from flask_restful import Resource, reqparse, request
from flask_expects_json import expects_json

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
            # if carts:
            #     return {'carts': [cart.json() for cart in carts]}, 200
            return {'message': 'Cart not found!'}, 404

    def delete(self, user_id, product_id=None, coupon_id=None):
        """Deletes cart."""
        if product_id:
            cart = CartModel.DeleteByProductId(user_id, product_id)
            if cart:
                return {'message': 'Cart successfully delete'}, 200
            return {'message': 'Cart not found!'}, 404
        elif coupon_id:
            cart = CartModel.DeleteByProductId(user_id, coupon_id)
            if cart:
                return {'message': 'Cart successfully delete'}, 200
            return {'message': 'Cart not found!'}, 404
        else:
            carts = CartModel.DeleteById(user_id)
            if carts:
                return {'message': 'Cart successfully delete'}, 200
            return {'message': 'Cart not found'}, 404

    def put(self, user_id, product_id, coupon_id=None):
        """Updates a cart."""
        parser.add_argument('product_id',
                            type=int,
                            required=True,
                            help='This field is required!')

        parser.add_argument('quantity',
                            type=int,
                            required=True,
                            help='This field is required!')

        data_payload = parser.parse_args()
        cart = CartModel.UpdateById(user_id, product_id, data_payload)
        if cart:
            return {'code': 201, 'message': 'Product successfully created'}, 201
        return {'code': 400, 'message': 'Product not created!'}, 400

    @expects_json({
        'type': 'object',
        'properties': {
            'user_id': {'type': 'integer'},
            'products': {
                'type': 'array',
                'properties': {
                    'id': {'type': 'integer'},
                    'quantity': {'type': 'integer'}
                },
                'required': ['id', 'quantity']
            },
            'coupon_code': {
                "anyOf": [
                    {"type": "null"},
                    {"type": "string"}
                ]
            }
        },
        'required': ['user_id']
    })
    def post(self):
        """Creates a new cart."""
        data_payload = request.get_json()
        cartReturn = CartModel.InsertData(data_payload)
        return cartReturn
