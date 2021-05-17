import sqlite3

def create_database(db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()