import serial
from flask import Flask
from app.db import init_app
from IA2_IoT.config import Config
import json
from app.db import get_db
from datetime import datetime

# Allow access to the database by setting up an application context
app = Flask(__name__)
app.config.from_object(Config)
init_app(app)

context = app.app_context()
context.push()
db = get_db()
ser = serial.Serial('COM3', 9600)  # Selects current serial port
while True:
    try:
        data = ser.readline().decode("utf-8")
        # Turn the string into a JSON object
        arduino_json = json.loads(data)
        db.execute('INSERT INTO ARDinfo (int_temp, rel_hum, timestamp)'
                   'VALUES (?,?,?);', (arduino_json["int_temp"], arduino_json["rel_hum"],
                                       datetime.today().strftime('%Y%m%d%H%M%S')))
        db.commit()
    except KeyboardInterrupt:
        break  # Stop getting data on command
    except json.decoder.JSONDecodeError:
        pass  # Continue if invalid data is entered
db.close()
context.pop()
