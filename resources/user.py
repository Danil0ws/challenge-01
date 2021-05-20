from models.user import UserModel
from flask_restful import Resource, reqparse


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

    def put(self, user_id):
        """Updates a user."""
        parser.add_argument('email',
                            type=str,
                            required=True,
                            help='This field is required!')

        parser.add_argument('name',
                            type=str,
                            required=True,
                            help='This field is required!')

        data_payload = parser.parse_args()
        user = UserModel.UpdateById(id, data_payload)
        if user:
            return {'message': 'User successfully edited'}, 201
        return {'message': 'User not edited!'}, 400

    def post(self):
        """Creates a new user."""
        parser.add_argument('email',
                            type=str,
                            required=True,
                            help='This field is required!')

        parser.add_argument('name',
                            type=str,
                            required=True,
                            help='This field is required!')

        data_payload = parser.parse_args()
        user = UserModel.InsertData(data_payload)
        if user:
            return {'message': 'User successfully created'}, 201
        return {'message': 'User not created!'}, 400
