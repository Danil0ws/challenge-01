import sqlite3
from models.product import ProductModel
from models.coupon import CouponModel


class CartModel:

    db_path = './src/db/datacart.db'

    def __init__(self, id, user_id, products, coupon_code, disconut, subtotal, total):
        self.id = id
        self.user_id = user_id
        self.products = products
        self.coupon_code = coupon_code
        self.disconut = disconut
        self.subtotal = subtotal
        self.total = total

    def __repr__(self):
        return str(self.id) + ", " + str(self.user_id) + ", " + str(self.products) + ", " + str(self.coupon_code) + ", " + str(self.disconut) + ", " + str(self.subtotal) + ", " + str(self.total)

    def json(self):
        return {'id': self.id,
                'user_id': self.user_id,
                'products': self.products,
                'coupon_code': self.coupon_code,
                'disconut': self.disconut,
                'subtotal': self.subtotal,
                'total': self.total}

    @classmethod
    def FindByIdComplete(cls, user_id):
        try:
            CartId = None
            CartUserId = None
            CartCoupon = None
            CartDisconut = 0
            CartTotal = 0
            CartSubTotal = 0
            ConnectionSqlite = sqlite3.connect(CartModel.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultCartById = CursorSqlite.execute(
                'SELECT * FROM carts WHERE user_id=? AND active=1', (user_id,))
            RowsCartById = ResultCartById.fetchone()
            if RowsCartById is None:
                return {"message": "Cart is empty"}, 400
            CartId = RowsCartById[0]
            CartUserId = RowsCartById[1]
            CartProductRow = CartModel.FindByProductId(RowsCartById[0])
            GetCouponById = CartModel.FindByCouponId(RowsCartById[0])
            if CartProductRow is False:
                CartModel.DeactivatedByCartId(CartId)
                return {"message": "Cart is empty"}, 400
            for Row in CartProductRow:
                CartTotal = CartTotal + float(Row['price'])
                CartSubTotal = CartSubTotal + float(Row['price'])
                if GetCouponById is not False:
                    CartCoupon = GetCouponById['code']
                    if GetCouponById['type'] == 'fixed':
                        CartDisconut = float(GetCouponById['value'])
                        CartTotal = CartTotal - CartDisconut
                    else:
                        CartDisconut = (CartTotal / 100) * \
                            float(GetCouponById['value'])
                        CartTotal = CartTotal - CartDisconut
            CartReturn = CartModel(
                CartId, CartUserId, CartProductRow, CartCoupon, float("{:.2f}".format(CartDisconut)), float("{:.2f}".format(CartSubTotal)), float("{:.2f}".format(CartTotal)))
            return CartReturn.json(), 200
        except sqlite3.Error as er:
            return {"message": "Cart not found"}, 404

    @ classmethod
    def FindAllComplete(cls):
        try:
            CartList = list()
            ConnectionSqlite = sqlite3.connect(CartModel.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultCartAll = CursorSqlite.execute(
                'SELECT * FROM carts WHERE active=1')
            RowsCartAll = ResultCartAll.fetchall()
            if len(RowsCartAll) == 0:
                return {"message": "Carts not found"}, 400
            CartAll = list()
            for Row in RowsCartAll:
                GetFindById = CartModel.FindByIdComplete(Row[1])
                CartAll.append(GetFindById[0])
            return CartAll, 200
        except sqlite3.Error as er:
            return {"message": "Carts not found"}, 404

    @ classmethod
    def InsertNewByProductId(cls, user_id, body):
        try:
            ConnectionSqlite = sqlite3.connect(CartModel.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            CartFindById = CartModel.FindById(int(user_id))
            for Row in body['products']:
                CartInsertList = CartModel.InsertByProductId(
                    int(CartFindById['message']), int(Row['id']), int(Row['quantity']))
                if CartInsertList['status'] is False:
                    return {'message': CartInsertList['message']}, 400
            return {'message': 'Product successfully added in cart'}, 200
        except sqlite3.Error as er:
            return {'message': 'Product not added in cart'}, 404

    @ classmethod
    def UpdateByProductId(cls, user_id, product_id, body):
        try:
            ConnectionSqlite = sqlite3.connect(CartModel.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            CartFindById = CartModel.FindById(int(user_id))
            if CartFindById['status'] is False:
                return {'message': CartFindById['message']}, 400
            CheckProductQuantity = CartModel.CheckProductbyQuantity(
                product_id, int(body['quantity']))
            if CheckProductQuantity['status'] is False:
                return {'message': CheckProductQuantity['message']}, 400
            ResultUpdateCart = CursorSqlite.execute(
                'UPDATE carts_product SET quantity = ? WHERE cart_id=? AND product_id=?;', (int(body['quantity']), int(CartFindById['message']), product_id))
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if ResultUpdateCart.rowcount:
                return {'message': 'Product successfully edited in cart'}, 200
            return {'message': 'Product not find in cart'}, 400
        except sqlite3.Error as er:
            return {'message': 'Product not edited in cart'}, 404

    @ classmethod
    def UpdateByCouponId(cls, user_id, body):
        try:
            ConnectionSqlite = sqlite3.connect(CartModel.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            CartFindById = CartModel.FindById(int(user_id))
            if CartFindById['status'] is False:
                return {'message': CartFindById['message']}, 400
            CheckCouponQuantity = CartModel.CheckProductbyCoupon(
                str(body['coupon_code']))
            if CheckCouponQuantity['status'] is False:
                return {'message': CheckCouponQuantity['message']}, 400
            GetCouponById = CartModel.FindByCouponId(
                int(CartFindById['message']))
            if GetCouponById is not False:
                ResultUpdateCart = CursorSqlite.execute(
                    'UPDATE carts_coupon SET coupon_code = ? WHERE cart_id=?;', (str(body['coupon_code']), int(CartFindById['message'])))
                ConnectionSqlite.commit()
                ConnectionSqlite.close()
                return {'message': 'Coupon successfully edited in cart'}, 200
            else:
                CouponId = CartModel.InsertByCouponId(
                    CartFindById['message'], str(body['coupon_code']))
                if CouponId['status'] is False:
                    return {'message': CouponId['message']}, 400
                return {'message': 'Coupon successfully added in cart'}, 200
        except sqlite3.Error as er:
            return {'message': 'Coupon not added in cart'}, 404

    @ classmethod
    def InsertData(cls, user_id, body):
        CartId = CartModel.InsertByCartId(user_id)
        CartList = list()
        for Row in body['products']:
            CartInsertList = CartModel.InsertByProductId(
                CartId['message'], str(Row['id']), str(Row['quantity']))
            if CartInsertList['status'] is False:
                return {'status': False, 'message': CartInsertList['message']}, 400
            CartList.append(CartInsertList)
        CouponId = None
        if body['coupon_code'] is not None:
            CouponId = CartModel.InsertByCouponId(
                CartId['message'], str(body['coupon_code']))
            if CouponId['status'] is False:
                return {'status': False, 'message': CouponId['message']}, 400
        return {'message': 'Cart successfully created'}, 201

    def DeactivatedByCartId(id):
        try:
            ConnectionSqlite = sqlite3.connect(CartModel.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultDeleteCart = CursorSqlite.execute(
                'UPDATE carts SET active = 0 WHERE id=?;', (id,))
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if ResultDeleteCart.rowcount:
                return {'message': 'Cart successfully deactivated'}, 200
            return {'message': 'Cart not deactivated'}, 400
        except sqlite3.Error as er:
            return {'message': 'Cart not found'}, 404

    def DeleteByCartId(user_id):
        try:
            ConnectionSqlite = sqlite3.connect(CartModel.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultCartById = CursorSqlite.execute(
                'SELECT * FROM carts WHERE user_id=? AND active=1', (user_id,))
            RowsCartById = ResultCartById.fetchone()
            if RowsCartById is None:
                return {"message": "Cart not found"}, 400
            CartId = RowsCartById[0]
            ResultDeleteCart = CursorSqlite.execute(
                'DELETE FROM carts WHERE id=?', (CartId,))
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if ResultDeleteCart.rowcount:
                return {'message': 'Cart successfully delete'}, 200
            return {'message': 'Cart not delete'}, 400
        except sqlite3.Error as er:
            return {'message': 'Cart not found'}, 404

    def DeleteByProductId(user_id, product_id=None):
        try:
            ConnectionSqlite = sqlite3.connect(CartModel.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultCartById = CursorSqlite.execute(
                'SELECT * FROM carts WHERE user_id=? AND active=1', (user_id,))
            RowsCartById = ResultCartById.fetchone()
            if RowsCartById is None:
                return {"message": "Cart not found"}, 400
            CartId = RowsCartById[0]
            if product_id is None:
                ResultDeleteCart = CursorSqlite.execute(
                    'DELETE FROM carts_product WHERE cart_id=?;', (CartId,))
            else:
                ResultDeleteCart = CursorSqlite.execute(
                    'DELETE FROM carts_product WHERE cart_id=? AND product_id=?;', (CartId, product_id))
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if ResultDeleteCart.rowcount:
                return {'message': 'Product successfully delete in cart'}, 200
            return {'message': 'Product not delete in cart'}, 400
        except sqlite3.Error as er:
            return {'message': 'Product not delete in cart'}, 404

    def DeleteByCouponId(user_id, coupon_id=None):
        try:
            ConnectionSqlite = sqlite3.connect(CartModel.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultCartById = CursorSqlite.execute(
                'SELECT * FROM carts WHERE user_id=? AND active=1', (user_id,))
            RowsCartById = ResultCartById.fetchone()
            if RowsCartById is None:
                return {"message": "Cart not found"}, 400
            CartId = RowsCartById[0]
            if coupon_id is None:
                ResultUpdateCart = CursorSqlite.execute(
                    'DELETE FROM carts_coupon WHERE cart_id=?;', (CartId,))
            else:
                ResultUpdateCart = CursorSqlite.execute(
                    'DELETE FROM carts_coupon WHERE cart_id=? AND coupon_id=?;', (CartId, coupon_id))
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if ResultUpdateCart.rowcount:
                return {'message': 'Coupon successfully delete in cart'}, 200
            return {'message': 'Coupon not delete in cart'}, 400
        except sqlite3.Error as er:
            return {'message': 'Cart not found'}, 404

    def InsertByCartId(user_id):
        try:
            ConnectionSqlite = sqlite3.connect(CartModel.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            CartIsActived = CartModel.CheckCartIsActived(user_id)
            if CartIsActived['status']:
                DeactivatedByCartId = CartModel.DeactivatedByCartId(
                    int(CartIsActived['message']))
                # DeleteByCartId = CartModel.DeleteByCartId(
                #     int(CartIsActived['message']))
                # DeleteByProductId = CartModel.DeleteByProductId(
                #     int(CartIsActived['message']))
                # DeleteByCouponId = CartModel.DeleteByCouponId(
                #     int(CartIsActived['message']))
                if DeactivatedByCartId:
                    # if DeleteByCartId['status'] or DeleteByProductId['status'] or DeleteByCouponId['status']:
                    {'message': 'Cart not created'}
            ResultInsertCart = CursorSqlite.execute(
                'INSERT INTO carts VALUES(NULL, ?, ?)', (user_id, 1))
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if ResultInsertCart.rowcount:
                return {'message': ResultInsertCart.lastrowid}
            return {'message': 'Cart not created'}
        except sqlite3.Error as er:
            return {'message': 'Cart not created'}

    def InsertByProductId(cart_id, product_id, product_quantity):
        try:
            ConnectionSqlite = sqlite3.connect(CartModel.db_path)
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
            ConnectionSqlite = sqlite3.connect(CartModel.db_path)
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

    def CheckCartIsActived(user_id):
        try:
            ConnectionSqlite = sqlite3.connect(CartModel.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultProductQuantity = CursorSqlite.execute(
                'SELECT * FROM carts WHERE user_id=? AND active=1', (user_id,))
            GetProductQuantity = ResultProductQuantity.fetchone()
            if GetProductQuantity is None:
                return {'status': False}
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if int(GetProductQuantity[0]) >= 0:
                return {'status': True, 'message': GetProductQuantity[0]}
            return {'status': False}
        except sqlite3.Error as er:
            return {'status': False}

    def CheckProductbyQuantity(product_id, product_quantity):
        try:
            ConnectionSqlite = sqlite3.connect(CartModel.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultProductQuantity = CursorSqlite.execute(
                'SELECT quantity FROM products WHERE id=?', (product_id, ))
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
            ConnectionSqlite = sqlite3.connect(CartModel.db_path)
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
        ConnectionSqlite = sqlite3.connect(CartModel.db_path)
        CursorSqlite = ConnectionSqlite.cursor()
        ResultCartProductById = CursorSqlite.execute(
            'SELECT * FROM carts_product WHERE cart_id=?', (cart_id,))
        RowsCartProductById = ResultCartProductById.fetchall()
        if len(RowsCartProductById) == 0:
            return False
        ProductList = list()
        for Row in RowsCartProductById:
            GetProductById = ProductModel.FindById(Row[2])
            GetProductById[0]['quantity'] = Row[3]
            GetProductById[0]['price_unit'] = GetProductById[0]['price']
            GetProductById[0]['price'] = float("{:.2f}".format(float(
                GetProductById[0]['price_unit']) * float(Row[3])))
            ProductList.append(GetProductById[0])
        return ProductList

    def FindByCouponId(cart_id):
        ConnectionSqlite = sqlite3.connect(CartModel.db_path)
        CursorSqlite = ConnectionSqlite.cursor()
        ResultCartCouponById = CursorSqlite.execute(
            'SELECT * FROM carts_coupon WHERE cart_id=?', (cart_id,))
        RowsCartCouponById = ResultCartCouponById.fetchall()
        if len(RowsCartCouponById) == 0:
            return False
        for Row in RowsCartCouponById:
            GetCouponById = CouponModel.FindByCode(Row[2])
            return GetCouponById[0]
        return False

    def FindById(user_id):
        try:
            ConnectionSqlite = sqlite3.connect(CartModel.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultCartById = CursorSqlite.execute(
                'SELECT * FROM carts WHERE user_id=? AND active=1', (user_id,))
            RowsCartById = ResultCartById.fetchone()
            if RowsCartById is None:
                return {"status": False, "message": "Cart not found"}
            CartId = RowsCartById[0]
            return {"status": True, "message": CartId}
        except sqlite3.Error as er:
            return {"status": False, "message": "Cart not found"}
