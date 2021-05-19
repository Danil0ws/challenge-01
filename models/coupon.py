import sqlite3


class CouponModel:

    db_path = './db/datacart.db'

    def __init__(self, id, active, type, code, value):
        self.id = id
        self.active = active
        self.type = type
        self.code = code
        self.value = value

    @classmethod
    def FindById(cls, id):
        try:
            ConnectionSqlite = sqlite3.connect(cls.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultCouponById = CursorSqlite.execute(
                'SELECT * FROM coupons WHERE id=?', (id,))
            RowsCouponByIdAll = ResultCouponById.fetchall()
            for Row in RowsCouponByIdAll:
                CouponByIdAll = CouponModel(
                    Row[0], Row[1], Row[2], Row[3], Row[4])
                ConnectionSqlite.close()
                return CouponByIdAll
        except sqlite3.Error as er:
            return False

    @classmethod
    def DeleteById(cls, id):
        try:
            ConnectionSqlite = sqlite3.connect(cls.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultDeleteCoupon = CursorSqlite.execute(
                'DELETE FROM coupons WHERE id=?;', (id,))
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if ResultDeleteCoupon.rowcount:
                return ResultDeleteCoupon.rowcount
        except sqlite3.Error as er:
            return False

    @classmethod
    def UpdateById(cls, id, body):
        try:
            ConnectionSqlite = sqlite3.connect(cls.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultUpdateCoupon = CursorSqlite.execute(
                'UPDATE coupons SET active = ?, type = ?, code = ?, value = ? WHERE id=?;', (body.active, body.type, body.code, body.value, id))
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if ResultUpdateCoupon.rowcount:
                return ResultUpdateCoupon.rowcount
        except sqlite3.Error as er:
            return False

    @classmethod
    def InsertData(cls, body):
        try:
            ConnectionSqlite = sqlite3.connect(cls.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultInsertCoupon = CursorSqlite.execute(
                'INSERT INTO coupons VALUES(NULL, ?, ?, ?, ?)', (body.active, body.type, body.code, body.value))
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if ResultInsertCoupon.rowcount:
                return ResultInsertCoupon.rowcount
        except sqlite3.Error as er:
            return False

    @classmethod
    def FindAll(cls):
        try:
            CouponList = list()
            ConnectionSqlite = sqlite3.connect(cls.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultCouponAll = CursorSqlite.execute('SELECT * FROM coupons')
            RowsCouponAll = ResultCouponAll.fetchall()
            for Row in RowsCouponAll:
                CouponList.append(CouponModel(
                    Row[0], Row[1], Row[2], Row[3], Row[4]))
            ConnectionSqlite.close()
            return CouponList
        except sqlite3.Error as er:
            return False

    def json(self):
        return {'id': self.id,
                'active': self.active,
                'type': self.type,
                'code': self.code,
                'value': self.value}
