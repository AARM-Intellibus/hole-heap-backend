"""
Contains the methods to process messages from the bus
"""

from typing import Any, Callable
from marshmallow import Schema
from sqlalchemy import asc
from db.models.pothole import Pothole
from db.models.user_pothole_exist import UserPotholeExist
from db.models.user_settings import UserSetting
from db.schemas import PotholeSchema, UserPotholeExistSchema, UserSettingSchema
from event.direction import get_direction, get_surrounding_location_matrix
from event.schemas import PotholeExistsMessage, RegisterPotholeMessage, SaveUserSettingsMessage, UserLocationChangeEvent

from config import firestore_db, db, app

def _validate_message_load_body(validator:Schema, model_serializer:Schema, message_body:str):
    """
    Validates the message format and deserializes it into a database model

    Args:
        validator: Schema
            The validator for the bus message
        model_serializer: Schema
            The serializer for the database model
        message_body: str
            The text of the message body
    
    Returns:
        An tuple of the instance of the model, and the original message as a dict

    Raises:
        ValidationError: when schema validation fails
    """
    # validate the message body
    message = validator.loads(message_body) # will throw exception if message is malformed
    # deserialize message into db model
    model = model_serializer.loads(message_body)

    return message, model

def _save_model_trigger_pothole_updates(validator:Schema, model_serializer:Schema, message_body:str, adjust_model_pre_save: Callable[[Any, dict], None]):
    db_model, register_pothole_cmd = _validate_message_load_body(validator,model_serializer, message_body)

    # map fields
    adjust_model_pre_save(db_model,register_pothole_cmd)

    # save updates to db

    with app.app_context():
        db.session.add(db_model)
        db.session.commit()

    # push updates to firebase so that the client pothole feeds can be updated
    _post_pothole_update(db_model.id, db_model)

def process_register_pothole(message):
    def mutate_model(model,msg):
        pass
    
    try:
        _save_model_trigger_pothole_updates(RegisterPotholeMessage(), PotholeSchema(), message,  mutate_model)
    except Exception as e:
        print(e)

def process_pothole_exists(message):
    _toggle_pothole_exists(message, True)

def _toggle_pothole_exists(message:str, pothole_exists: bool):
    with app.app_context():
        try:
            db_model, _ = _validate_message_load_body(PotholeExistsMessage(),UserPotholeExistSchema(), message)

            db_model.does_exist = pothole_exists

            pothole:Pothole = Pothole.query.get(db_model.pothole_id)

            if(pothole):
                existing_upvote = UserPotholeExist.query.filter_by(uid = db_model.user_id, pid=db_model.pothole_id).first()

                # if they already upvoted this pothole, treat the command as a toggle to remove the upvote
                if existing_upvote:
                    db.session.delete(existing_upvote)
                else:
                    db.session.add(db_model)

                db.session.commit()
                db.session.refresh(pothole)

                _post_pothole_update(pothole.id, pothole)

        except Exception as e:
                print(e)

def process_pothole_fixed(message):
    _toggle_pothole_fixed(message, True)

def _toggle_pothole_fixed(message:str, is_fixed:bool):
    with app.app_context():
        try:
            db_model, _ = _validate_message_load_body(PotholeExistsMessage(),UserPotholeExistSchema(), message)

            db_model.is_fixed = is_fixed

            pothole:Pothole = Pothole.query.get(db_model.pothole_id)

            if(pothole):
                existing_upvote = UserPotholeExist.query.filter_by(uid = db_model.user_id, pid=db_model.pothole_id).first()

                # if they already upvoted this pothole, treat the command as a toggle to remove the upvote
                if existing_upvote:
                    db.session.delete(existing_upvote)
                else:
                    db.session.add(db_model)

                db.session.commit()
                db.session.refresh(pothole)

                _post_pothole_update(pothole.id, pothole)
        except Exception as e:
            print(e)

def process_pothole_not_real(message):
    _toggle_pothole_exists(message, False)

def process_pothole_not_fixed(message):
    _toggle_pothole_fixed(message, True)

def process_location_changed(message):
    with app.app_context():
        try:
            user_location_changed = UserLocationChangeEvent().loads(message)
            direction = get_direction(
                (user_location_changed['previous_latitude'], user_location_changed['previous_longitude']), 
                (user_location_changed['latitude'], user_location_changed['longitude']))
            
            matrix = get_surrounding_location_matrix(
                user_location_changed['latitude'],
                user_location_changed['longitude'],
                direction)

            potholes_nearby = []
            for [lat,lon] in matrix:
                pothole_nearby = Pothole.query.filter(Pothole.latitude>=lat, Pothole.longitude>=lon).order_by(
                    asc(
                        abs(Pothole.latitude-user_location_changed['latitude'])+abs(Pothole.longitude-user_location_changed['longitude']))).first()
                if(pothole_nearby):
                    potholes_nearby.append(pothole_nearby)


            if(potholes_nearby):
                nearest_pothole = pothole_nearby[0]
                nearest_distance = abs(nearest_pothole.latitude-user_location_changed['latitude'])+abs(nearest_pothole.longitude-user_location_changed['longitude'])
                for pothole in potholes_nearby:
                    next_distance = abs(pothole.latitude-user_location_changed['latitude'])+abs(pothole.longitude-user_location_changed['longitude'])
                    if(next_distance < nearest_distance):
                        nearest_distance = next_distance
                        nearest_pothole = pothole
            
                firestore_db.collection('warnings').document(user_location_changed['user_id']).set(pothole)

        except Exception as e:
            print(e)

def process_save_user_settigs(message):    
    try:
        _save_model_trigger_user_settings(SaveUserSettingsMessage(), UserSettingSchema(), message)
    except Exception as e:
        print(e)

def _save_model_trigger_user_settings(validator:Schema, model_serializer:Schema, message_body:str, adjust_model_pre_save: Callable[[Any, dict], None]):
    try:
        db_model, save_user_setting_cmd = _validate_message_load_body(validator,model_serializer, message_body)

        # map fields
        adjust_model_pre_save(db_model, save_user_setting_cmd)

        # save updates to db
        db.session.add(db_model)
        db.session.commit()

        user_setting:UserSetting = UserSetting.query.get(db_model.user_id)

        if(not user_setting):
            # save updates to db
            db.session.add(db_model)
            db.session.commit()
    except Exception as e:
        print(e)

def _post_pothole_update(pothole_id:str,data:dict ):
    firestore_db.collection('pothole_feed').document(pothole_id).set(data)