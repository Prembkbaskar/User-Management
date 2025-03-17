from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from flask_cors import CORS
from datetime import datetime, timedelta
import os

app = Flask(__name__)
CORS(app)

# Configurations
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("MYSQL_URI", "mysql+pymysql://root:Root#04@localhost/user_management")
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/api_logs")

db = SQLAlchemy(app)
mongo = PyMongo(app)

# User Model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

# Create tables
with app.app_context():
    db.create_all()

# Add a user
# @app.route('/users', methods=['POST'])
# def add_user():
#     data = request.json
#     user = User(name=data['name'], email=data['email'])
#     db.session.add(user)
#     db.session.commit()

#     # Log request in MongoDB
#     mongo.db.logs.insert_one({
#         "endpoint": "/users",
#         "method": "POST",
#         "data": data,
#         # "timestamp": datetime.utcnow().isoformat()
#         "timestamp": (datetime.utcnow() + timedelta(hours=5, minutes=30)).isoformat()

#     })

#     return jsonify({"message": "User added"}), 201


@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    try:
        # Check if user already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({"error": "Email already exists"}), 400

        # Create new user
        user = User(name=data['name'], email=data['email'])
        db.session.add(user)
        db.session.commit()

        # Log request in MongoDB
        mongo.db.logs.insert_one({
            "endpoint": "/users",
            "method": "POST",
            "data": data,
            "timestamp": (datetime.utcnow() + timedelta(hours=5, minutes=30)).isoformat()
        })

        return jsonify({"message": "User added"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500  # Return error message


# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [{"id": u.id, "name": u.name, "email": u.email} for u in users]   

    # Log request in MongoDB
    man = mongo.db.logs.insert_one({
        "endpoint": "/users",
        "method": "GET",
        # "timestamp": datetime.now
        "timestamp": (datetime.utcnow() + timedelta(hours=5, minutes=30)).isoformat()

    })
    return jsonify(users_list)

if __name__ == "__main__":
    app.run(debug=True)
