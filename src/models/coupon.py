import sqlite3


class CouponModel:

    db_path = './src/db/datacart.db'

    def __init__(self, id, active, type, code, quantity, value):
        self.id = id
        self.active = active
        self.type = type
        self.code = code
        self.quantity = quantity
        self.value = value

    def __repr__(self):
        return str(self.id) + ", " + str(self.active) + ", " + self.type + ", " + self.code + ", " + str(self.quantity) + ", " + str(self.value)

    def json(self):
        return {'id': self.id,
                'active': self.active,
                'type': self.type,
                'code': self.code,
                'quantity': self.quantity,
                'value': self.value}

    @classmethod
    def FindById(cls, id):
        try:
            ConnectionSqlite = sqlite3.connect(CouponModel.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultCouponsById = CursorSqlite.execute(
                'SELECT * FROM coupons WHERE id=?', (id,))
            RowsCouponsByIdAll = ResultCouponsById.fetchall()
            if RowsCouponsByIdAll is None:
                return {'message': "Coupon id not found"}
            for Row in RowsCouponsByIdAll:
                CouponsByIdAll = CouponModel(
                    Row[0], Row[1], Row[2], Row[3], Row[4], Row[5])
                ConnectionSqlite.close()
                return CouponsByIdAll.json(), 200
            return {'message': 'Coupon Invalid ID supplied'}, 400
        except sqlite3.Error as er:
            return {'message': 'Coupon not found'}, 404

    @classmethod
    def FindByCode(cls, code):
        try:
            ConnectionSqlite = sqlite3.connect(CouponModel.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultCouponsById = CursorSqlite.execute(
                'SELECT * FROM coupons WHERE code=?', (code,))
            RowsCouponsByIdAll = ResultCouponsById.fetchall()
            if RowsCouponsByIdAll is None:
                return {'message': "Coupon Invalid Code supplied"}
            for Row in RowsCouponsByIdAll:
                CouponsByIdAll = CouponModel(
                    Row[0], Row[1], Row[2], Row[3], Row[4], Row[5])
                ConnectionSqlite.close()
                return CouponsByIdAll.json(), 200
            return {'message': 'Coupon Invalid Code supplied'}, 400
        except sqlite3.Error as er:
            return {'message': 'Coupon not found'}, 404

    @classmethod
    def DeleteById(cls, id):
        try:
            ConnectionSqlite = sqlite3.connect(CouponModel.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultDeleteCoupon = CursorSqlite.execute(
                'DELETE FROM coupons WHERE id=?;', (id,))
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if ResultDeleteCoupon.rowcount:
                return {'message': 'Coupon successfully delete'}, 200
            return {'message': 'Coupon Invalid ID supplied'}, 400
        except sqlite3.Error as er:
            return {'message': 'Coupon not delete'}, 404

    @classmethod
    def UpdateById(cls, id, body):
        try:
            ConnectionSqlite = sqlite3.connect(CouponModel.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultUpdateCoupon = CursorSqlite.execute(
                'UPDATE coupons SET active = ?, type = ?, code = ?, quantity = ?, value = ? WHERE id=?;', (int(body['active']), str(body['type']), str(body['code']), int(body['quantity']), float(body['value']), id))
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if ResultUpdateCoupon.rowcount:
                return {'message': 'Coupon successfully edited'}, 200
            return {'message': 'Coupon Invalid ID supplied'}, 400
        except sqlite3.Error as er:
            return {'message': 'Coupon not edited'}, 404

    @classmethod
    def InsertData(cls, body):
        try:
            ConnectionSqlite = sqlite3.connect(CouponModel.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultInsertCoupon = CursorSqlite.execute(
                'INSERT INTO coupons VALUES(NULL, ?, ?, ?, ?, ?)', (int(body['active']), str(body['type']), str(body['code']), int(body['quantity']), float(body['value'])))
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if ResultInsertCoupon.rowcount:
                return {'message': 'Coupon successfully created'}, 201
            return {'message': 'Coupon not created'}, 400
        except sqlite3.Error as er:
            return {'message': 'Coupon not created'}, 404

    @classmethod
    def FindAll(cls):
        try:
            CouponsList = list()
            ConnectionSqlite = sqlite3.connect(CouponModel.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultCouponsAll = CursorSqlite.execute('SELECT * FROM coupons')
            RowsCouponsAll = ResultCouponsAll.fetchall()
            for Row in RowsCouponsAll:
                CouponsList.append(CouponModel(
                    Row[0], Row[1], Row[2], Row[3], Row[4], Row[5]))
            ConnectionSqlite.close()
            if len(CouponsList) >= 0:
                return [coupon.json() for coupon in CouponsList], 200
            return {'message': 'Coupon not found'}, 400
        except sqlite3.Error as er:
            return {'message': 'Coupon not found'}, 404
