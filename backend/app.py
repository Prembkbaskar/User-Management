from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from flask_cors import CORS
from datetime import datetime, timedelta
import os
from config import Config

app = Flask(__name__)
CORS(app)

app.config.from_object(Config)

db = SQLAlchemy(app)
mongo = PyMongo(app)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

with app.app_context():
    db.create_all()

def get_ist_time():
    return (datetime.utcnow() + timedelta(hours=5, minutes=30)).isoformat()

@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    try:
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({"error": "Email already exists"}), 400

        user = User(name=data['name'], email=data['email'])
        db.session.add(user)
        db.session.commit()

        mongo.db.logs.insert_one({
            "full_url": request.url,  
            "method": request.method,  
            "client_ip": request.remote_addr,  
            "request_data": data,      
            "timestamp": get_ist_time()
        })

        return jsonify({"message": "User added"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500  

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [{"id": u.id, "name": u.name, "email": u.email} for u in users]   

    mongo.db.logs.insert_one({
            "full_url": request.url,  
            "method": request.method,  
            "client_ip": request.remote_addr,      
            "timestamp": get_ist_time()
        })
    return jsonify(users_list)

if __name__ == "__main__":
    app.run(debug=True)
