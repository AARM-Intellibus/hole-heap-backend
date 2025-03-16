import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from dotenv import load_dotenv

#Firebase Imports
import firebase_admin
from firebase_admin import credentials, firestore

load_dotenv()

app = Flask(__name__)
jwt = JWTManager(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

FIREBASE_CONFIG = os.environ.get('FIREBASE_CONFIGS')
creds = credentials.Certificate(FIREBASE_CONFIG)
firebase_admin.initialize_app(creds)
firestore_db = firestore.client()

from db.models.user_settings import UserSetting
from db.models.pothole import Pothole
from db.models.user_pothole_fixed import UserPotholeFixed
from db.models.user_pothole_exist import UserPotholeExist