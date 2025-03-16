from functools import wraps
from flask import abort, g, jsonify, request
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from marshmallow import Schema, ValidationError
from app import app
from event.config import send_message_to_bus
from event.schemas import MessageTypes
from routes.schemas import PotholeFixStatusRequest, PotholeRealStatusRequest, ProcessLocationChangeRequest, RegisterPotholeRequest
from firebase_admin import auth

def firebase_jwt_required():
    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            try:
                verify_jwt_in_request()
                submitted_jwt = get_jwt()
                print(submitted_jwt)

                decoded_token = auth.verify_id_token(submitted_jwt, check_revoked=True)
                
                g.uid = decoded_token['uid']
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
    return wrapper

@app.route('/location', methods=['POST'])
@firebase_jwt_required
def location():
    try:
        validated_request = _deserialize_and_validate_request(ProcessLocationChangeRequest())
        send_message_to_bus(validated_request, MessageTypes.NEW_USER_LOCATION)

        return 202
    except ValidationError as validationErr:
        return jsonify(validationErr.messages), 400
    except Exception as unknownErr:
        return jsonify(unknownErr), 500

@app.route('/pothole', methods=['POST'])
@firebase_jwt_required
def register_new_pothole():
    try:
        validated_request = _deserialize_and_validate_request(RegisterPotholeRequest())
        send_message_to_bus(validated_request, MessageTypes.REGISTER_POTHOLE)

        return 202
    except ValidationError as validationErr:
        return jsonify(validationErr.messages), 400
    except Exception as unknownErr:
        return jsonify(unknownErr), 500

@app.route('/pothole/exists', methods=['POST'])
@firebase_jwt_required
def confirm_whether_a_pothole_exists():
    try:
        validated_request = _deserialize_and_validate_request(PotholeRealStatusRequest())
        is_real = validated_request[PotholeRealStatusRequest.is_real.name]
        send_message_to_bus(validated_request, MessageTypes.POTHOLE_EXISTS if is_real else MessageTypes.POTHOLE_NOT_REAL)

        return 202
    except ValidationError as validationErr:
        return jsonify(validationErr.messages), 400
    except Exception as unknownErr:
        return jsonify(unknownErr), 500

@app.route('/pothole/fixed', methods=['POST'])
@firebase_jwt_required
def confirm_whether_a_pothole_was_fixed():
    try:
        validated_request = _deserialize_and_validate_request(PotholeFixStatusRequest())
        is_fixed = validated_request[PotholeFixStatusRequest.is_fixed.name]
        send_message_to_bus(validated_request, MessageTypes.POTHOLE_FIXED if is_fixed else MessageTypes.POTHOLE_NOT_FIXED)

        return 202
    except ValidationError as validationErr:
        return jsonify(validationErr.messages), 400
    except Exception as unknownErr:
        return jsonify(unknownErr), 500


def _deserialize_and_validate_request(schema:Schema):
    body = request.get_json()
    validated_request = schema.load(body)
    validated_request['user_id'] = g.uid
    return validated_request