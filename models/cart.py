import sqlite3
from models.product import ProductModel
from models.coupon import CouponModel


class CartModel:

    db_path = './db/datacart.db'

    def __init__(self, id, quantity, product_id, user_id, coupon_id):
        self.id = id
        self.quantity = quantity
        self.product_id = product_id
        self.user_id = user_id
        self.coupon_id = coupon_id

    def __repr__(self):
        return str(self.id) + ", " + str(self.product_id) + ", " + str(self.quantity) + ", " + str(self.user_id) + ", " + str(self.coupon_id)

    @classmethod
    def FindById(cls, user_id):
        try:
            CartList = list()
            ConnectionSqlite = sqlite3.connect(cls.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultCartById = CursorSqlite.execute(
                'SELECT * FROM carts WHERE user_id=?', (user_id,))
            RowsCartByIdAll = ResultCartById.fetchall()
            for Row in RowsCartByIdAll:
                ProductByIdStr = str(ProductModel.FindById(Row[2]))
                ProductByIdSplit = ProductByIdStr.split(",")
                if Row[4] is None:
                    CartList.append(CartModel(
                        Row[0], Row[1], ProductModel(
                            ProductByIdSplit[0], ProductByIdSplit[1],  ProductByIdSplit[2], ProductByIdSplit[3]).json(), Row[3], Row[4]))
                else:
                    CouponByIdStr = str(CouponModel.FindById(Row[4]))
                    CouponByIdSplit = CouponByIdStr.split(",")
                    CartList.append(CartModel(
                        Row[0], Row[1], ProductModel(
                            ProductByIdSplit[0], ProductByIdSplit[1],  ProductByIdSplit[2], ProductByIdSplit[3]).json(), Row[3], CouponModel(
                            CouponByIdSplit[0], CouponByIdSplit[1],  CouponByIdSplit[2], CouponByIdSplit[3], CouponByIdSplit[4], CouponByIdSplit[5]).json()))

            ConnectionSqlite.close()
            return CartList
        except sqlite3.Error as er:
            return False

    @classmethod
    def DeleteById(cls, user_id):
        try:
            ConnectionSqlite = sqlite3.connect(cls.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultDeleteCart = CursorSqlite.execute(
                'DELETE FROM carts WHERE user_id=?', (user_id,))
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if ResultDeleteCart.rowcount:
                return ResultDeleteCart.rowcount
        except sqlite3.Error as er:
            return False

    @classmethod
    def DeleteByProductId(cls, user_id, product_id):
        try:
            ConnectionSqlite = sqlite3.connect(cls.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultDeleteCart = CursorSqlite.execute(
                'DELETE FROM carts WHERE id=? AND product_id=?;', (user_id, product_id))
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if ResultDeleteCart.rowcount:
                return ResultDeleteCart.rowcount
        except sqlite3.Error as er:
            return False

    @classmethod
    def UpdateById(cls, user_id, product_id, body):
        try:
            ConnectionSqlite = sqlite3.connect(cls.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultUpdateCart = CursorSqlite.execute(
                'UPDATE carts SET quantity = ? WHERE user_id=? AND product_id=?;', (body.quantity, user_id, product_id))
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if ResultUpdateCart.rowcount:
                return ResultUpdateCart.rowcount
        except sqlite3.Error as er:
            return False

    @ classmethod
    def InsertData(cls, user_id, body):
        try:
            # Falta calida user,product e coupon antes de adicionar
            ConnectionSqlite = sqlite3.connect(cls.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultInsertCart = CursorSqlite.execute(
                'INSERT INTO carts VALUES(NULL, ?, ?, ?, ?)', (body.quantity, body.product_id, user_id, body.coupon_id))
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if ResultInsertCart.rowcount:
                return ResultInsertCart.rowcount
        except sqlite3.Error as er:
            return False

    @ classmethod
    def FindAll(cls):
        try:
            CartList = list()
            ConnectionSqlite = sqlite3.connect(cls.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultCartAll = CursorSqlite.execute('SELECT * FROM carts')
            RowsCartAll = ResultCartAll.fetchall()
            for Row in RowsCartAll:
                CartList.append(CartModel(
                    Row[0], Row[1], Row[2], Row[3], Row[4]))
            ConnectionSqlite.close()
            return CartList
        except sqlite3.Error as er:
            return False

    def json(self):
        return {'id': self.id,
                'quantity': self.quantity,
                'product_id': self.product_id,
                'user_id': self.user_id,
                'coupon_id': self.coupon_id}
