from app import db
from uuid import uuid4

class UserPotholeExist(db.Model):
    __tablename__ = "user_pothole_exist"
    id = db.Column(db.Uuid, primary_key=True, default=uuid4)
    uid = db.Column(db.String(50), nullable=False)
    pid = db.Column(db.ForeignKey('pothole.id'), nullable=False)
    doesExist = db.Column(db.Boolean, nullable=False )
    pothole = db.relationship('Pothole', back_populates='pothole')
