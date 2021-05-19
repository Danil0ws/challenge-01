from flask import Flask
from flask_restful import Resource, Api
from resources.user import User, UserList, UserRegister
from resources.product import Product, ProductList, ProductRegister
from resources.coupon import Coupon, CouponList, CouponRegister
from resources.cart import Cart, CartList, CartRegister

app = Flask(__name__)
api = Api(app)

api.add_resource(User, '/users/<int:id>')
api.add_resource(UserList, '/users')
api.add_resource(UserRegister, '/user')

api.add_resource(Product, '/products/<int:id>')
api.add_resource(ProductList, '/products')
api.add_resource(ProductRegister, '/product')

api.add_resource(Coupon, '/coupons/<int:id>')
api.add_resource(CouponList, '/coupons')
api.add_resource(CouponRegister, '/coupon')

api.add_resource(Cart, '/carts/<int:id>')
api.add_resource(CartList, '/carts')
api.add_resource(CartRegister, '/cart')


def page_not_found(err):
    return {'message': 'Page not found.'}, 404


if __name__ == '__main__':
    app.run(debug=True)
