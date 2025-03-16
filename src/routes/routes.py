"""
Contains the API routes for Hole Heap
"""


from functools import wraps
from flask import Blueprint, abort, g, json, jsonify, make_response, request, session
from marshmallow import Schema, ValidationError
from event.config import send_message_to_bus
from event.schemas import MessageTypes
from routes.schemas import PotholeFixStatusRequest, PotholeRealStatusRequest, ProcessLocationChangeRequest, RegisterPotholeRequest, SaveUserSettingsRequest
from firebase_admin import auth

app_routes = Blueprint('main_routes', __name__)

def firebase_jwt_required(fn):
    """
    A custom jwt decoder to complement the firebase authentication in the form of a decorator method

    Decodes and verifies a token from Firebase

    Args:
        fn: The function to be wrapped

    Returns:
        The wrapped fn
    """
    @wraps(fn)
    def decorated(*args, **kwargs):
        """
        Decodes a firebase auth token and verifies it

        Args: None

        Returns: None

        Raises:
            401, 403
        """
        try:
            header_value =request.headers.get('Authorization')

            if header_value == None or not header_value.startswith('Bearer '):
                abort(401)

            token_parts = header_value.split(' ')

            print(token_parts)

            if(len(token_parts)!=2):
                abort(401, 'malformed header')

            submitted_jwt = token_parts[-1]

            decoded_token = auth.verify_id_token(submitted_jwt, check_revoked=True)
            
            g.uid = decoded_token['uid']
            return fn(*args, **kwargs)
        except auth.RevokedIdTokenError:
            # Token revoked, inform the user to reauthenticate or signOut().
            abort(401)
        except auth.UserDisabledError:
            # Token belongs to a disabled user record.
            abort(403)
        except auth.InvalidIdTokenError:
            # Token is invalid
            abort(401)
    return decorated

@app_routes.route('/location', methods=['POST'])
@firebase_jwt_required
def location():
    """
    Accepts updates for the user location from the client
    which is then published to the message bus

    Body: ProcessLocationChangeRequest

    Returns:
        202 - None
        400 - errors: dict
        500 - err: Exception
    """
    validated_request = _deserialize_and_validate_request(ProcessLocationChangeRequest())
    previous_location = json.loads(session['last_location'])
    validated_request['previous_latitude'] = previous_location['latitude']
    validated_request['previous_longitude'] = previous_location['longitude']
    session['last_location'] = json.dumps({'latitude': validated_request['latitude'], 'longitude': validated_request['longitude']})
    validated_request['user_id'] = g.uid
    send_message_to_bus(validated_request, MessageTypes.NEW_USER_LOCATION)

    return jsonify(data=[]),202

@app_routes.route('/pothole', methods=['POST'])
@firebase_jwt_required
def register_new_pothole():
    """
    Allows a new pothole to be added to the app
    
    Body: RegisterPotholeRequest

    Returns:
        202 - None
        400 - errors: dict
        500 - err: Exception
    """    
    validated_request = _deserialize_and_validate_request(RegisterPotholeRequest())
    validated_request['user_id'] = g.uid
    send_message_to_bus(validated_request, MessageTypes.REGISTER_POTHOLE)

    return jsonify(data=[]),202

@app_routes.route('/pothole/exists', methods=['POST'])
@firebase_jwt_required
def confirm_whether_a_pothole_exists():
    """
    Allows users to upvote and downvote whether a pothole listed in the app exists.

    Body: PotholeRealStatus

    Returns:
        202 - None
        400 - errors: dict
        500 - err: Exception
    """
    validated_request = _deserialize_and_validate_request(PotholeRealStatusRequest())
    is_real = validated_request[PotholeRealStatusRequest.is_real.name]
    validated_request['user_id'] = g.uid
    send_message_to_bus(validated_request, MessageTypes.POTHOLE_EXISTS if is_real else MessageTypes.POTHOLE_NOT_REAL)

    return jsonify(data=[]),202

@app_routes.route('/pothole/fixed', methods=['POST'])
@firebase_jwt_required
def confirm_whether_a_pothole_was_fixed():
    """
    Allows users to upvote or downvote whether a pothole was fixed

    Body: PotholeFixStatusRequest

    Returns:
        202 - None
        400 - errors: dict
        500 - err: Exception
    """
    validated_request = _deserialize_and_validate_request(PotholeFixStatusRequest())
    is_fixed = validated_request[PotholeFixStatusRequest.is_fixed.name]
    validated_request['user_id'] = g.uid
    send_message_to_bus(validated_request, MessageTypes.POTHOLE_FIXED if is_fixed else MessageTypes.POTHOLE_NOT_FIXED)

    return jsonify(data=[]),202

@app_routes.route('/user_settings', methods=['POST'])
@firebase_jwt_required
def save_user_settings():
    """
    Allows users to save their settings in the database

    Body: SaveUserSettingsRequest

    Returns:
        202 - None
        400 - errors: dict
        500 - err: Exception
    """
    validated_request = _deserialize_and_validate_request(SaveUserSettingsRequest())
    validated_request['user_id'] = g.uid
    send_message_to_bus(validated_request, MessageTypes.SAVE_USER_SETTINGS)

    return jsonify(data=[]),202


def _deserialize_and_validate_request(schema:Schema):
    """
    Helper method to execute deserialzation and validation common to all endpoints

    Args:
        schema: Schema
            The marshmallow schema validator for the request

    Returns: dict
        The validated request as a dict
    """
    try:
        body = request.get_json()
        validated_request = schema.load(body)
        validated_request['user_id'] = g.uid
        return validated_request
    except ValidationError as validationErr:
        abort(make_response(jsonify(validationErr.messages), 400))