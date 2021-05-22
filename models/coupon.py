import sqlite3


class CouponModel:

    db_path = './db/datacart.db'

    def __init__(self, id, active, type, code, quantity, value):
        self.id = id
        self.active = active
        self.type = type
        self.code = code
        self.quantity = quantity
        self.value = value

    def __repr__(self):
        return str(self.id) + ", " + str(self.active) + ", " + self.type + ", " + self.code + ", " + str(self.quantity) + ", " + str(self.value)

    @classmethod
    def FindById(cls, id):
        try:
            ConnectionSqlite = sqlite3.connect(cls.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultCouponsById = CursorSqlite.execute(
                'SELECT * FROM coupons WHERE id=?', (id,))
            RowsCouponsByIdAll = ResultCouponsById.fetchall()
            if RowsCouponsByIdAll is None:
                return {'code': 400, 'message': "Coupon id not found"}
            for Row in RowsCouponsByIdAll:
                CouponsByIdAll = CouponModel(
                    Row[0], Row[1], Row[2], Row[3], Row[4], Row[5])
                ConnectionSqlite.close()
                return {'code': 200, 'coupon': CouponsByIdAll.json()}, 200
            return {'code': 400, 'message': 'Coupon not edited'}, 400
        except sqlite3.Error as er:
            return {'code': 400, 'message': 'Coupon not edited'}, 400

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
                return {'code': 200, 'message': 'Coupon successfully delete'}, 200
            return {'code': 400, 'message': 'Coupon not delete'}, 400
        except sqlite3.Error as er:
            return {'code': 400, 'message': 'Coupon not delete'}, 400

    @classmethod
    def UpdateById(cls, id, body):
        try:
            ConnectionSqlite = sqlite3.connect(cls.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultUpdateCoupon = CursorSqlite.execute(
                'UPDATE coupons SET active = ?, type = ?, code = ?, quantity = ?, value = ? WHERE id=?;', (int(body['active']), str(body['type']), str(body['code']), int(body['quantity']), int(body['value']), id))
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if ResultUpdateCoupon.rowcount:
                return {'code': 201, 'message': 'Coupon successfully edited'}, 200
            return {'code': 400, 'message': 'Coupon not edited'}, 400
        except sqlite3.Error as er:
            return {'code': 400, 'message': 'Coupon not edited'}, 400

    @classmethod
    def InsertData(cls, body):
        try:
            ConnectionSqlite = sqlite3.connect(cls.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultInsertCoupon = CursorSqlite.execute(
                'INSERT INTO coupons VALUES(NULL, ?, ?, ?, ?, ?)', (int(body['active']), str(body['type']), str(body['code']), int(body['quantity']), int(body['value'])))
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if ResultInsertCoupon.rowcount:
                return {'code': 201, 'message': 'Coupon successfully created'}, 201
            return {'code': 400, 'message': 'Coupon not created'}, 400
        except sqlite3.Error as er:
            return {'code': 400, 'message': 'Coupon not created'}, 400

    @classmethod
    def FindAll(cls):
        try:
            CouponsList = list()
            ConnectionSqlite = sqlite3.connect(cls.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultCouponsAll = CursorSqlite.execute('SELECT * FROM coupons')
            RowsCouponsAll = ResultCouponsAll.fetchall()
            for Row in RowsCouponsAll:
                CouponsList.append(CouponModel(
                    Row[0], Row[1], Row[2], Row[3], Row[4], Row[5]))
            ConnectionSqlite.close()
            if len(CouponsList) >= 0:
                return {'code': 200, 'coupons': [coupon.json() for coupon in CouponsList]}, 200
            return {'code': 400, 'message': 'Coupon not found'}, 400
        except sqlite3.Error as er:
            return {'code': 400, 'message': 'Coupon not found'}, 400

    def json(self):
        return {'id': self.id,
                'active': self.active,
                'type': self.type,
                'code': self.code,
                'quantity': self.quantity,
                'value': self.value}
