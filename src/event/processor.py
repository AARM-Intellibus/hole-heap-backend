"""
Contains the methods to process messages from the bus
"""

from typing import Any, Callable
from marshmallow import Schema
from db.models.pothole import Pothole
from db.models.user_pothole_exist import UserPotholeExist
from db.schemas import PotholeSchema, UserPotholeExistSchema
from event.schemas import PotholeExistsMessage, RegisterPotholeMessage, UserLocationChangeEvent

from config import firestore_db, db

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
    message = validator.load(message_body) # will throw exception if message is malformed
    # deserialize message into db model
    model = model_serializer.load(message_body, load_instance=True)

    return message, model

def _save_model_trigger_pothole_updates(validator:Schema, model_serializer:Schema, message_body:str, adjust_model_pre_save: Callable[[Any, dict], None]):
    db_model, register_pothole_cmd = _validate_message_load_body(validator,model_serializer, message_body)

    # map fields
    adjust_model_pre_save(db_model,register_pothole_cmd)

    # save updates to db
    db.session.add(db_model)
    db.session.commit()

    # push updates to firebase so that the client pothole feeds can be updated
    _post_pothole_update(db_model.id, db_model)

def process_register_pothole(message):
    def mutate_model(model,msg):
        model.created_by_uid = msg['user_id']
    
    try:
        _save_model_trigger_pothole_updates(RegisterPotholeMessage(), PotholeSchema(), message,  mutate_model)
    except Exception as e:
        print(e)

def process_pothole_exists(message):
    _toggle_pothole_exists(message, True)

def _toggle_pothole_exists(message:str, pothole_exists: bool):
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
    try:
        user_location_changed = UserLocationChangeEvent().load(message)
        # determine whether to warn users
    except Exception as e:
        print(e)


def _post_pothole_update(pothole_id:str,data:dict ):
    firestore_db.collection('pothole_feed').document(pothole_id).set(data)