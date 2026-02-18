from __future__ import annotations

import sqlite3
import uuid
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "catalogue.db"
UPLOAD_FOLDER = BASE_DIR / "static" / "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-key"
app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

    with get_db_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                price REAL NOT NULL CHECK (price >= 0),
                image_path TEXT
            )
            """
        )

        count = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        if count == 0:
            conn.executemany(
                "INSERT INTO products (name, description, price, image_path) VALUES (?, ?, ?, ?)",
                [
                    (
                        "Xenova Rockie",
                        "Roomy main compartment with our signature front pocket design",
                        42.0,
                        "images/backpack.png",
                    ),
                    (
                        "Zanon EOS6D",
                        "Full-frame camera built for sharp images and reliable low-light performance.",
                        1392.0,
                        "images/camera.png",
                    ),
                    (
                        "Schola V",
                        "A classical design in matt finish. Durable and resistant to heat and cold.",
                        342.0,
                        "images/glasses.jpg",
                    ),
                    (
                        "Scott Digital Smart Band",
                        "Heart-rate monitoring, stress tracking, and advanced fitness insights.",
                        365.0,
                        "images/watch.png",
                    ),
                ],
            )
        conn.commit()


def is_allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_image(file_storage) -> str | None:
    if not file_storage or not file_storage.filename:
        return None

    if not is_allowed_file(file_storage.filename):
        return None

    safe_name = secure_filename(file_storage.filename)
    unique_name = f"{uuid.uuid4().hex}_{safe_name}"
    destination = UPLOAD_FOLDER / unique_name
    file_storage.save(destination)
    return f"uploads/{unique_name}"


@app.route("/")
def root():
    return redirect(url_for("product_list"))


@app.route("/products")
def product_list():
    with get_db_connection() as conn:
        products = conn.execute("SELECT * FROM products ORDER BY id DESC").fetchall()
    return render_template("products.html", products=products)


@app.route("/products/new", methods=["GET", "POST"])
def product_create():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        price_raw = request.form.get("price", "").strip()
        image_file = request.files.get("image")

        errors = []
        if not name:
            errors.append("Product name is required.")
        if not description:
            errors.append("Product description is required.")

        try:
            price = float(price_raw)
            if price < 0:
                errors.append("Price must be zero or greater.")
        except ValueError:
            errors.append("Price must be a valid number.")
            price = 0.0

        image_path = save_image(image_file)
        if image_file and image_file.filename and not image_path:
            errors.append("Image must be png, jpg, jpeg, gif, or webp.")

        if errors:
            for error in errors:
                flash(error, "error")
            form_data = {"name": name, "description": description, "price": price_raw}
            return render_template("product_form.html", mode="create", product=form_data)

        with get_db_connection() as conn:
            conn.execute(
                "INSERT INTO products (name, description, price, image_path) VALUES (?, ?, ?, ?)",
                (name, description, price, image_path),
            )
            conn.commit()

        flash("Product added.", "success")
        return redirect(url_for("product_list"))

    return render_template("product_form.html", mode="create", product={})


@app.route("/products/<int:product_id>/edit", methods=["GET", "POST"])
def product_edit(product_id: int):
    with get_db_connection() as conn:
        product = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()

    if product is None:
        flash("Product not found.", "error")
        return redirect(url_for("product_list"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        price_raw = request.form.get("price", "").strip()
        image_file = request.files.get("image")

        errors = []
        if not name:
            errors.append("Product name is required.")
        if not description:
            errors.append("Product description is required.")

        try:
            price = float(price_raw)
            if price < 0:
                errors.append("Price must be zero or greater.")
        except ValueError:
            errors.append("Price must be a valid number.")
            price = 0.0

        image_path = product["image_path"]
        new_image_path = save_image(image_file)
        if image_file and image_file.filename and not new_image_path:
            errors.append("Image must be png, jpg, jpeg, gif, or webp.")
        if new_image_path:
            image_path = new_image_path

        if errors:
            for error in errors:
                flash(error, "error")
            form_data = {
                "id": product_id,
                "name": name,
                "description": description,
                "price": price_raw,
                "image_path": image_path,
            }
            return render_template("product_form.html", mode="edit", product=form_data)

        with get_db_connection() as conn:
            conn.execute(
                """
                UPDATE products
                SET name = ?, description = ?, price = ?, image_path = ?
                WHERE id = ?
                """,
                (name, description, price, image_path, product_id),
            )
            conn.commit()

        flash("Product updated.", "success")
        return redirect(url_for("product_list"))

    return render_template("product_form.html", mode="edit", product=product)


@app.route("/products/<int:product_id>/delete", methods=["GET", "POST"])
def product_delete(product_id: int):
    with get_db_connection() as conn:
        product = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()

    if product is None:
        flash("Product not found.", "error")
        return redirect(url_for("product_list"))

    if request.method == "POST":
        with get_db_connection() as conn:
            conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
            conn.commit()

        flash("Product deleted.", "success")
        return redirect(url_for("product_list"))

    return render_template("product_delete.html", product=product)


init_db()

if __name__ == "__main__":
    app.run(debug=True)
