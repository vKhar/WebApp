import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
# In production, set SECRET_KEY environment variable to a secure random value
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-please-change-in-production')

DATABASE = 'products.db'

def get_db():
    """Create a database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with the products table."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            price REAL NOT NULL,
            image TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """Landing page displaying the product catalogue."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    return render_template('products.html', data=products)

@app.route('/admin')
def admin():
    """Admin page for managing products."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    return render_template('admin.html', products=products)

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    """Add a new product."""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        image = request.form.get('image')
        
        if name and description and price and image:
            conn = get_db()
            try:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO products (name, description, price, image) VALUES (?, ?, ?, ?)',
                    (name, description, float(price), image)
                )
                conn.commit()
                flash('Product added successfully!', 'success')
                return redirect(url_for('admin'))
            except Exception as e:
                flash(f'Error adding product: {str(e)}', 'error')
            finally:
                conn.close()
        else:
            flash('All fields are required!', 'error')
    
    return render_template('add_product.html')

@app.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    """Edit an existing product."""
    conn = get_db()
    try:
        cursor = conn.cursor()
        
        if request.method == 'POST':
            name = request.form.get('name')
            description = request.form.get('description')
            price = request.form.get('price')
            image = request.form.get('image')
            
            if name and description and price and image:
                try:
                    cursor.execute(
                        'UPDATE products SET name=?, description=?, price=?, image=? WHERE id=?',
                        (name, description, float(price), image, product_id)
                    )
                    conn.commit()
                    flash('Product updated successfully!', 'success')
                    return redirect(url_for('admin'))
                except Exception as e:
                    flash(f'Error updating product: {str(e)}', 'error')
            else:
                flash('All fields are required!', 'error')
        
        cursor.execute('SELECT * FROM products WHERE id=?', (product_id,))
        product = cursor.fetchone()
        
        if not product:
            flash('Product not found!', 'error')
            return redirect(url_for('admin'))
        
        return render_template('edit_product.html', product=product)
    finally:
        conn.close()

@app.route('/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    """Delete a product."""
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM products WHERE id=?', (product_id,))
        conn.commit()
        flash('Product deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting product: {str(e)}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('admin'))

if __name__ == '__main__':
    init_db()
    # Debug mode should only be enabled in development
    # Set DEBUG=1 environment variable to enable debug mode
    debug_mode = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 't')
    app.run(debug=debug_mode)
