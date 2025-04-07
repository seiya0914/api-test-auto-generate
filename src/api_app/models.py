import uuid
import json
from datetime import datetime
from sqlalchemy import Text
from .extensions import db # Import db from extensions

# --- Database Model ---
class User(db.Model):
    # Using Text for UUID for broader compatibility, could use String or specific UUID type
    userId = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    lastLogin = db.Column(db.DateTime, nullable=True)
    isActive = db.Column(db.Boolean, default=True, nullable=False)
    # Store complex types as JSON strings in SQLite
    profile = db.Column(Text, nullable=True, default='{}') # Store ProfileDetails as JSON string
    tags = db.Column(Text, nullable=True, default='[]') # Store tags array as JSON string
    preferences = db.Column(Text, nullable=True, default='{}') # Store preferences as JSON string

    def to_dict(self):
        """Converts the User model instance to a dictionary matching the OpenAPI schema."""
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
