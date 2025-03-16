from app import db
from datetime import datetime
from uuid import uuid4
from .user_pothole_fixed import UserPotholeFixed

class Pothole(db.Model):
    __tablename__ = 'pothole'
    id = db.Column(db.Uuid, primary_key=True, default=uuid4)
    created_by_uid = db.Column(db.String(50),nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    danger_level = db.Column(db.String(10), nullable=False)
    street_name = db.Column(db.String(100), nullable=False)

    @property
    def upvotes(self):
        count = UserPotholeFixed.query.filter(pid = self.id, isFixed = True).count()
        if count is None:
            return 0
        return count
    
    @property
    def downvotes(self):
        count = UserPotholeFixed.query.filter(pid = self.id, isFalse = False).count()
        if count is None: 
            return 0
        return count
