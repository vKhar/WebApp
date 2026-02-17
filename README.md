# Product Management Web Application

A Flask-based web application for managing a product catalog with a responsive UI.

## Features

- **Product Catalog**: Display all products with images, descriptions, and prices
- **Admin Dashboard**: Manage products with a clean table interface
- **CRUD Operations**: Add, edit, and delete products
- **Responsive Design**: Mobile-friendly interface that adapts to different screen sizes
- **Database-backed**: SQLite database for persistent storage
- **Server-side rendering**: Pure HTML/CSS with Jinja2 templates (no client-side JavaScript)

## Requirements

- Python 3.7+
- Flask 3.0.0
- Werkzeug 3.0.1

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Migrate existing data from JSON to SQLite database:
```bash
python migrate_data.py
```

3. Run the application:
```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000/`

## Usage

### Viewing the Product Catalog
- Navigate to the home page (`/`) to view all products
- Products are displayed in a responsive grid layout

### Managing Products
- Click "Manage Catalogue" in the navigation menu to access the admin dashboard
- Use the "Add New Product" button to create new products
- Click "Edit" next to any product to modify its details
- Click "Delete" to remove a product (confirmation required)

### Adding Products
When adding or editing products, provide:
- **Product Name**: Name of the product
- **Description**: Brief description
- **Price**: Product price in USD
- **Image Path**: Path to the product image relative to the static folder (e.g., `images/product.png`)

## Configuration

### Debug Mode
By default, debug mode is disabled for security. To enable debug mode during development:
```bash
export DEBUG=1
python app.py
```

### Secret Key
The application uses a default secret key for development. In production, set a secure secret key:
```bash
export SECRET_KEY='your-secure-random-key-here'
python app.py
```

## File Structure

```
.
├── app.py                      # Main Flask application
├── migrate_data.py             # Database migration script
├── requirements.txt            # Python dependencies
├── products.db                 # SQLite database (created after migration)
├── static/
│   ├── data.json              # Original product data
│   ├── products.css           # Main stylesheet
│   ├── admin.css              # Admin interface styles
│   └── images/                # Product images
└── templates/
    ├── products.html          # Product catalog page
    ├── admin.html             # Admin dashboard
    ├── add_product.html       # Add product form
    └── edit_product.html      # Edit product form
```

## Security Notes

1. **Secret Key**: Change the default secret key in production using the `SECRET_KEY` environment variable
2. **Debug Mode**: Ensure debug mode is disabled in production
3. **CSRF Protection**: For production use, consider implementing CSRF protection with Flask-WTF
4. **Database**: The SQLite database file is excluded from version control via `.gitignore`

## Screenshots

- **Landing Page**: Product catalog with responsive grid layout
- **Admin Dashboard**: Table view with edit and delete options
- **Add/Edit Forms**: Clean forms with validation
- **Flash Messages**: User feedback for actions

## License

This project is part of a demonstration web application.
