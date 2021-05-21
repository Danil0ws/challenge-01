from models.product import ProductModel
from flask_restful import Resource, reqparse, request
from flask_expects_json import expects_json

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
        return {'message': 'Product not found'}, 400

    @expects_json({
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'quantity': {'type': 'integer'},
            'price': {'type': 'integer'}
        },
        'required': ['name', 'quantity', 'price']
    })
    def put(self, id):
        """Updates a product."""
        data_payload = request.get_json()
        productReturn = ProductModel.UpdateById(id, data_payload)
        return productReturn

    @expects_json({
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'quantity': {'type': 'integer'},
            'price': {'type': 'integer'}
        },
        'required': ['name', 'quantity', 'price']
    })
    def post(self):
        """Creates a new product."""
        data_payload = request.get_json()
        productReturn = ProductModel.InsertData(data_payload)
        return productReturn
