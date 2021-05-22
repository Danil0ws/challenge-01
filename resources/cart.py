from models.cart import CartModel
from flask_restful import Resource, reqparse, request
from flask_expects_json import expects_json

parser = reqparse.RequestParser()


class Cart(Resource):
    """Operations related to carts."""

    def get(self, user_id=None):
        """Returns details of a cart."""
        if user_id:
            CartModel.FindById(user_id)
            return {'message': 'Cart not found!'}, 404
        else:
            CartModel.FindAll()
            return {'message': 'Cart not found!'}, 404

    def delete(self, user_id, product_id=None, coupon_id=None):
        """Deletes cart."""
        if product_id:
            cartReturn = CartModel.DeleteByProductId(user_id, product_id)
            return cartReturn
        elif coupon_id:
            cartReturn = CartModel.DeleteByProductId(user_id, coupon_id)
            return cartReturn
        else:
            cartReturn = CartModel.DeleteById(user_id)
            return cartReturn

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
    def put(self, user_id, product_id, coupon_id=None):
        """Updates a cart."""
        if product_id:
            data_payload = request.get_json()
            # cart = CartModel.UpdateById(user_id, product_id, data_payload)
            return {'code': 400, 'message': 'Product not created!'}, 400
        elif coupon_id:
            data_payload = request.get_json()
            # cart = CartModel.UpdateById(user_id, coupon_id, data_payload)
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
