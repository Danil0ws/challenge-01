from flask import Flask
from flask_restful import Resource, Api
from resources.user import User
from resources.product import Product
from resources.coupon import Coupon
from resources.cart import Cart

app = Flask(__name__)
api = Api(app)

api.add_resource(User, '/users', '/users/<int:id>')
api.add_resource(Product, '/products', '/products/<int:id>')
api.add_resource(Coupon, '/coupons', '/coupons/<int:id>')
api.add_resource(Cart, '/carts', '/carts/<int:user_id>',
                 '/carts/<int:user_id>/products/<int:product_id>',
                 '/carts/<int:user_id>/coupons/<int:coupon_id>')


@app.errorhandler(404)
def not_found(e):
    return {'message': 'Page not found.'}, 404


if __name__ == '__main__':
    app.run(debug=True)
