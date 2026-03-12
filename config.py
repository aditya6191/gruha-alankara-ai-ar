class Config:
    """Base configuration."""
    SECRET_KEY = 'your_super_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///gruha_alankara.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'uploads/'
