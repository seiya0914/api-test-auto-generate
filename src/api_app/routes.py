import json
from datetime import datetime
from flask import Blueprint, jsonify, request
from .extensions import db
from .models import User

# Create a Blueprint
api_bp = Blueprint('api', __name__)

# --- API Endpoints ---
@api_bp.route('/ping', methods=['GET'])
def ping():
    """Simple ping endpoint."""
    return jsonify({"message": "pong"})

@api_bp.route('/users/<uuid_str>', methods=['GET'])
def get_user_profile(uuid_str):
    """Get user profile by userId."""
    user_id = str(uuid_str) # Ensure it's a string for lookup
    # Use get_or_404 for cleaner handling
    user = db.session.get(User, user_id)
    if user:
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({"code": "USER_NOT_FOUND", "message": "User not found"}), 404

@api_bp.route('/users/<uuid_str>', methods=['PATCH'])
def update_user_profile(uuid_str):
    """Update user profile by userId."""
    user_id = str(uuid_str) # Ensure it's a string for lookup
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"code": "USER_NOT_FOUND", "message": "User not found"}), 404

    update_data = request.get_json()
    if not update_data:
        return jsonify({"code": "BAD_REQUEST", "message": "Invalid JSON payload"}), 400

    # Update fields based on request body
    for key, value in update_data.items():
        if hasattr(user, key) and key not in ["userId", "createdAt"]: # Prevent updating readOnly fields
            if key in ["profile", "preferences", "tags"]:
                # Handle JSON fields carefully
                try:
                    current_data = json.loads(getattr(user, key) or ('{}' if key != 'tags' else '[]'))
                    if isinstance(current_data, dict) and isinstance(value, dict): # Merge dictionaries (profile, preferences)
                        current_data.update(value)
                        setattr(user, key, json.dumps(current_data))
                    elif isinstance(current_data, list) and isinstance(value, list): # Replace lists (tags)
                        setattr(user, key, json.dumps(value))
                    else: # Overwrite if types don't match standard update pattern
                         setattr(user, key, json.dumps(value))
                except (json.JSONDecodeError, TypeError):
                     # Fallback: just store the raw value as JSON string if complex update fails
                     setattr(user, key, json.dumps(value))
            elif key == 'lastLogin' and value is not None:
                 try: # Attempt to parse datetime string
                    # Handle potential timezone info (like Z for UTC)
                    dt_value = value.replace('Z', '+00:00')
                    setattr(user, key, datetime.fromisoformat(dt_value))
                 except (ValueError, TypeError):
                    pass # Ignore invalid date format
            else:
                setattr(user, key, value)

    try:
        db.session.commit()
        return jsonify(user.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        # Log the error properly in a real app
        print(f"Database error during update: {e}") # Basic logging
        return jsonify({"code": "DB_ERROR", "message": "Database error during update"}), 500
