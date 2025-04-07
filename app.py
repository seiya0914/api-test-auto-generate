import uuid
import json
from datetime import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy import Text 
import click

app = Flask(__name__)
# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)

# --- Database Model ---
class User(db.Model):
    userId = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    lastLogin = db.Column(db.DateTime, nullable=True)
    isActive = db.Column(db.Boolean, default=True, nullable=False)
    profile = db.Column(Text, nullable=True, default='{}') 
    tags = db.Column(Text, nullable=True, default='[]') 
    preferences = db.Column(Text, nullable=True, default='{}') 

    def to_dict(self):
        return {
            "userId": self.userId,
            "username": self.username,
            "email": self.email,
            "createdAt": self.createdAt.isoformat() + "Z" if self.createdAt else None,
            "lastLogin": self.lastLogin.isoformat() + "Z" if self.lastLogin else None,
            "isActive": self.isActive,
            "profile": json.loads(self.profile) if self.profile else {},
            "tags": json.loads(self.tags) if self.tags else [],
            "preferences": json.loads(self.preferences) if self.preferences else {}
        }

# --- Helper to initialize DB ---
@app.cli.command("init-db")
@click.option('--seed', is_flag=True, help='Seed the database with a sample user.')
def init_db_command(seed):
    with app.app_context():
        db.create_all()
        print("Initialized the database.")
        if seed:
            existing_user = db.session.get(User, "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11")
            if not existing_user:
                dummy_user = User(
                    userId="a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
                    username="testuser",
                    email="test@example.com",
                    profile=json.dumps({
                        "fullName": "Test User",
                        "bio": "A sample user for testing.",
                        "avatarUrl": "https://example.com/avatar.png",
                        "birthDate": "1990-01-01",
                        "address": {
                            "street": "123 Main St",
                            "city": "Anytown",
                            "postalCode": "12345",
                            "country": "USA"
                        }
                    }),
                    tags=json.dumps(["tester", "sample"]),
                    preferences=json.dumps({
                        "theme": "light",
                        "notifications": True
                    })
                )
                db.session.add(dummy_user)
                db.session.commit()
                print(f"Seeded database with user: a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11")
            else:
                print(f"User a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11 already exists, skipping seed.")

# Use a consistent dummy ID for seeding and testing if needed
DUMMY_USER_ID = "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11" 

# --- API Endpoints ---
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message": "pong"})

@app.route('/users/<uuid_str>', methods=['GET'])
def get_user_profile(uuid_str):
    user_id = str(uuid_str) 
    user = db.session.get(User, user_id)
    if user:
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({"code": "USER_NOT_FOUND", "message": "User not found"}), 404

@app.route('/users/<uuid_str>', methods=['PATCH'])
def update_user_profile(uuid_str):
    user_id = str(uuid_str) 
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"code": "USER_NOT_FOUND", "message": "User not found"}), 404

    update_data = request.get_json()
    if not update_data:
        return jsonify({"code": "BAD_REQUEST", "message": "Invalid JSON payload"}), 400

    for key, value in update_data.items():
        if hasattr(user, key) and key not in ["userId", "createdAt"]: 
            if key in ["profile", "preferences", "tags"]:
                try:
                    current_data = json.loads(getattr(user, key) or ('{}' if key != 'tags' else '[]'))
                    if isinstance(current_data, dict) and isinstance(value, dict): 
                        current_data.update(value)
                        setattr(user, key, json.dumps(current_data))
                    elif isinstance(current_data, list) and isinstance(value, list): 
                        setattr(user, key, json.dumps(value))
                    else: 
                         setattr(user, key, json.dumps(value))
                except (json.JSONDecodeError, TypeError):
                     setattr(user, key, json.dumps(value))
            elif key == 'lastLogin' and value is not None:
                 try: 
                    setattr(user, key, datetime.fromisoformat(value.replace('Z', '+00:00')))
                 except (ValueError, TypeError):
                    pass 
            else:
                setattr(user, key, value)

    try:
        db.session.commit()
        return jsonify(user.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"code": "DB_ERROR", "message": "Database error during update"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
