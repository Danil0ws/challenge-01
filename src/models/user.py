import sqlite3
from typing import List, Set, Dict, Tuple, Optional, AnyStr


class UserModel:

    db_path = './src/db/datacart.db'

    def __init__(self, id, email, name):
        self.id = id
        self.email = email
        self.name = name

    def __repr__(self):
        return str(self.id) + ", " + self.email + ", " + self.name

    def json(self):
        return {'id': self.id,
                'email': self.email,
                'name': self.name}

    @classmethod
    def FindById(cls, id):
        try:
            ConnectionSqlite = sqlite3.connect(UserModel.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultUsersById = CursorSqlite.execute(
                'SELECT * FROM users WHERE id=?', (id,))
            RowsUsersByIdAll = ResultUsersById.fetchall()
            if RowsUsersByIdAll is None:
                return {'message': "User id not found"}
            for Row in RowsUsersByIdAll:
                UsersByIdAll = UserModel(Row[0], Row[1], Row[2])
                ConnectionSqlite.close()
                return UsersByIdAll.json(), 200
            return {'message': 'User Invalid ID supplied'}, 400
        except sqlite3.Error as er:
            return {'message': 'User not edited'}, 404

    @classmethod
    def DeleteById(cls, id):
        try:
            ConnectionSqlite = sqlite3.connect(UserModel.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultDeleteUser = CursorSqlite.execute(
                'DELETE FROM users WHERE id=?;', (id,))
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if ResultDeleteUser.rowcount:
                return {'message': 'User successfully delete'}, 200
            return {'message': 'User Invalid ID supplied'}, 400
        except sqlite3.Error as er:
            return {'message': 'User not delete'}, 404

    @classmethod
    def UpdateById(cls, id, body):
        try:
            ConnectionSqlite = sqlite3.connect(UserModel.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultUpdateUser = CursorSqlite.execute(
                'UPDATE users SET email = ?, name = ? WHERE id=?;', (str(body['email']), str(body['name']), id))
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if ResultUpdateUser.rowcount:
                return {'message': 'User successfully edited'}, 200
            return {'message': 'User Invalid ID supplied'}, 400
        except sqlite3.Error as er:
            return {'message': 'User not edited'}, 404

    @classmethod
    def InsertData(cls, body):
        try:
            ConnectionSqlite = sqlite3.connect(UserModel.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultInsertUser = CursorSqlite.execute(
                'INSERT INTO users VALUES(NULL, ?, ?)', (str(body['email']), str(body['name'])))
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if ResultInsertUser.rowcount:
                return {'message': 'User successfully created'}, 201
            return {'message': 'User not created'}, 400
        except sqlite3.Error as er:
            return {'message': 'User not created'}, 404

    @classmethod
    def FindAll(cls):
        try:
            UsersList = list()
            ConnectionSqlite = sqlite3.connect(UserModel.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultUsersAll = CursorSqlite.execute('SELECT * FROM users')
            RowsUsersAll = ResultUsersAll.fetchall()
            for Row in RowsUsersAll:
                UsersList.append(UserModel(Row[0], Row[1], Row[2]))
            ConnectionSqlite.close()
            if len(UsersList) >= 0:
                return [user.json() for user in UsersList], 200
            return {'message': 'User not found'}, 400
        except sqlite3.Error as er:
            return {'message': 'User not found'}, 404
