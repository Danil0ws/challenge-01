from models.product import ProductModel
from flask_restful import Resource, reqparse

parser = reqparse.RequestParser()


class Product(Resource):

    def get(self, id):
        product = ProductModel.FindById(id)
        if product:
            return {'product': product.json()}, 200
        return {'message': 'Product not found!'}, 404

    def delete(self, id):
        product = ProductModel.DeleteById(id)
        if product:
            return {'message': "Product successfully delete"}, 200
        return {'message': 'Product not found!'}, 400

    def put(self, id):
        parser.add_argument('name',
                            type=str,
                            required=True,
                            help='This field is required!')

        parser.add_argument('amount',
                            type=int,
                            required=True,
                            help='This field is required!')

        parser.add_argument('price',
                            type=int,
                            required=True,
                            help='This field is required!')

        data_payload = parser.parse_args()
        product = ProductModel.UpdateById(id, data_payload)
        if product:
            return {'message': 'Product successfully edited'}, 201
        return {'message': 'Product not edited!'}, 400


class ProductList(Resource):

    def get(self):
        products = ProductModel.FindAll()
        if products:
            return {'products': [product.json() for product in products]}, 200
        return {'message': 'Product not found!'}, 404


class ProductRegister(Resource):

    def post(self):
        parser.add_argument('name',
                            type=str,
                            required=True,
                            help='This field is required!')

        parser.add_argument('amount',
                            type=int,
                            required=True,
                            help='This field is required!')

        parser.add_argument('price',
                            type=int,
                            required=True,
                            help='This field is required!')

        data_payload = parser.parse_args()
        product = ProductModel.InsertData(data_payload)
        if product:
            return {'message': 'Product successfully created'}, 201
        return {'message': 'Product not created!'}, 400
