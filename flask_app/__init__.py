import os

from flask import Flask, jsonify
from flask_mqtt import Mqtt


# error functions
def page_not_found(e):
        return jsonify(error=str(e)), 404

def internal(e):
        return jsonify(error=str(e)), 500

# add mqtt app
flask_app = None
mqtt = Mqtt()

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
    mqtt.subscribe("home/1")
    mqtt.subscribe("aa")

    mqtt.subscribe("scaun/user_asezat")
    mqtt.subscribe("scaun/avertisment")
    from mqtt import publisher_chair_sensor
    publisher_chair_sensor.mqtt = mqtt
    publisher_chair_sensor.flask_app = flask_app
    publisher_chair_sensor.on_connect()

    mqtt.subscribe('scaun/incalzire')
    mqtt.subscribe('camera/temperatura')


# print the message, later more logic
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    print(f"MQTT message --- topic: {message.topic}; message: {message.payload.decode()} ")

    if message.topic == 'camera/temperatura':
        from . import heat
        heat.new_temp(int(message.payload.decode()))

# app factory
def create_app(test_config=None, db_file=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=(db_file is not None))

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=os.path.join(app.instance_path, 'flask-app.sqlite'),
        )
    else:
        # load the test config if passed in
        app.config.from_object(test_config)

    if db_file is not None:
        app.config["DATABASE"] = db_file

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # error handling
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal)

    # database
    from . import db
    db.init_app(app)
    
    # Url to check if running
    @app.route('/')
    def hello():
        return 'Hello, World!'

    # Adding blueprints/controllers
    from . import user_info
    app.register_blueprint(user_info.bp)

    from . import heat
    app.register_blueprint(heat.bp)
    heat.mqtt = mqtt
    heat.app = app

    from . import weight
    app.register_blueprint(weight.bp)

    global flask_app
    flask_app = app

    # Adding mqtt app
    add_mqtt(app)

    return app
