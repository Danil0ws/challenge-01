import sqlite3


class ProductModel:

    db_path = './db/datacart.db'

    def __init__(self, id, name, quantity, price):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.price = price

    def __repr__(self):
        return str(self.id) + ", " + self.name + ", " + str(self.quantity) + ", " + str(self.price)

    @classmethod
    def FindById(cls, id):
        try:
            ConnectionSqlite = sqlite3.connect(cls.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultProductById = CursorSqlite.execute(
                'SELECT * FROM products WHERE id=?', (id,))
            RowsProductByIdAll = ResultProductById.fetchall()
            for Row in RowsProductByIdAll:
                ProductByIdAll = ProductModel(Row[0], Row[1], Row[2], Row[3])
                ConnectionSqlite.close()
                return ProductByIdAll
            return {'code': 400, 'message': 'Product not found'}, 400    
        except sqlite3.Error as er:
            return {'code': 400, 'message': 'Product not found'}, 400

    @classmethod
    def DeleteById(cls, id):
        try:
            ConnectionSqlite = sqlite3.connect(cls.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultDeleteProduct = CursorSqlite.execute(
                'DELETE FROM products WHERE id=?;', (id,))
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if ResultDeleteProduct.rowcount:
                return {'code': 200, 'message': 'Product successfully delete'}, 200
            return {'code': 400, 'message': 'Product not found'}, 400
        except sqlite3.Error as er:
            return {'code': 400, 'message': 'Product not found'}, 400

    @classmethod
    def UpdateById(cls, id, body):
        try:
            ConnectionSqlite = sqlite3.connect(cls.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultUpdateProduct = CursorSqlite.execute(
                'UPDATE products SET name = ?, quantity = ?, price = ? WHERE id=?;', (str(body['name']), int(body['quantity']), int(body['price']), id))
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if ResultUpdateProduct.rowcount:
                return {'code': 201, 'message': 'Product successfully edited'}, 201
            return {'code': 400, 'message': 'Product not edited'}, 400
        except sqlite3.Error as er:
            return {'code': 400, 'message': 'Product not edited'}, 400

    @classmethod
    def InsertData(cls, body):
        try:
            ConnectionSqlite = sqlite3.connect(cls.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultInsertProduct = CursorSqlite.execute(
                'INSERT INTO products VALUES(NULL, ?, ?, ?)', (str(body['name']), int(body['quantity']), int(body['price'])))
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if ResultInsertProduct.rowcount:
                return {'code': 201, 'message': 'Product successfully created'}, 201
            return {'code': 400, 'message': 'Product not created'}, 400
        except sqlite3.Error as er:
            return {'code': 400, 'message': 'Product not created'}, 400

    @classmethod
    def FindAll(cls):
        try:
            ProductList = list()
            ConnectionSqlite = sqlite3.connect(cls.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultProductAll = CursorSqlite.execute('SELECT * FROM products')
            RowsProductAll = ResultProductAll.fetchall()
            for Row in RowsProductAll:
                ProductList.append(ProductModel(
                    Row[0], Row[1], Row[2], Row[3]))
            ConnectionSqlite.close()
            if ProductList.count()>=0:
                return ProductList                
            return {'code': 400, 'message': 'Product not found'}, 400
        except sqlite3.Error as er:
            return {'code': 400, 'message': 'Product not found'}, 400

    def json(self):
        return {'id': self.id,
                'name': self.name,
                'quantity': self.quantity,
                'price': self.price}
