import sqlite3


class UserModel:

    db_path = './db/datacart.db'

    def __init__(self, id, email, name):
        self.id = id
        self.email = email
        self.name = name

    def __repr__(self):
        return str(self.id) + ", " + self.email + ", " + self.name

    @classmethod
    def FindById(cls, id):
        try:
            ConnectionSqlite = sqlite3.connect(cls.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultUsersById = CursorSqlite.execute(
                'SELECT * FROM users WHERE id=?', (id,))
            RowsUsersByIdAll = ResultUsersById.fetchall()
            for Row in RowsUsersByIdAll:
                UsersByIdAll = UserModel(Row[0], Row[1], Row[2])
                ConnectionSqlite.close()
                return UsersByIdAll
        except sqlite3.Error as er:
            return False

    @classmethod
    def DeleteById(cls, id):
        try:
            ConnectionSqlite = sqlite3.connect(cls.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultDeleteUser = CursorSqlite.execute(
                'DELETE FROM users WHERE id=?;', (id,))
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if ResultDeleteUser.rowcount:
                return ResultDeleteUser.rowcount
        except sqlite3.Error as er:
            return False

    @classmethod
    def UpdateById(cls, id, body):
        try:
            ConnectionSqlite = sqlite3.connect(cls.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultUpdateUser = CursorSqlite.execute(
                'UPDATE users SET email = ?, name = ? WHERE id=?;', (body.email, body.name, id))
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if ResultUpdateUser.rowcount:
                return {'code': 201, 'message': 'User successfully edited'}, 201
            return {'code': 400, 'message': 'User not edited'}, 400
        except sqlite3.Error as er:
            return {'code': 400, 'message': 'Product not edited'}, 400

    @classmethod
    def InsertData(cls, body):
        try:
            ConnectionSqlite = sqlite3.connect(cls.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultInsertUser = CursorSqlite.execute(
                'INSERT INTO users VALUES(NULL, ?, ?)', (body.email, body.name))
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if ResultInsertUser.rowcount:
                return {'code': 201, 'message': 'User successfully created'}, 201
            return {'code': 400, 'message': 'User not created'}, 400
        except sqlite3.Error as er:
            return {'code': 400, 'message': 'User not created'}, 400

    @classmethod
    def FindAll(cls):
        try:
            UsersList = list()
            ConnectionSqlite = sqlite3.connect(cls.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultUsersAll = CursorSqlite.execute('SELECT * FROM users')
            RowsUsersAll = ResultUsersAll.fetchall()
            for Row in RowsUsersAll:
                UsersList.append(UserModel(Row[0], Row[1], Row[2]))
            ConnectionSqlite.close()
            if UsersList.count()>=0:
                return UsersList                
            return {'code': 400, 'message': 'User not found'}, 400
        except sqlite3.Error as er:
            return {'code': 400, 'message': 'User not found'}, 400

    def json(self):
        return {'id': self.id,
                'email': self.email,
                'name': self.name}
