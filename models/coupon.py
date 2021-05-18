import sqlite3


class CouponModel:

    def __init__(self, id, active, type, value):
        self.id = id
        self.active = active
        self.type = type
        self.value = value

    @classmethod
    def FindById(cls, id):
        ConnectionSqlite = sqlite3.connect('./db/datacart.db')
        cursorSqlite = ConnectionSqlite.cursor()
        ResultCouponById = cursorSqlite.execute(
            'SELECT * FROM coupons WHERE id=?', (id,))
        RowsCouponByIdAll = ResultCouponById.fetchall()
        for Row in RowsCouponByIdAll:
            CouponByIdAll = CouponModel(Row[0], Row[1], Row[2], Row[3])
            ConnectionSqlite.close()
            return CouponByIdAll

    @classmethod
    def FindAll(cls):
        CouponList = list()
        ConnectionSqlite = sqlite3.connect('./db/datacart.db')
        cursorSqlite = ConnectionSqlite.cursor()
        ResultCouponAll = cursorSqlite.execute('SELECT * FROM coupons')
        RowsCouponAll = ResultCouponAll.fetchall()
        for Row in RowsCouponAll:
            CouponList.append(CouponModel(Row[0], Row[1], Row[2], Row[3]))
        return CouponList
        ConnectionSqlite.close()

    def json(self):
        return {'id': self.id,
                'active': self.active,
                'type': self.type,
                'value': self.value}

    def AddSaveDb(self): 
        self.ConnectionSqlite.commit()
        self.ConnectionSqlite.close()
    
    def DeleteSaveDb(self): 
        self.ConnectionSqlite.commit()
        self.ConnectionSqlite.close()
