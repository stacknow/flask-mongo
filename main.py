from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

# Configure MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/flask_mongo_db"
mongo = PyMongo(app)

# Route to get all users
@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    result = [{"_id": str(user["_id"]), "name": user["name"], "email": user["email"]} for user in users]
    return jsonify(result)

# Route to create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = {"name": data["name"], "email": data["email"]}
    user_id = mongo.db.users.insert_one(new_user).inserted_id
    return jsonify({"message": "User created", "user": {"_id": str(user_id), "name": data["name"], "email": data["email"]}}), 201

# Start the Flask server
if __name__ == '__main__':
    app.run(port=5000, debug=True)
