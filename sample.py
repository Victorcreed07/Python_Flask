from flask import Flask, render_template,request,redirect
from flask_pymongo import pymongo
from flask import jsonify, request
from bson.objectid import ObjectId


app = Flask(__name__)

con_string = "mongodb+srv://victor:creed@nodeexpress.jq3xj.mongodb.net/?retryWrites=true&w=majority"


client = pymongo.MongoClient(con_string)

db = client.get_database('python-to-do')

user_collection = pymongo.collection.Collection(db, 'python-prod')
print("MongoDB connected Successfully")
# @app.route("/")
# def whatup():
#   return render_template("index.html")


@app.route('/', methods=['POST', 'GET'])
def index():
    if (request.method == 'POST'):
        resp = {}
        try:
            content = request.form['content']
            degree = request.form['degree']
            user_collection.insert_one({'content': content, 'degree': degree})
            print("User Data Stored Successfully in the Database.")
            status = {
                "statusCode": "200",
                "statusMessage": "User Data Stored Successfully in the Database."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode": "400",
                "statusMessage": str(e)
            }
        resp["status"] = status
        return redirect("/")

    else:
        users = user_collection.find({})
       
        users = list(users)
        status = {
            "statusCode": "200",
            "statusMessage": "User Data Retrieved Successfully from the Database."
        }
        output = [{'Id':str(user['_id']),'Task': user['content'], 'Degree': user['degree']}
                  for user in users]  # list comprehension
       
        return render_template("index.html",output = output)



@app.route('/delete/<id>')
def delete(id):

    try:
        print(id)
        user_collection.delete_one({"_id":ObjectId(id)})
    except Exception as e:
        print(e)
        return "Problrm here"
    return redirect("/")




@app.route('/update/<id>' , methods=['POST', 'GET'])
def update(id):
    users = user_collection.find({})
    users = list(users)
    output = [{'Id':str(user['_id']),'Task': user['content'], 'Degree': user['degree']}
              for user in users] 

   
    for i in output:
        if(i['Id'] == id):
            val = i
    
    print(val)
    if(request.method == "POST"):
        try:
            update = request.form['update']
            user_collection.update_one({"_id":ObjectId(id)}, {"$set": {"content":update}})
            return redirect("/")
        except Exception as e:
            print(e)
            return "Problrm here"
    else:
        return render_template("update.html",val=val)
# @app.route('/read', methods=['GET'])
# def read_users():
#     resp = {}
#     try:
#         users = user_collection.find({})
#         print(users)
#         users = list(users)
#         status = {
#             "statusCode":"200",
#             "statusMessage":"User Data Retrieved Successfully from the Database."
#         }
#         output = [{'Task' : user['content'], 'Degree' : user['degree']} for user in users]   #list comprehension
#         resp['data'] = output
#     except Exception as e:
#         print(e)
#         status = {
#             "statusCode":"400",
#             "statusMessage":str(e)
#         }
#     resp["status"] =status
#     return resp


if __name__ == "__main__":
    app.run(debug=True)
