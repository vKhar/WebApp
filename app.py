from flask import Flask,render_template,json,request,jsonify
import os
import atexit

app = Flask("__name__")
#loads json file to memory
json_file_path=os.path.join(app.root_path,"static",'data.json')
product_list = json.load(open(json_file_path))

def save_json():
    with open(json_file_path,"w") as f:
        json.dump(product_list,f)
        
## dumps json to file on app termination
## atexit.register(save_json)

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
        save_json()
        return render_template("products.html",data=product_list)
    else:
        return render_template("product_frm.html",result = None)

if __name__ == "__main__":
    app.run(debug=True)
