import sqlite3


def CreateDatabase(db_path):
    ConnectionSqlite = sqlite3.connect(db_path)
    cursorSqlite = ConnectionSqlite.cursorSqlite()

    CreateUserTable = '{}{}{}'.format(
        'CREATE TABLE IF NOT EXISTS',
        ' users(id INTEGER PRIMARY KEY,',
        ' email text NOT NULL, name text NOT NULL);'
    )

    cursorSqlite.execute(CreateUserTable)

    CreateProductTable = '{}{}{}'.format(
        'CREATE TABLE IF NOT EXISTS',
        ' products(id INTEGER PRIMARY KEY,',
        ' name text NOT NULL, amount INTEGER NOT NULL, price INTEGER NOT NULL);'
    )

    cursorSqlite.execute(CreateProductTable)

    CreateCouponTable = '{}{}{}{}'.format(
        'CREATE TABLE IF NOT EXISTS',
        ' coupons(id INTEGER PRIMARY KEY,',
        ' active INTEGER, type INTEGER NOT NULL, code INTEGER NOT NULL, value INTEGER NOT NULL);'
    )

    cursorSqlite.execute(CreateCouponTable)

    CreateCartTable = '{}{}{}{}'.format(
        'CREATE TABLE IF NOT EXISTS',
        ' carts(id INTEGER PRIMARY KEY,',
        ' price FLOAT, products_id INTEGER NOT NULL, user_id INTEGER NOT NULL, cupon_id INTEGER NULL,',
        '  FOREIGN KEY (products_id) REFERENCES products(id), FOREIGN KEY (user_id) REFERENCES users(id), FOREIGN KEY (cupon_id) REFERENCES cupons(id));'
    )

    cursorSqlite.execute(CreateCartTable)    

    cursorSqlite.execute(
        'INSERT OR REPLACE INTO users VALUES(1, "admin@exemple.com", "admin");')

    cursorSqlite.execute(
        'INSERT OR REPLACE INTO products VALUES(1, "Remote control car", 1, 99.99);')
    cursorSqlite.execute(
        'INSERT OR REPLACE INTO products VALUES(2, "Electric bike", 1, 5080.99);')
    cursorSqlite.execute(
        'INSERT OR REPLACE INTO products VALUES(3, "Smartphone", 5, 1559.99);')
    cursorSqlite.execute(
        'INSERT OR REPLACE INTO products VALUES(4, "Smartwatch", 10, 580.99);')

    cursorSqlite.execute(
        'INSERT OR REPLACE INTO coupons VALUES(1, true, "percentage", 10);')

    ConnectionSqlite.commit()

    print('Database successfully Created.')

    ConnectionSqlite.close()