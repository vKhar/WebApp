import json
import sqlite3
import os

def migrate_data():
    """Migrate data from static/data.json to SQLite database."""
    
    # Initialize database
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    
    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            price REAL NOT NULL,
            image TEXT NOT NULL
        )
    ''')
    
    # Check if table is empty
    cursor.execute('SELECT COUNT(*) FROM products')
    count = cursor.fetchone()[0]
    
    if count == 0:
        # Read data from JSON file
        with open('static/data.json', 'r') as f:
            products = json.load(f)
        
        # Insert data into database
        for product in products:
            cursor.execute(
                'INSERT INTO products (name, description, price, image) VALUES (?, ?, ?, ?)',
                (product['name'], product['description'], product['price'], product['image'])
            )
        
        conn.commit()
        print(f"Successfully migrated {len(products)} products to database.")
    else:
        print(f"Database already contains {count} products. Skipping migration.")
    
    conn.close()

if __name__ == '__main__':
    migrate_data()
