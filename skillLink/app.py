from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from env_variable import username, password

app = Flask(__name__)
connection_string = f"mongodb+srv://{username}:{password}@cluster0.ir9o1.mongodb.net/talent_db?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(connection_string)
db = client.talent_db  # Access the 'talent_db' database

# Method to initialize collections and create default documents
def initialize_db():
    # Create collections if they don't exist
    if 'talents' not in db.list_collection_names():
        db.create_collection('talents')
    if 'talent_seekers' not in db.list_collection_names():
        db.create_collection('talent_seekers')
    if 'jobs' not in db.list_collection_names():
        db.create_collection('jobs')

    # Optionally, you can create some default documents here
    # Example: Check if any talents exist and insert a default talent
    if db.talents.count_documents({}) == 0:
        default_talent = {
            "name": "Default",
            "surname": "Talent",
            "id_number": "123456789",
            "cell_number": "0123456789",
            "email": "default.talent@example.com",
            "address": "123 Default Street",
            "password": generate_password_hash("default_password", method='pbkdf2:sha256'),
        }
        db.talents.insert_one(default_talent)

# Initialize the database
initialize_db()

# -------------------------------
# 1. Talent Signup Endpoint
# -------------------------------
@app.route('/api/talent/signup', methods=['POST'])
def talent_signup():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

    talent = {
        "name": data['name'],
        "surname": data['surname'],
        "id_number": data['id_number'],
        "cell_number": data['cell_number'],
        "email": data['email'],
        "address": data['address'],
        "password": hashed_password,
    }

    db.talents.insert_one(talent)
    return jsonify({"message": "Talent registered successfully"}), 201

# -------------------------------
# 2. Talent Login Endpoint
# -------------------------------
@app.route('/api/talent/login', methods=['POST'])
def talent_login():
    data = request.get_json()

    # Check if the required fields are present
    if 'email' not in data or 'password' not in data:
        return jsonify({"error": "Email and password are required"}), 400

    talent = db.talents.find_one({"email": data['email']})
    
    if talent and check_password_hash(talent['password'], data['password']):
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"error": "Invalid credentials"}), 401


# -------------------------------
# 3. Talent Profile Update Endpoint
# -------------------------------
@app.route('/api/talent/profile', methods=['PUT'])
def talent_profile_update():
    data = request.get_json()
    db.talents.update_one(
        {"email": data['email']},
        {"$set": {
            "status": data.get('status'),
            "files": data.get('files'),
            "education": data.get('education'),
            "skills": data.get('skills')
        }}
    )
    return jsonify({"message": "Profile updated successfully"}), 200

# -------------------------------
# 4. TalentSeeker Signup Endpoint
# -------------------------------
@app.route('/api/talentseeker/signup', methods=['POST'])
def talentseeker_signup():
    data = request.get_json()
    
    talent_seeker = {
        "name": data['name'],
        "surname": data['surname'],
        "id_number": data['id_number'],
        "cell_number": data['cell_number'],
        "email": data['email'],
        "address": data['address'],
        "biz_name": data['biz_name'],
        "biz_address": data['biz_address'],
        "biz_contact": data['biz_contact'],
        "password": generate_password_hash("default_password", method='pbkdf2:sha256'),
    }
    
    db.talent_seekers.insert_one(talent_seeker)
    return jsonify({"message": "Talent Seeker registered successfully"}), 201

# -------------------------------
# 5. TalentSeeker Job Posting Endpoint
# -------------------------------
@app.route('/api/talentseeker/job', methods=['POST'])
def talentseeker_job_post():
    data = request.get_json()
    job = {
        "title": data['title'],
        "description": data['description'],
        "skills_required": data['skills_required'],
        "posted_by": data['email']
    }
    
    db.jobs.insert_one(job)
    return jsonify({"message": "Job posted successfully"}), 201

if __name__ == '__main__':
    app.run(debug=True)

# -------------------------------
#  List Talent
# -------------------------------
@app.route('/api/talents', methods=['GET'])
def get_talents():
    talents = db.talents.find()
    talent_list = []

    for talent in talents:
        talent['_id'] = str(talent['_id'])  # Convert ObjectId to string
        talent_list.append(talent)

    return jsonify(talent_list), 200

# -------------------------------
#  List Talent by ID
# -------------------------------
@app.route('/api/talents/<id>', methods=['GET'])
def get_talent_by_id(id):
    talent = db.talents.find_one({"_id": ObjectId(id)})

    if talent:
        talent['_id'] = str(talent['_id'])  # Convert ObjectId to string
        return jsonify(talent), 200
    return jsonify({"error": "Talent not found"}), 404
# -------------------------------
#  Select talent seeker
# -------------------------------
@app.route('/api/talentseeker/select', methods=['POST'])
def select_talent():
    data = request.get_json()
    
    selected_talent = {
        "talent_id": data['talent_id'],  # ID of the selected talent
        "job_id": data['job_id'],         # ID of the job for which the talent is selected
        "selected_by": data['email'],     # Email of the talent seeker
        "reason": data.get('reason'),      # Reason for selection, if any
    }

    db.selected_talents.insert_one(selected_talent)
    return jsonify({"message": "Talent selected successfully"}), 201

