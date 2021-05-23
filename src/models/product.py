import sqlite3


class ProductModel:

    db_path = './src/db/datacart.db'

    def __init__(self, id, name, quantity, price):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.price = price

    def __repr__(self):
        return str(self.id) + ", " + self.name + ", " + str(self.quantity) + ", " + str(self.price)

    def json(self):
        return {'id': self.id,
                'name': self.name,
                'quantity': self.quantity,
                'price': self.price}

    @classmethod
    def FindById(cls, id):
        try:
            ConnectionSqlite = sqlite3.connect(ProductModel.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultProductById = CursorSqlite.execute(
                'SELECT * FROM products WHERE id=?', (id,))
            RowsProductByIdAll = ResultProductById.fetchall()
            for Row in RowsProductByIdAll:
                ProductByIdAll = ProductModel(Row[0], Row[1], Row[2], Row[3])
                ConnectionSqlite.close()
                return ProductByIdAll.json(), 200
            return {'message': 'Product Invalid ID supplied'}, 400
        except sqlite3.Error as er:
            return {'message': 'Product not found'}, 404

    @classmethod
    def DeleteById(cls, id):
        try:
            ConnectionSqlite = sqlite3.connect(ProductModel.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultDeleteProduct = CursorSqlite.execute(
                'DELETE FROM products WHERE id=?;', (id,))
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if ResultDeleteProduct.rowcount:
                return {'message': 'Product successfully delete'}, 200
            return {'message': 'Product Invalid ID supplied'}, 400
        except sqlite3.Error as er:
            return {'message': 'Product not found'}, 404

    @classmethod
    def UpdateById(cls, id, body):
        try:
            ConnectionSqlite = sqlite3.connect(ProductModel.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultUpdateProduct = CursorSqlite.execute(
                'UPDATE products SET name = ?, quantity = ?, price = ? WHERE id=?;', (str(body['name']), int(body['quantity']), float(body['price']), id))
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if ResultUpdateProduct.rowcount:
                return {'message': 'Product successfully edited'}, 200
            return {'message': 'Product Invalid ID supplied'}, 400
        except sqlite3.Error as er:
            return {'message': 'Product not edited'}, 404

    @classmethod
    def InsertData(cls, body):
        try:
            ConnectionSqlite = sqlite3.connect(ProductModel.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultInsertProduct = CursorSqlite.execute(
                'INSERT INTO products VALUES(NULL, ?, ?, ?)', (str(body['name']), int(body['quantity']), float(body['price'])))
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if ResultInsertProduct.rowcount:
                return {'message': 'Product successfully created'}, 201
            return {'message': 'Product not created'}, 400
        except sqlite3.Error as er:
            return {'message': 'Product not created'}, 404

    @classmethod
    def FindAll(cls):
        try:
            ProductList = list()
            ConnectionSqlite = sqlite3.connect(ProductModel.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultProductAll = CursorSqlite.execute('SELECT * FROM products')
            RowsProductAll = ResultProductAll.fetchall()
            for Row in RowsProductAll:
                ProductList.append(ProductModel(
                    Row[0], Row[1], Row[2], Row[3]))
            ConnectionSqlite.close()
            if len(ProductList) >= 0:
                return [product.json() for product in ProductList], 200
            return {'message': 'Product not found'}, 400
        except sqlite3.Error as er:
            return {'message': 'Product not found'}, 404
