from flask import Flask
from flask_restful import Resource, Api
from resources.user import User
from resources.product import Product
from resources.cart import Cart
from db.database import create_database

app = Flask(__name__)
api = Api(app)

api.add_resource(User, '/users')
api.add_resource(Product, '/products')
api.add_resource(Cart, '/carts')

def auth_error_handler(err):
    return {'message': 'Could not authorize user.'}, 400

if __name__ == '__main__':
    # create_database('./db/datashop.db')
    app.run(debug=True)