import uuid
from datetime import datetime, timezone
from flask import Flask, jsonify, request

app = Flask(__name__)

# --- Dummy Data ---
# Consistent dummy data matching the OpenAPI schema structure
DUMMY_USER = {
    "userId": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11", # Fixed UUID for simplicity
    "username": "dummyuser",
    "email": "dummy@example.com",
    "createdAt": datetime.now(timezone.utc).isoformat(), # Use ISO format
    "lastLogin": datetime.now(timezone.utc).isoformat(),
    "isActive": True,
    "profile": {
        "fullName": "Dummy User",
        "bio": "This is a dummy bio.",
        "avatarUrl": "http://example.com/avatar.jpg"
    },
    "tags": ["dummy", "test"],
    "preferences": {
        "theme": "dark",
        "notifications": {
            "email": True,
            "sms": False
        }
    }
}

# --- API Endpoints ---

@app.route('/users/<uuid:userId>', methods=['GET'])
def get_user_profile(userId):
    """Get user profile by userId (returns dummy data)."""
    # Ignore the input userId, always return the same dummy user
    print(f"GET /users/{userId} called")
    # Ensure returned data structure matches schema
    response_data = DUMMY_USER.copy()
    response_data["userId"] = str(userId) # Reflect the requested userId if needed, or keep fixed
    response_data["createdAt"] = datetime.now(timezone.utc).isoformat() # Update timestamp
    response_data["lastLogin"] = datetime.now(timezone.utc).isoformat()
    return jsonify(response_data), 200

@app.route('/users/<uuid:userId>', methods=['PATCH'])
def update_user_profile(userId):
    """Update user profile by userId (simulated)."""
    print(f"PATCH /users/{userId} called")
    if not request.is_json:
        return jsonify({"code": "INVALID_REQUEST", "message": "Request must be JSON"}), 400

    data = request.get_json()

    # Simulate update: return a modified version of the dummy data
    # We don't actually store anything
    updated_data = DUMMY_USER.copy()
    updated_data["userId"] = str(userId) # Reflect requested userId

    # Very basic simulation of applying changes from request body
    if 'profile' in data and isinstance(data['profile'], dict):
        updated_data['profile'].update(data['profile'])
    if 'tags' in data and isinstance(data['tags'], list):
        updated_data['tags'] = data['tags']
    if 'isActive' in data and isinstance(data['isActive'], bool):
        updated_data['isActive'] = data['isActive']
    if 'preferences' in data and isinstance(data['preferences'], dict):
        # Simple merge, not deep merge
        updated_data['preferences'].update(data['preferences'])

    updated_data["lastLogin"] = datetime.now(timezone.utc).isoformat() # Update timestamp

    # Note: Read-only fields like createdAt are not updated from request

    return jsonify(updated_data), 200

# --- Error Handlers (Optional but good practice) ---
@app.errorhandler(404)
def not_found(error):
    # Handle cases where routes don't match (e.g., /)
    return jsonify({"code": "NOT_FOUND", "message": "Resource not found"}), 404

@app.errorhandler(400)
def bad_request(error):
    # Catch other potential bad requests (like non-UUID userId)
    return jsonify({"code": "BAD_REQUEST", "message": str(error)}), 400

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"code": "METHOD_NOT_ALLOWED", "message": "Method not allowed for this resource"}), 405


if __name__ == '__main__':
    # Run directly with Python, enable debug for auto-reload
    app.run(host='0.0.0.0', port=8000, debug=True)
