import sqlite3
from models.product import ProductModel
from models.coupon import CouponModel


class CartModel:

    db_path = './db/datacart.db'

    def __init__(self, id, quantity, products_id, user_id, coupon_id):
        self.id = id
        self.quantity = quantity
        self.products_id = products_id
        self.user_id = user_id
        self.coupon_id = coupon_id

    def __repr__(self):
        return str(self.id) + ", " + str(self.products_id) + ", " + str(self.quantity) + ", " + str(self.user_id) + ", " + str(self.coupon_id)

    @classmethod
    def FindById(cls, user_id):
        # try:
        #     CartList = list()
        #     ConnectionSqlite = sqlite3.connect(cls.db_path)
        #     CursorSqlite = ConnectionSqlite.cursor()
        #     ResultCartById = CursorSqlite.execute(
        #         'SELECT * FROM carts WHERE user_id=?', (user_id,))
        #     RowsCartByIdAll = ResultCartById.fetchall()
        #     for Row in RowsCartByIdAll:
        #         ProductByIdStr = str(ProductModel.FindById(Row[2]))
        #         ProductByIdSplit = ProductByIdStr.split(",")
        #         if Row[4] is None:
        #             CartList.append(CartModel(
        #                 Row[0], Row[1], ProductModel(
        #                     ProductByIdSplit[0], ProductByIdSplit[1],  ProductByIdSplit[2], ProductByIdSplit[3]).json(), Row[3], Row[4]))
        #         else:
        #             CouponByIdStr = str(CouponModel.FindById(Row[4]))
        #             CouponByIdSplit = CouponByIdStr.split(",")
        #             CartList.append(CartModel(
        #                 Row[0], Row[1], ProductModel(
        #                     ProductByIdSplit[0], ProductByIdSplit[1],  ProductByIdSplit[2], ProductByIdSplit[3]).json(), Row[3], CouponModel(
        #                     CouponByIdSplit[0], CouponByIdSplit[1],  CouponByIdSplit[2], CouponByIdSplit[3], CouponByIdSplit[4], CouponByIdSplit[5]).json()))

        #     ConnectionSqlite.close()
        #     return CartList
        # except sqlite3.Error as er:
        #     return False
        return False

    @classmethod
    def FindAll(cls):
        # try:
        #     CartList = list()
        #     ConnectionSqlite = sqlite3.connect(cls.db_path)
        #     CursorSqlite = ConnectionSqlite.cursor()
        #     ResultCartAll = CursorSqlite.execute('SELECT * FROM carts_product')
        #     RowsCartAll = ResultCartAll.fetchall()
        #     print(RowsCartAll)
        #     # for Row in RowsCartAll:
        #     #     CartList.append(CartModel(
        #     #         Row[0], Row[1], Row[2], Row[3], Row[4]))
        #     ConnectionSqlite.close()
        #     return True
        # except sqlite3.Error as er:
        #     return False
        return False

    @classmethod
    def UpdateById(cls, user_id, products_id, body):
        # try:
        #     ConnectionSqlite = sqlite3.connect(cls.db_path)
        #     CursorSqlite = ConnectionSqlite.cursor()
        #     ResultUpdateCart = CursorSqlite.execute(
        #         'UPDATE carts SET quantity = ? WHERE user_id=? AND products_id=?;', (body.quantity, user_id, products_id))
        #     ConnectionSqlite.commit()
        #     ConnectionSqlite.close()
        #     if ResultUpdateCart.rowcount:
        #         return ResultUpdateCart.rowcount
        # except sqlite3.Error as er:
        return False

    @classmethod
    def InsertData(cls, body):
        CartId = CartModel.InsertByCartId(str(body['user_id']))
        CartList = list()
        for Row in body['products']:
            CartInsertList = CartModel.InsertByProductId(
                CartId, str(Row['id']), str(Row['quantity']))
            if CartInsertList['status'] is False:
                return {'code': 401, 'message': CartInsertList['message']}, 401
            CartList.append(CartInsertList)
        CouponId = None
        if body['coupon_code'] is not None:
            CouponId = CartModel.InsertByCouponId(
                CartId, str(body['coupon_code']))
            if CouponId['status'] is False:
                return {'code': 401, 'message': CouponId['message']}, 401

        return {'code': 201, 'message': 'Cart successfully created'}, 201

    def DeleteByCartId(cls, id):
        try:
            ConnectionSqlite = sqlite3.connect(cls.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultDeleteCart = CursorSqlite.execute(
                'DELETE FROM carts WHERE id=?', (id,))
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if ResultDeleteCart.rowcount:
                return ResultDeleteCart.rowcount
            return False
        except sqlite3.Error as er:
            return False

    def DeleteByProductId(cls, user_id, product_id):
        try:
            ConnectionSqlite = sqlite3.connect(cls.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultDeleteCart = CursorSqlite.execute(
                'DELETE FROM carts_product WHERE id=? AND products_id=?;', (user_id, products_id))
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if ResultDeleteCart.rowcount:
                return ResultDeleteCart.rowcount
            return False
        except sqlite3.Error as er:
            return False

    def DeleteByCouponId(cls, user_id, coupon_id):
        try:
            ConnectionSqlite = sqlite3.connect(cls.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultUpdateCart = CursorSqlite.execute(
                'DELETE FROM carts_coupon WHERE id=? AND coupon_id=?;', (user_id, coupon_id))
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if ResultUpdateCart.rowcount:
                return ResultUpdateCart.rowcount
            return False
        except sqlite3.Error as er:
            return False

    def InsertByCartId(user_id):
        try:
            ConnectionSqlite = sqlite3.connect('./db/datacart.db')
            CursorSqlite = ConnectionSqlite.cursor()
            ResultInsertCart = CursorSqlite.execute(
                'INSERT INTO carts VALUES(NULL, ?)', (user_id))
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if ResultInsertCart.rowcount:
                return ResultInsertCart.lastrowid
        except sqlite3.Error as er:
            return False

    def InsertByProductId(cart_id, product_id, product_quantity):
        try:
            ConnectionSqlite = sqlite3.connect('./db/datacart.db')
            CursorSqlite = ConnectionSqlite.cursor()
            CheckProductQuantity = CartModel.CheckProductbyQuantity(
                product_id, product_quantity)
            if CheckProductQuantity['status'] is False:
                return {'status': False, 'message': CheckProductQuantity['message']}
            ResultInsertCartProduct = CursorSqlite.execute(
                'INSERT INTO carts_product VALUES(NULL, ?, ?, ?)', (cart_id, product_id, product_quantity))
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if ResultInsertCartProduct.rowcount:
                return {'status': True}
            return {'status': False, 'message': 'Cart not created'}
        except sqlite3.Error as er:
            return {'status': False, 'message': CheckProductQuantity['message']}

    def InsertByCouponId(cart_id, coupon_code):
        try:
            ConnectionSqlite = sqlite3.connect('./db/datacart.db')
            CursorSqlite = ConnectionSqlite.cursor()
            CheckCouponQuantity = CartModel.CheckProductbyCoupon(
                coupon_code)
            if CheckCouponQuantity['status'] is False:
                return {'status': False, 'message': CheckCouponQuantity['message']}
            ResultInsertCartCoupon = CursorSqlite.execute(
                'INSERT INTO carts_coupon VALUES(NULL, ?, ?)', (cart_id, coupon_code))
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if ResultInsertCartCoupon.rowcount:
                return {'status': True}
            return {'status': False, 'message': 'Coupon not available'}
        except sqlite3.Error as er:
            return {'status': False, 'message': 'Coupon not available'}

    def CheckProductbyQuantity(product_id, product_quantity):
        try:
            ConnectionSqlite = sqlite3.connect('./db/datacart.db')
            CursorSqlite = ConnectionSqlite.cursor()
            ResultProductQuantity = CursorSqlite.execute(
                'SELECT quantity FROM products WHERE id=?', (product_id))
            GetProductQuantity = ResultProductQuantity.fetchone()
            if GetProductQuantity is None:
                return {'status': False, 'message': "Product id not found"}
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if int(GetProductQuantity[0]) >= int(product_quantity):
                return {'status': True}
            return {'status': False, 'message': "Product out of stock"}
        except sqlite3.Error as er:
            return {'status': False, 'message': "Product not available"}

    def CheckProductbyCoupon(coupon_code):
        try:
            ConnectionSqlite = sqlite3.connect('./db/datacart.db')
            CursorSqlite = ConnectionSqlite.cursor()
            ResultCouponQuantity = CursorSqlite.execute(
                f'SELECT quantity FROM coupons WHERE code="{coupon_code}"')
            GetCouponQuantity = ResultCouponQuantity.fetchone()
            if GetCouponQuantity is None:
                return {'status': False, 'message': "Coupon not found"}
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if int(GetCouponQuantity[0]) >= 1:
                return {'status': True}
            return {'status': False, 'message': "Coupon out of stock"}
        except sqlite3.Error as er:
            return {'status': False, 'message': "Coupon not available"}

    def json(self):
        return {'id': self.id,
                'quantity': self.quantity,
                'products_id': self.products_id,
                'user_id': self.user_id,
                'coupon_id': self.coupon_id}
