"""
Contains the setup for the message bus integration
"""

import atexit
import os
import sys
from typing import Any
import uuid
from flask import json
import pika
from pika import BasicProperties
from pika.channel import Channel
from pika.spec import Basic

from config.environ import ENVIRON_QUEUE_NAME, MESSAGE_BROKER_URL
from event.processor import process_location_changed, process_pothole_exists, process_pothole_fixed, process_pothole_not_fixed, process_pothole_not_real, process_register_pothole
from event.schemas import MessageTypes

params = pika.URLParameters(MESSAGE_BROKER_URL)
connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue=ENVIRON_QUEUE_NAME, durable=True)

def send_message_to_bus(body:Any, type:str):
    channel.basic_publish(exchange='', routing_key=ENVIRON_QUEUE_NAME, body=json.dumps(body), properties=BasicProperties(
        content_type= 'application/json',
        message_id= uuid.uuid4(),
        type= type))

def shutdown_channels():
    try:
        channel.close()
    except Exception as e:
        print(e)


def _consume_collaback(channel :Channel, method :Basic.Deliver, properties: BasicProperties, body:str):
    print(f"{channel} - {method} - {properties} - {body}")
    message_type = properties.type

    print(f"Received message of type {message_type}")

    try:
        if(message_type == MessageTypes.REGISTER_POTHOLE.value):
            process_register_pothole(body)
        if(message_type == MessageTypes.POTHOLE_NOT_FIXED.value):
            process_pothole_not_fixed(body)
        if(message_type == MessageTypes.NEW_USER_LOCATION.value):
            process_location_changed(body)
        if(message_type == MessageTypes.POTHOLE_EXISTS.value):
            process_pothole_exists(body)
        if(message_type == MessageTypes.POTHOLE_FIXED.value):
            process_pothole_fixed(body)
        if(message_type == MessageTypes.POTHOLE_NOT_REAL.value):
            process_pothole_not_real(body)

        # any other message type is ignored
    except Exception as e:
        print(e)    


channel.basic_consume(ENVIRON_QUEUE_NAME, _consume_collaback, auto_ack=True)

def listen_for_messages():
    print("Listening for messages from the bus...")
    try:
        channel.start_consuming()
    except Exception as e:
        print(e)
        try:
            sys.exit(-1)
        except SystemExit:
            os._exit(-1)

atexit.register(shutdown_channels)
