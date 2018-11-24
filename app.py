from flask import Flask,render_template,json,request,jsonify
import os
import copy

app = Flask("__name__")
json_file_path=os.path.join(app.root_path,"static",'data.json')
product_list = json.load(open(json_file_path))

@app.route("/")
def root():
    return render_template("products.html",data=product_list)

@app.route('/add',methods = ['POST', 'GET'])
def add_product():
    global product_list
    if request.method == 'POST':
        f=request.files["image"]
        result={"name":request.form["name"],
                "description":request.form["description"],
                "price":float(request.form["price"]),
                "image":"images/"+f.filename
               }
        upload_file_path=os.path.join(app.root_path,"static","images",f.filename)
        f.save(upload_file_path)
        product_list.append(result) 
        #return (jsonify(result))
        return render_template("products.html",data=product_list)
    else:
        return render_template("product_frm.html",result = None)

if __name__ == "__main__":
    app.run(debug=True)
