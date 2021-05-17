from models.user import UserModel
from flask_restful import Resource

class User(Resource):
    def get(self, id):
        return {'message': 'User not found!'}, 404
