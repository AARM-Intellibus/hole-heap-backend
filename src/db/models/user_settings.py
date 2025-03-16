from config import db
from datetime import datetime
from uuid import uuid4

class UserSetting(db.Model):
    __tablename__ = 'user_setting'
    id = db.Column(db.Uuid, primary_key=True, default=uuid4)
    user_id = db.Column(db.String(50), unique=True,)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    min_danger_level = db.Column(db.String(10), nullable=False)
    pref_distance_range = db.Column(db.Integer, nullable=False, default=10)
   