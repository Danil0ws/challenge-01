import sqlite3


class CartModel:

    def __init__(self, id, products_id, user_id):
        self.price = price
        self.products_id = products_id
        self.user_id = user_id

    def json(self):
        return {'id': self.id,
                'products_id': self.products_id,
                'user_id': self.user_id}
