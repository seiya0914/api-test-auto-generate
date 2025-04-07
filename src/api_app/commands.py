import click
import json
from flask.cli import with_appcontext
from .extensions import db
from .models import User
from .config import Config # Import Config to get DUMMY_USER_ID

@click.command("init-db")
@click.option('--seed', is_flag=True, help='Seed the database with a sample user.')
@with_appcontext # Ensures app context is available
def init_db_command(seed):
    """Initialize the database tables."""
    db.create_all()
    print("Initialized the database.")
    if seed:
        # Use the ID from config
        dummy_id = Config.DUMMY_USER_ID
        existing_user = db.session.get(User, dummy_id)
        if not existing_user:
            dummy_user = User(
                userId=dummy_id,
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
            print(f"Seeded database with user: {dummy_id}")
        else:
            print(f"User {dummy_id} already exists, skipping seed.")

def register_commands(app):
    """Register CLI commands with the Flask app."""
    app.cli.add_command(init_db_command)
