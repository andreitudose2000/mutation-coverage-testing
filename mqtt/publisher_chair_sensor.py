import random
import time
from datetime import datetime
from threading import Thread

mqtt = None
flask_app = None
is_currently_sitting = False
sitting_status_thread = None
sit_too_much_warning_thread = None

def on_connect():
    print("Main app to MQTT")
    global sitting_status_thread
    if sitting_status_thread is None:
        with flask_app.app_context():
            sitting_status_thread = Thread(target=sitting_status_thread_func)
            sitting_status_thread.daemon = True
            print("Starting sitting_status_thread")
            sitting_status_thread.start()
            print("Started sitting_status_thread")
    global sit_too_much_warning_thread
    if sit_too_much_warning_thread is None:
        with flask_app.app_context():
            sit_too_much_warning_thread = Thread(target=sit_too_much_warning_thread_func)
            sit_too_much_warning_thread.daemon = True
            print("Starting sit_too_much_warning_thread")
            sit_too_much_warning_thread.start()
            print("Started sit_too_much_warning_thread")

def sitting_status_thread_func():
    global is_currently_sitting
    while True:
        time.sleep(5)
        chance = random.randint(1, 100)
        if chance <= 1:
            is_currently_sitting = not is_currently_sitting
            print(f"Senzor scaun --> Userul s-a {'asezat' if is_currently_sitting else 'ridicat'}")
            from flask_app import sitting_status
            sitting_status.flask_app = flask_app
            with flask_app.app_context():
                sitting_status.set_sitting_status(is_currently_sitting)
            mqtt.publish("scaun/user_asezat", is_currently_sitting)

def sit_too_much_warning_thread_func():
    while True:
        time.sleep(60)
        from flask_app import sitting_status
        sitting_status.flask_app = flask_app
        with flask_app.app_context():
            sitting_status = sitting_status.get_sitting_status()
        if sitting_status is not None:
            if sitting_status["is_sitting"] == 1:
                lastUpdate = datetime.strptime(sitting_status["updated_on"], '%Y-%m-%d %H:%M:%S')
                duration = datetime.now() - lastUpdate
                if duration.total_seconds() > 30 * 60:
                    print(f"Senzor scaun --> Userul nu s-a mai ridicat de 30 minute")
                    mqtt.publish("scaun/avertisment", b"Ati stat pe scaun prea mult. Luati o pauza.")
