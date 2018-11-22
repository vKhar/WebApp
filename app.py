from flask import Flask,render_template

app = Flask("__name__")
product_list = [
    {
        "name":"Xenova Rockie",
        "description":"Roomy main compartment with our signature front pocket design",
        "price":42.00,
        "image":"images/backpack.png"
    },
        {
        "name":"Zenon EOS6D",
        "description":"Duis felis orci, pulvinar id metus ut, rutrum luctus orci",
        "price":1392.00,
        "image":"images/camera.png"
    },
        {
        "name":"Schola V",
        "description":"A classical design in matt finish. Durable, tough and resistent to heat and cold",
        "price":342.00,
        "image":"images/glasses.jpg"
    },
        {
        "name":"Scott Digital Smart Band",
        "description":"4/7 heart rate monitoring with Elevate™ wrist heart rate technology",
        "price":365.00,
        "image":"images/watch.png"
    }
]


@app.route("/")
def root():
    return render_template("products.html",data=product_list)

if __name__ == "__main__":
    app.run(debug=True)