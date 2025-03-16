from config import ma
from db.models.user_settings import UserSetting
from db.models.user_pothole_fixed import UserPotholeFixed
from db.models.user_pothole_exist import UserPotholeExist
from db.models.pothole import Pothole
from marshmallow import fields

class UserSettingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserSetting
        load_instance = True
        include_relationships = True

class PotholeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pothole
        load_instance = True
        include_relationships = True

class UserPotholeFixedSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserPotholeFixed
        load_instance = True
        include_relationships = True

class UserPotholeExistSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserPotholeExist
        load_instance = True
        include_relationships = True