from models.user import UserModel
from flask_restful import Resource, reqparse, request
from flask_expects_json import expects_json


parser = reqparse.RequestParser()


class User(Resource):
    """Operations related to Users."""

    def get(self, id=None):
        """Returns details of a user."""
        if id:
            user = UserModel.FindById(id)
            if user:
                return {'user': user.json()}, 200
            return {'message': 'User not found!'}, 404
        else:
            users = UserModel.FindAll()
            if users:
                return {'users': [user.json() for user in users]}, 200
            return {'message': 'User not found!'}, 404

    def delete(self, id):
        """Deletes user."""
        user = UserModel.DeleteById(id)
        if user:
            return {'message': 'User successfully delete'}, 200
        return {'message': 'User not found!'}, 400

    @expects_json({
        'type': 'object',
        'properties': {
            'email': {'type': 'string'},
            'name': {'type': 'string'}
        }
    })
    def put(self, user_id):
        """Updates a user."""
        data_payload = request.get_json()
        return userReturn


    @expects_json({
        'type': 'object',
        'properties': {
            'email': {'type': 'string'},
            'name': {'type': 'string'}
        },
        'required': ['name', 'name']
    })
    def post(self):
        """Creates a new user."""
        data_payload = request.get_json()
        userReturn = UserModel.InsertData(data_payload)
        return userReturn
