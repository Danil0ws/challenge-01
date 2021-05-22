from models.product import ProductModel
from flask_restful import Resource, reqparse, request
from flask_expects_json import expects_json

parser = reqparse.RequestParser()


class Product(Resource):
    """Operations related to products."""

    def get(self, id=None):
        """Returns details of a product."""
        if id:
            productReturn = ProductModel.FindById(id)
            return productReturn
        else:
            productsReturn = ProductModel.FindAll()
            return productsReturn

    @expects_json({
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'quantity': {'type': 'integer'},
            'price': {'type': 'number'}
        },
        'required': ['name', 'quantity', 'price']
    })
    def post(self):
        """Creates a new product."""
        data_payload = request.get_json()
        productReturn = ProductModel.InsertData(data_payload)
        return productReturn

    @expects_json({
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'quantity': {'type': 'integer'},
            'price': {'type': 'number'}
        },
        'required': ['name', 'quantity', 'price']
    })
    def put(self, id):
        """Updates a product."""
        data_payload = request.get_json()
        productReturn = ProductModel.UpdateById(id, data_payload)
        return productReturn

    def delete(self, id):
        """Deletes product."""
        productReturn = ProductModel.DeleteById(id)
        return productReturn
