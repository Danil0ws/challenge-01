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
        Coupon = None
        ConnectionSqlite = sqlite3.connect(cls.db_path)
        CursorSqlite = ConnectionSqlite.cursor()
        ResultCartById = CursorSqlite.execute(
            'SELECT * FROM carts WHERE user_id=?', (user_id,))
        RowsCartById = ResultCartById.fetchall()
        for Row in RowsCartById:
            GetProductById = CartModel.FindByProductId(Row[0])
            GetCouponById = CartModel.FindByCouponId(Row[0])
            # print(GetProductById)
            # print(GetCouponById)
            # GetProductById = CartModel.FindByProductId(Row[0])
            # GetCouponById = CartModel.FindByCouponId(Row[0])
            # ProductList.append(GetProductById[0]['product'])
            # GetProductById[0]['product']
        # print(ProductList)
        return False

    @classmethod
    def FindAll(cls):
        # try:
        CartList = list()
        ConnectionSqlite = sqlite3.connect(cls.db_path)
        CursorSqlite = ConnectionSqlite.cursor()
        ResultCartAll = CursorSqlite.execute('SELECT * FROM carts')
        RowsCartAll = ResultCartAll.fetchall()
        print(RowsCartAll)
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
                CartId['message'], str(Row['id']), str(Row['quantity']))
            if CartInsertList['status'] is False:
                return {'code': 400, 'message': CartInsertList['message']}, 400
            CartList.append(CartInsertList)
        CouponId = None
        if body['coupon_code'] is not None:
            CouponId = CartModel.InsertByCouponId(
                CartId['message'], str(body['coupon_code']))
            if CouponId['status'] is False:
                return {'code': 400, 'message': CouponId['message']}, 400
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
                return {'code': 200, 'message': 'Coupon successfully delete'}, 200
            return {'code': 400, 'message': 'Coupon not delete'}, 400
        except sqlite3.Error as er:
            return {'code': 400, 'message': 'Coupon not delete'}, 400

    def InsertByCartId(user_id):
        try:
            ConnectionSqlite = sqlite3.connect('./db/datacart.db')
            CursorSqlite = ConnectionSqlite.cursor()
            ResultInsertCart = CursorSqlite.execute(
                'INSERT INTO carts VALUES(NULL, ?)', (user_id))
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if ResultInsertCart.rowcount:
                return {'code': 200, 'message': ResultInsertCart.lastrowid}
            return {'code': 400, 'message': 'Cart not created'}
        except sqlite3.Error as er:
            return {'code': 400, 'message': 'Cart not created'}

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
            print(CheckProductQuantity)
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

    def FindByProductId(cart_id):
        ConnectionSqlite = sqlite3.connect(cls.db_path)
        CursorSqlite = ConnectionSqlite.cursor()
        ResultCartProductById = CursorSqlite.execute(
            'SELECT * FROM carts_product WHERE cart_id=?', (cart_id,))
        RowsCartProductById = ResultCartProductById.fetchall()
        if len(RowsCartProductById) == 0:
            return False
        ProductList = list()
        for Row in RowsCartProductById:
            GetProductById = ProductModel.FindById(Row[2])
            GetProductById[0]['product']['quantity'] = Row[3]
            ProductList.append(GetProductById[0]['product'])
        return ProductList

    def FindByCouponId(cart_id):
        ConnectionSqlite = sqlite3.connect(cls.db_path)
        CursorSqlite = ConnectionSqlite.cursor()
        ResultCartCouponById = CursorSqlite.execute(
            'SELECT * FROM carts_coupon WHERE cart_id=?', (cart_id,))
        RowsCartCouponById = ResultCartCouponById.fetchall()
        if len(RowsCartCouponById) == 0:
            return False
        for Row in RowsCartCouponById:
            GetCouponById = CouponModel.FindById(Row[2])
            return GetCouponById[0]['coupon']
        return False

    def json(self):
        return {'id': self.id,
                'quantity': self.quantity,
                'products_id': self.products_id,
                'user_id': self.user_id,
                'coupon_id': self.coupon_id}
