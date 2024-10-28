from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import SocketIO, emit, join_room
from datetime import datetime
import pytz  
from env_variable import username, password

app = Flask(__name__)
socketio = SocketIO(app)  # Initializing the SocketIO

connection_string = f"mongodb+srv://{username}:{password}@connection.4x5l5.mongodb.net/?retryWrites=true&w=majority&appName=connection"

client = MongoClient(connection_string)
db = client.talent_db  # Accessing the 'talent_db' database

# Using flask_SocketIO to make messages appear instantly as they are sent    
# Send a Message (Real-Time)
@socketio.on('handle/send/message', namespace='/socket.io')
def handle_send_message(data):
    message = {
        "sender": data['sender'],
        "receiver": data['receiver'],
        "message": data['message'],
        "timestamp": datetime.utcnow(),
        "attachments": data.get("attachments")
    }
    
    db.messages.insert_one(message)  # Store message in database

    # Emit the message to the recipient's room for real-time delivery
    room = data['receiver']
    emit('receive_message', message, room=room)


# Join a Chat Room (Real-Time)
@socketio.on('on/join')
def on_join(data):
    username = data['username']
    join_room(username)  # Users join a room with their username as the room ID
    emit('status', {'message': f'{username} has entered the chat'}, room=username)


@app.route('/api/get/messages', methods=['GET'])
def get_messages():
    sender = request.args.get('sender')
    receiver = request.args.get('receiver')

    try:
        # Fetch messages where the sender is either the sender or receiver, and vice versa
        messages = list(db.messages.find({
            "$or": [
                {"sender": sender, "receiver": receiver},
                {"sender": receiver, "receiver": sender}
            ]
        }).sort("timestamp", 1))  

        # Defining the South Africa timezone
        south_africa_tz = pytz.timezone('Africa/Johannesburg')

        chat_history = [
            {
                "message": m['message'],
                "timestamp": m['timestamp'].astimezone(south_africa_tz).strftime("%Y-%m-%d %H:%M:%S %Z"),  # Converting to South Africa time
                "from": m['sender'],  # Sender of the message
                "to": m['receiver']  # Receiver of the message
            } 
            for m in messages
        ]

        return jsonify(chat_history), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    socketio.run(app, debug=True)  