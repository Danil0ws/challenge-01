from models.user import UserModel
from flask_restful import Resource, reqparse


class User(Resource):
    def get(self, id):
        user = UserModel.FindById(id)
        if user:
            return {'user': user.json()}, 200
        return {'message': 'User not found!'}, 404


class UserList(Resource):
    def get(self):
        users = UserModel.FindAll()
        if users:
            return {'users': [user.json() for user in users]}, 200
        return {'message': 'User not found!'}, 404
