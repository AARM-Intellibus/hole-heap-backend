from enum import Enum
from marshmallow import Schema, fields

class MessageTypes(Enum):
    REGISTER_POTHOLE = 'REGISTER_POTHOLE',
    POTHOLE_FIXED = 'POTHOLE_FIXED',
    POTHOLE_EXISTS = 'POTHOLE_EXISTS',
    POTHOLE_NOT_REAL = 'POTHOLE_NOT_REAL',
    POTHOLE_NOT_FIXED = 'POTHOLE_NOT_FIXED'
    WARN_USER_OF_POTHOLE = 'WARN_USER_OF_POTHOLE'
    NEW_USER_LOCATION = 'NEW_USER_LOCATION'

class PotholeDangerLevel(Enum):
    LEVEL_1 = 'LEVEL_1'
    LEVEL_2 = 'LEVEL_2'
    LEVEL_3 = 'LEVEL_3'
    LEVEL_4 = 'LEVEL_4'

class RegisterPotholeMessage(Schema):
    user_id = fields.Str(required=True)
    street_name = fields.Str(required=True)
    latitude = fields.Decimal(required=True)
    longitude = fields.Decimal(required=True)
    danger_level = fields.Enum(PotholeDangerLevel, by_value=True, required=True)
    image= fields.Str(required=True)

class PotholeFixedMessage(Schema):
    user_id = fields.Str(required=True)
    pothole_id= fields.UUID(required=True)

class PotholeExistsMessage(Schema):
    user_id = fields.Str(required=True)
    pothole_id= fields.UUID(required=True)

class PotholeNotFixedMessage(Schema):
    user_id = fields.Str(required=True)
    pothole_id= fields.UUID(required=True)

class PotholeNotRealMessage(Schema):
    user_id = fields.Str(required=True)
    pothole_id= fields.UUID(required=True)

class UserLocationChangeEvent(Schema):
    user_id=fields.Str(required=True)
    latitude=fields.Str(required=True)
    longitude=fields.Str(required=True)

class WarnUserOfPotholeMessage(Schema):
    user_id = fields.Str(required=True)
    latitude = fields.Decimal(required=True)
    longitude = fields.Decimal(required=True)
    danger_level = fields.Enum(PotholeDangerLevel, by_value=True, required=True)

