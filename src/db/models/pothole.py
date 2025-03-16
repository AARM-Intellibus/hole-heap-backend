from config import db    
from datetime import datetime
from uuid import uuid4
from .user_pothole_fixed import UserPotholeFixed
from sqlalchemy.ext.hybrid import hybrid_property

class Pothole(db.Model):
    __tablename__ = 'pothole'
    id = db.Column(db.Uuid, primary_key=True, default=uuid4)
    created_by_uid = db.Column(db.String(50),nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    danger_level = db.Column(db.String(10), nullable=False)
    street_name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String, nullable=False)

    @hybrid_property
    def fixed_upvotes(self):
        count = UserPotholeFixed.query.filter(pid = self.id, is_fixed = True).count()
        if count is None:
            return 0
        return count

    @hybrid_property
    def fixed_downvotes(self):
        count = UserPotholeFixed.query.filter(pid = self.id, is_fixed = False).count()
        if count is None:
            return 0
        return count
    
    @hybrid_property
    def exists_upvotes(self):
        count = UserPotholeFixed.query.filter(pid = self.id, does_exist = True).count()
        if count is None: 
            return 0
        return count

    @hybrid_property
    def exists_downvotes(self):
        count = UserPotholeFixed.query.filter(pid = self.id, does_exist = False).count()
        if count is None: 
            return 0
        return count
