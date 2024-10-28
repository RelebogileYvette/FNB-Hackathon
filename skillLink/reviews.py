from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import SocketIO, emit, join_room
from datetime import datetime
from env_variable import username, password

app = Flask(__name__)
socketio = SocketIO(app)

# MongoDB connection setup
connection_string= f"mongodb+srv://{username}:{password}@connection.4x5l5.mongodb.net/?retryWrites=true&w=majority&appName=connection"
client = MongoClient(connection_string)
db = client.talent_db  

# Post a Review
@app.route('/api/post/review', methods=['POST'])
def post_review():
    data = request.get_json()
    review = {
        "freelancer_id": data['freelancer_id'],
        "client_id": data['client_id'],
        "rating": data['rating'],
        "review": data['review']
    }
    
    db.reviews.insert_one(review)
    return jsonify({"message": "Review posted successfully"}), 201

# Get Freelancer Reviews
@app.route('/api/freelancer/reviews/<freelancer_id>', methods=['GET'])
def get_freelancer_reviews(freelancer_id):
    reviews = db.reviews.find({"freelancer_id": freelancer_id})
    results = [{"rating": r['rating'], "review": r['review']} for r in reviews]
    return jsonify(results), 200


if __name__ == '__main__':
    app.run(debug=True)
