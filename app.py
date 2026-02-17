from flask import Flask, render_template

app = Flask("__name__")

product_list = [
    {"name": ""}
]


@app.route("/")
def root():
    return render_template("products.html")


@app.route("/insert-product")
def insert_product():
    return render_template("insert_product.html")


if __name__ == "__main__":
    app.run(debug=True)
