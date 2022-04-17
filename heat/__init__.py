import os
from random import random
from flask import Flask
from flask_mqtt import Mqtt
import time
from threading import Thread
from random import randint

mqtt = Mqtt()
thread = None
temp = 21

def add_mqtt(app):
    app.config['MQTT_BROKER_URL'] = 'localhost'  # use the free broker from HIVEMQ
    app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
    app.config['MQTT_USERNAME'] = ''  # set the username here if you need authentication for the broker
    app.config['MQTT_PASSWORD'] = ''  # set the password here if the broker demands authentication
    app.config['MQTT_KEEPALIVE'] = 60  # set the time interval for sending a ping to the broker to 5 seconds
    app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes

    mqtt.init_app(app)
    return mqtt

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("Heat connected to MQTT")
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.daemon = True
        thread.start()

def background_thread():
    global temp
    while True:
        time.sleep(10)
        x = randint(-1, 1)
        temp = temp + x
        print(temp)
        mqtt.publish('camera/temperatura', temp)

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        app.config.from_pyfile('flask_configurations.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    add_mqtt(app)
    return app
