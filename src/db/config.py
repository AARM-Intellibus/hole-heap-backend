import os

FIREBASE_CONFIG = os.environ.get('FIREBASE_CONFIGS')
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://username:password@localhost/mydatabase'
SQLALCHEMY_TRACK_MODIFICATIONS = False