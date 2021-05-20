from models.product import ProductModel
from flask_restful import Resource, reqparse

parser = reqparse.RequestParser()


class Product(Resource):
    """Operations related to products."""

    def get(self, id=None):
        """Returns details of a product."""
        if id:
            product = ProductModel.FindById(id)
            if product:
                return {'product': product.json()}, 200
            return {'message': 'Product not found!'}, 404
        else:
            products = ProductModel.FindAll()
            if products:
                return {'products': [product.json() for product in products]}, 200
            return {'message': 'Product not found!'}, 404

    def delete(self, id):
        """Deletes product."""
        product = ProductModel.DeleteById(id)
        if product:
            return {'message': 'Product successfully delete'}, 200
        return {'message': 'Product not found!'}, 400

    def put(self, id):
        """Updates a product."""
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

    def post(self):
        """Creates a new product."""
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
