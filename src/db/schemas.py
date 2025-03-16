from src.app import ma
from models.user_settings import UserSetting
from models.user_pothole_fixed import UserPotholeFixed
from models.user_pothole_exist import UserPotholeExist
from models.pothole import Pothole

class UserSettingSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserSetting
    
    uid = ma.auto_field()
    min_danger_level = ma.auto_field()

class UserPotholeFixedSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserPotholeFixed
    
    uid = ma.auto_field()
    pid =  ma.auto_field()
    is_fixed =  ma.auto_field()

class UserPotholeExistSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserPotholeExist
    
    uid = ma.auto_field()
    pid =  ma.auto_field()
    does_exist =  ma.auto_field()

class PotholeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Pothole
    created_by_uid = ma.auto_field()
    latitude = ma.auto_field()
    longitude = ma.auto_field()
    date_created = ma.auto_field()
    danger_level = ma.auto_field()
    street_name = ma.auto_field()