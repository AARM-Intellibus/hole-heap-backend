from config import db
from uuid import uuid4

class UserPotholeExist(db.Model):
    __tablename__ = "user_pothole_exist"
    id = db.Column(db.Uuid, primary_key=True, default=uuid4)
    user_id = db.Column(db.String(50), nullable=False)
    pothole_id = db.Column(db.ForeignKey('pothole.id'), nullable=False)
    does_exist = db.Column(db.Boolean, nullable=False )
    pothole = db.relationship('Pothole')
