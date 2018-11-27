import sqlite3

con = sqlite3.connect("inventory.db")
con.execute("DROP TABLE products")
con.execute("""CREATE TABLE products
            (name TEXT PRIMARY KEY, description TEXT, price REAL,image TEXT)"""
            )
con.close()