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

from config.environ import SECRET_KEY, SQLALCHEMY_DATABASE_URI

app = Flask(__name__)
app.secret_key = SECRET_KEY
jwt = JWTManager(app)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
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


from routes.routes import app_routes

app.register_blueprint(app_routes)
