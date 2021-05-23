from pyrsistent import m
from models.cart import CartModel
from flask_restful import Resource, request
from flask_expects_json import expects_json


class Cart(Resource):
    """Operations related to carts."""

    def get(self, user_id=None):
        """Returns details of a(all) cart(s)."""
        if user_id:
            cartReturn = CartModel.FindByIdComplete(user_id)
            return cartReturn
        else:
            cartsReturn = CartModel.FindAllComplete()
            return cartsReturn
        return cartReturn

    @expects_json({
        'type': 'object',
        'properties': {
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
        }
    })
    def post(self, user_id):
        """Add a new cart to the database."""
        data_payload = request.get_json()
        data_path = request.path
        if data_path.find('coupons') > 0:
            carReturn = CartModel.UpdateByCouponId(
                user_id, data_payload)
            return carReturn
        elif data_path.find('products') > 0:
            carReturn = CartModel.InsertNewByProductId(
                user_id, data_payload)
            return carReturn
        else:
            cartReturn = CartModel.InsertData(user_id, data_payload)
            return cartReturn

    @expects_json({
        'type': 'object',
        'properties': {
            'products': {
                'type': 'array',
                'properties': {
                    'quantity': {'type': 'integer'}
                },
                'required': ['id', 'quantity']
            },
            'quantity': {'type': 'integer'},
            'coupon_code': {"type": "string"}
        }
    })
    def put(self, user_id, product_id=None):
        """Update an existing cart."""
        data_payload = request.get_json()
        data_path = request.path
        if product_id is not None:
            carReturn = CartModel.UpdateByProductId(
                user_id, product_id, data_payload)
            return carReturn
        else:
            for key in data_payload.keys():
                if str(key) == 'coupon_code':
                    carReturn = CartModel.UpdateByCouponId(
                        user_id, data_payload)
                    return carReturn
                else:
                    if str(key) == "products":
                        carReturn = CartModel.InsertNewByProductId(
                            user_id, data_payload)
                        return carReturn

    def delete(self, user_id, product_id=None, coupon_code=None):
        """Deletes a cart."""
        data_path = request.path
        if product_id:
            cartReturn = CartModel.DeleteByProductId(user_id, product_id)
            return cartReturn
        elif data_path.find('coupons') == 9:
            cartReturn = CartModel.DeleteByCouponId(user_id, coupon_code)
            return cartReturn
        else:
            CartModel.DeleteByProductId(user_id)
            CartModel.DeleteByCouponId(user_id)
            cartReturn = CartModel.DeleteByCartId(user_id)
            return cartReturn
