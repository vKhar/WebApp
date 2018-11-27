## Step 7: remove json file, json load and json save
## use sqlite to list products and add new product
from flask import Flask,render_template,request,redirect,url_for
import os
import sqlite3

app = Flask("__name__")
DB="inventory.db" ## created from sqlitebrowser

@app.route("/")
def root():
    con = sqlite3.connect(DB)
    con.row_factory=sqlite3.Row #name-based access to columns
    cur=con.cursor()
    cur.execute("SELECT * FROM products")
    product_list=cur.fetchall() ## no change in products.html

    return render_template("products.html",data=product_list)

@app.route('/add',methods = ['POST', 'GET'])
def add_product():
    if request.method == 'POST':
        try:
            name=request.form["name"]
            description=request.form["description"]
            price=request.form["price"]
            f=request.files["image"]
            image="images/"+f.filename

            with sqlite3.connect(DB) as con:
                cur=con.cursor()
                cur.execute(
                    "INSERT INTO products(name,description,price,image) VALUES (?,?,?,?)",
                     (name,description,price,image))
                con.commit()
            msg="Product added"
            print(msg)
            upload_file_path=os.path.join(app.root_path,"static","images",f.filename)
            f.save(upload_file_path)
        except Exception as e:
            con.rollback()
            msg="Error in adding record"
            print(msg, str(e))
        finally:
            return redirect(url_for("root"))
    else:
        return render_template("product_frm.html",result = None)

if __name__ == "__main__":
    app.run(debug=True)
