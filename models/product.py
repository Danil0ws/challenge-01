import sqlite3


class ProductModel:

    def __init__(self, id, amount, price):
        self.id = id
        self.amount = amount
        self.price = price

    @classmethod
    def FindById(cls, id):
        ConnectionSqlite = sqlite3.connect('./db/datacart.db')
        cursorSqlite = ConnectionSqlite.cursor()
        ResultProductById = cursorSqlite.execute(
            'SELECT * FROM products WHERE id=?', (id,))
        RowsProductByIdAll = ResultProductById.fetchall()
        for Row in RowsProductByIdAll:
            ProductByIdAll = ProductModel(Row[0], Row[1], Row[2])
            ConnectionSqlite.close()
            return ProductByIdAll

    @classmethod
    def FindAll(cls):
        ProductList = list()
        ConnectionSqlite = sqlite3.connect('./db/datacart.db')
        cursorSqlite = ConnectionSqlite.cursor()
        ResultProductAll = cursorSqlite.execute('SELECT * FROM products')
        RowsProductAll = ResultProductAll.fetchall()
        for Row in RowsProductAll:
            ProductList.append(ProductModel(Row[0], Row[1], Row[2]))
        return ProductList
        ConnectionSqlite.close()

    def json(self):
        return {'id': self.id,
                'amount': self.amount,
                'price': self.price}
