import sqlite3


class ProductModel:

    db_path = './db/datacart.db'

    def __init__(self, id, name, amount, price):
        self.id = id
        self.name = name
        self.amount = amount
        self.price = price

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
        except sqlite3.Error as er:
            return False

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
                return ResultDeleteProduct.rowcount
        except sqlite3.Error as er:
            return False

    @classmethod
    def UpdateById(cls, id, body):
        try:
            ConnectionSqlite = sqlite3.connect(cls.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultUpdateProduct = CursorSqlite.execute(
                'UPDATE products SET name = ?, amount = ?, price = ? WHERE id=?;', (body.name, body.amount, body.price, id))
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if ResultUpdateProduct.rowcount:
                return ResultUpdateProduct.rowcount
        except sqlite3.Error as er:
            return False

    @classmethod
    def InsertData(cls, body):
        try:
            ConnectionSqlite = sqlite3.connect(cls.db_path)
            CursorSqlite = ConnectionSqlite.cursor()
            ResultInsertProduct = CursorSqlite.execute(
                'INSERT INTO products VALUES(NULL, ?, ?, ?)', (body.name, body.amount, body.price))
            ConnectionSqlite.commit()
            ConnectionSqlite.close()
            if ResultInsertProduct.rowcount:
                return ResultInsertProduct.rowcount
        except sqlite3.Error as er:
            return False

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
            return ProductList
        except sqlite3.Error as er:
            return False

    def json(self):
        return {'id': self.id,
                'name': self.name,
                'amount': self.amount,
                'price': self.price}
