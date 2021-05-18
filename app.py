from flask import Flask
from flask_restful import Resource, Api
from resources.user import User, UserList
from resources.product import Product, ProductList
from resources.cart import Cart

app = Flask(__name__)
api = Api(app)

api.add_resource(User, '/users/<string:id>')
api.add_resource(UserList, '/users')
api.add_resource(Product, '/products/<string:id>')
api.add_resource(ProductList, '/products')
api.add_resource(Cart, '/carts')


def page_not_found(err):
    return {'message': 'Page not found.'}, 404


if __name__ == '__main__':
    app.run(debug=True)
