# WebApp

Flask product catalogue app with SQLite persistence and full product management.

## Features
- View product catalogue
- Add new products
- Edit existing products
- Delete products
- Attach/upload product images (PNG, JPG, JPEG, GIF, WEBP)
- Responsive UI built with HTML/CSS only (no JavaScript)

## Run
1. Create and activate a virtual environment.
2. Install Flask:

```bash
pip install flask
```

3. Start the app:

```bash
python app.py
```

4. Open `http://127.0.0.1:5000`.

## Storage
- Database: `catalogue.db` (created automatically)
- Uploaded images: `static/uploads/`
