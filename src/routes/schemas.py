"""
Contains the API request and response schemas for Hole Heap
"""

from marshmallow import Schema, fields

from event.schemas import PotholeDangerLevel

class PotholeFixStatusRequest(Schema):
    """
    Specifies the schema for requests to POST /pothole/fixed
    """

    user_id = fields.Str(required=True)
    """
    The firebase user ID for the user making the request
    """
    
    pothole_id=fields.UUID(required=True)
    """
    The pothole ID in the postgres db
    """
    
    is_fixed= fields.Bool(required=True)
    """
    The status the user choose for whether the pothole has been fixed
    """


class PotholeRealStatusRequest(Schema):
    """
    Specifies the schema for requests to POST /pothole/exists
    """

    user_id = fields.Str(required=True)
    """
    The firebase user ID for the user making the request
    """
    
    pothole_id=fields.UUID(required=True)
    """
    The pothole ID in the postgres db
    """

    is_real= fields.Bool(required=True)
    """
    The status the user chose for whether the pothole actually exists
    """


class RegisterPotholeRequest(Schema):
    """
    Specifies the schema for requests to POST /pothole
    """

    user_id = fields.Str(required=True)
    """
    The firebase user ID for the user making the request
    """

    image=fields.Str()
    """
    The Base64 encoded string of the picture taken of the pothole
    """

    latitude=fields.Decimal(required=True)
    """
    The latitude portion of the pothole location
    """

    longitude=fields.Decimal(required=True)
    """
    The longitude portion of the pothole location
    """

    danger_level=fields.Enum(PotholeDangerLevel, required=True, by_value=True)
    """
    The danger level as rated by the user
    """
    
    street_name= fields.Str(required=True)
    """
    The street the pothole is on. This is stored for quick access for reporting purposes 
    """

    parish=fields.Str()
    """
    The parish the pothole is located in. This is stored for quick access for reporting purposes
    """


class ProcessLocationChangeRequest(Schema):
    """
    Specifies the schema for requests sent to POST /location
    """
    
    user_id = fields.Str(required=True)
    """
    The firebase user ID for the user making the request
    """

    latitude=fields.Decimal(required=True)
    """
    The latitude portion of the user's current location
    """
    
    longitude=fields.Decimal(required=True)
    """
    The longitude portion of the user's current location
    """