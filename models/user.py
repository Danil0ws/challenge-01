import sqlite3


class UserModel:

    def __init__(self, id, email, name):
        self.id = id
        self.email = email
        self.name = name

    @classmethod
    def FindById(cls, id):
        ConnectionSqlite = sqlite3.connect('./db/datacart.db')
        cursorSqlite = ConnectionSqlite.cursor()
        ResultUsersById = cursorSqlite.execute(
            'SELECT * FROM users WHERE id=?', (id,))
        RowsUsersByIdAll = ResultUsersById.fetchall()
        for Row in RowsUsersByIdAll:
            UsersByIdAll = UserModel(Row[0], Row[1], Row[2])
            ConnectionSqlite.close()
            return UsersByIdAll

    @classmethod
    def FindAll(cls):
        UsersList = list()
        ConnectionSqlite = sqlite3.connect('./db/datacart.db')
        cursorSqlite = ConnectionSqlite.cursor()
        ResultUsersAll = cursorSqlite.execute('SELECT * FROM users')
        RowsUsersAll = ResultUsersAll.fetchall()
        for Row in RowsUsersAll:
            UsersList.append(UserModel(Row[0], Row[1], Row[2]))
        return UsersList
        ConnectionSqlite.close()

    def json(self):
        return {'id': self.id,
                'email': self.email,
                'name': self.name}

    def AddSaveDb(self): 
        self.ConnectionSqlite.commit()
        self.ConnectionSqlite.close()
    
    def DeleteSaveDb(self): 
        self.ConnectionSqlite.commit()
        self.ConnectionSqlite.close()