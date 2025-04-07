import os

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a_default_secret_key') # Should be overridden
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///../instance/users.db') # Use instance folder
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Define the fixed UUID here for easier access if needed elsewhere
    DUMMY_USER_ID = "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:' # Use in-memory DB for tests

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    # Make sure SECRET_KEY and DATABASE_URL are set via environment variables

# Map config names to classes
config_by_name = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig,
    default=DevelopmentConfig
)
