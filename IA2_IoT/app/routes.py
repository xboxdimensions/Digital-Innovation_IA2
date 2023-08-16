import os

import requests
from flask import (redirect, render_template, send_from_directory,
                   session)

from app import app
from app.db import get_db  # Get Database
from app.Forms import AdjustTemp  # Adjust Threshold Form
from IA2_IoT.config import password, username  # Proxy Information

proxies = {'http': f'http://{username}:{password}@proxy.eq.edu.au:80',
           'https': f'http://{username}:{password}@proxy.eq.edu.au:80'}  # Proxy Details
url = f"http://reg.bom.gov.au/fwo/IDQ60901/IDQ60901.94576.json"  # BOM Data API


@app.route('/', methods=["GET", "POST"])
def index():
    session['message'] = ''  # Resets Adjustment message
    r = requests.get(url, proxies=proxies)  # Gets API information
    # assigns the data list inside the JSON to variable
    records = r.json()['observations']['data']
    db = get_db()  # Open database
    try:
        if session["MaxInt"]:
            pass  # checks if it is a new session
    except KeyError:
        session["MaxInt"] = 40  # Sets default thresholds
        session["MaxOut"] = 35
    for tempdict in records:  # Iterates between all records
        result = db.execute(
            'SELECT * FROM BOMinfo WHERE local_date_time_full = ?', (tempdict["local_date_time_full"],))  # Checks if there is data for the specific time already
        if not result.fetchall():
            db.execute('INSERT INTO BOMinfo (air_temp, apparent_t, rel_hum, local_date_time_full)'  # Add Required Data to BOMinfo SQL database
                       'VALUES (?,?,?,?);', (tempdict["air_temp"], tempdict["apparent_t"], tempdict["rel_hum"], tempdict["local_date_time_full"]))
            db.commit()  # Save Database
    alltempinfoq = db.execute(  # Gets the latest data to be displayed on website
        'SELECT air_temp, apparent_t, rel_hum FROM BOMinfo order by local_date_time_full desc limit 1;')
    tempinfo = [(row["air_temp"], row["apparent_t"], row["rel_hum"])
                for row in alltempinfoq]  # Gets information from query

    arddata = db.execute(
        'SELECT int_temp,rel_hum FROM ARDinfo order by timestamp desc limit 1;')  # Gets latest data from arduino sensor
    int_info = [(row["int_temp"], row["rel_hum"])
                for row in arddata]  # Gets the value from the query
    print(int_info)
    # Renders the html template
    return render_template('index.html', title="Temperature Info - UAP", bigtitle="Temperature Info", tempinfo=tempinfo, int_info=int_info, MaxInt=session["MaxInt"], MaxOut=session["MaxOut"])


@app.route('/settings', methods=["GET", "POST"])
def settings():
    # Displays if user has incorrectly submitted data
    message = session['message']
    Form = AdjustTemp()  # Sends form to HTML
    return render_template('alert.html', bigtitle="Adjust Threshold", message=message, Form=Form, title="Temperature Threshold Adjustments - UAP")


# Allows POST requests to this route
@app.route('/setthresh', methods=["POST"])
def posthere():
    Form = AdjustTemp()
    if Form.validate_on_submit():
        try:
            # Check if a decimal number was entered
            MaxInt = float(Form.MaxInt.data)
            MaxOut = float(Form.MaxOut.data)
            session["MaxInt"] = MaxInt  # Stores the threshold throughout pages
            session["MaxOut"] = MaxOut
            return redirect("/")  # Returns to main page
        except ValueError:
            # Displays if a non-number was entered for either entry
            session['message'] = "Your input is not valid"
            return redirect('/settings')  # Returns to settings page
    else:
        session['message'] = "Your input is not valid"
        return redirect('/settings')  # Returns to settings page


@app.route('/favicon.ico')
def favicon():  # Displays the UAP Logo as the favicon
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
