from marshmallow import Schema, fields

from event.schemas import PotholeDangerLevel

class PotholeFixStatusRequest(Schema):
    user_id = fields.Str(required=True)
    pothole_id=fields.UUID(required=True)
    is_fixed= fields.Bool(required=True)

class PotholeRealStatusRequest(Schema):
    user_id = fields.Str(required=True)
    pothole_id=fields.UUID(required=True)
    is_real= fields.Bool(required=True)

class RegisterPotholeRequest(Schema):
    user_id = fields.Str(required=True)
    image=fields.Str()
    latitude=fields.Decimal(required=True)
    longitude=fields.Decimal(required=True)
    danger_level=fields.Enum(PotholeDangerLevel, required=True, by_value=True)
    street_name= fields.Str(required=True)
    parish=fields.Str()

class ProcessLocationChangeRequest(Schema):
    user_id = fields.Str(required=True)
    latitude=fields.Decimal(required=True)
    longitude=fields.Decimal(required=True)

