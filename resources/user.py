from models.user import UserModel
from flask_restful import Resource, reqparse, request
from flask_expects_json import expects_json


parser = reqparse.RequestParser()


class User(Resource):
    """Operations related to Users."""

    def get(self, id=None):
        """Returns details of a user."""
        if id:
            userReturn = UserModel.FindById(id)
            return userReturn
        else:
            userReturn = UserModel.FindAll()
            return userReturn

    @expects_json({
        'type': 'object',
        'properties': {
            'email': {'type': 'string'},
            'name': {'type': 'string'}
        },
        'required': ['name', 'email']
    })
    def post(self):
        """Creates a new user."""
        data_payload = request.get_json()
        userReturn = UserModel.InsertData(data_payload)
        return userReturn

    @expects_json({
        'type': 'object',
        'properties': {
            'email': {'type': 'string'},
            'name': {'type': 'string'}
        },
        'required': ['name', 'email']
    })
    def put(self, id):
        """Updates a user."""
        data_payload = request.get_json()
        userReturn = UserModel.UpdateById(id, data_payload)
        return userReturn

    def delete(self, id):
        """Deletes user."""
        userReturn = UserModel.DeleteById(id)
        return userReturn
