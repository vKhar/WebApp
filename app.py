from flask import Flask,render_template,json
import os

app = Flask("__name__")
json_file_path=os.path.join(app.root_path,"static",'data.json')
product_list = json.load(open(json_file_path))

@app.route("/")
def root():
    return render_template("products.html",data=product_list)

if __name__ == "__main__":
    app.run(debug=True)