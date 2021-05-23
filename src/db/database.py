import sqlite3


def CreateDatabase(db_path):
    ConnectionSqlite = sqlite3.connect(db_path)
    cursorSqlite = ConnectionSqlite.cursor()

    CreateUserTable = '{}{}{}'.format(
        'CREATE TABLE IF NOT EXISTS',
        ' users(id INTEGER PRIMARY KEY,',
        ' email text NOT NULL, name text NOT NULL);'
    )

    cursorSqlite.execute(CreateUserTable)

    CreateProductTable = '{}{}{}'.format(
        'CREATE TABLE IF NOT EXISTS',
        ' products(id INTEGER PRIMARY KEY,',
        ' name text NOT NULL, quantity INTEGER NOT NULL, price INTEGER NOT NULL);'
    )

    cursorSqlite.execute(CreateProductTable)

    CreateCouponTable = '{}{}{}'.format(
        'CREATE TABLE IF NOT EXISTS',
        ' coupons(id INTEGER PRIMARY KEY,',
        ' active INTEGER, type text NOT NULL, code TEXT NOT NULL, quantity INTEGER NOT NULL, value FLOAT NOT NULL);'
    )

    cursorSqlite.execute(CreateCouponTable)

    CreateCartTable = '{}{}{}{}'.format(
        'CREATE TABLE IF NOT EXISTS',
        ' carts(id INTEGER PRIMARY KEY,',
        ' user_id INTEGER NOT NULL, active INTEGER NOT NULL,',
        ' FOREIGN KEY (user_id) REFERENCES users(id));'
    )

    cursorSqlite.execute(CreateCartTable)

    CreateCartProductTable = '{}{}{}{}'.format(
        'CREATE TABLE IF NOT EXISTS',
        ' carts_product(id INTEGER PRIMARY KEY,',
        ' cart_id INTEGER NOT NULL, product_id INTEGER NOT NULL, quantity INTEGER NOT NULL, ',
        ' FOREIGN KEY (cart_id) REFERENCES carts(id), FOREIGN KEY (product_id) REFERENCES products(id));'
    )

    cursorSqlite.execute(CreateCartProductTable)

    CreateCartCouponTable = '{}{}{}{}'.format(
        'CREATE TABLE IF NOT EXISTS',
        ' carts_coupon(id INTEGER PRIMARY KEY,',
        ' cart_id INTEGER NOT NULL, coupon_code TEXT NOT NULL,',
        ' FOREIGN KEY (cart_id) REFERENCES carts(id), FOREIGN KEY (coupon_code) REFERENCES coupon(code));'
    )

    cursorSqlite.execute(CreateCartCouponTable)

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
        'INSERT OR REPLACE INTO coupons VALUES(1, true, "percentage", "TEN10", 10, 10);')
    cursorSqlite.execute(
        'INSERT OR REPLACE INTO coupons VALUES(2, true, "fixed", "FIVE", 10, 5);')

    ConnectionSqlite.commit()

    print('Database successfully Created.')

    ConnectionSqlite.close()
