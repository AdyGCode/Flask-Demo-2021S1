# --------------------------------------------------------------
# File:     /app.py
# Project:  Flask-Demo
# Author:   Adrian Gould <Adrian.Gould@nmtafe.wa.edu.au>
# Created:  14/04/2021
# Purpose:  ...
#
# --------------------------------------------------------------
from csv import DictReader
from datetime import datetime, date
from flask import Flask, render_template

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from RainDB import Base, db_filename, Rainfall, db_data_file

app = Flask(__name__)

engine = create_engine(f"sqlite:///{db_filename}")
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)



@app.route('/splash')  # http://localhost:5000/splash
def splash():
    # current_date = datetime.now().date()
    # current_time = datetime.now().time()
    current_date = datetime.now().strftime("%d %B, %Y")
    current_time = datetime.now().strftime("%I:%M %p")
    return render_template('splash.html',
                           the_date=current_date,
                           the_time=current_time)


@app.route("/")  # http://localhost:5000/
def hello_world():
    # return "Yabba Dabba Doo! Fred Flintstone!"
    return render_template('index.html')


@app.route("/hello")
def greeting():
    return "<h1>Hello there</h1>"


@app.route("/hello/<name>")  # http://localhost:5000/hello/a_name
def hello(name):
    return f"<h1>Hello there, {name}</h1>"


@app.route("/rainfall")
def rainfall_page():
    session = sessionmaker(bind=engine)()
    rain_records = list(session.query(Rainfall).all())
    total_rain = 0
    for data in rain_records:
        total_rain += data.rainfall
    number_of_days = len(rain_records)
    mean_rain=0
    if number_of_days > 0:
        mean_rain = total_rain / number_of_days
    return render_template('db-rainfall.html',
                           rainfall=rain_records,
                           days=number_of_days,
                           total_rain=total_rain,
                           mean_rain=round(mean_rain, 3))


@app.route("/seed-rainfall")
def seed_rain():
    session = sessionmaker(bind=engine)()
    count = 0
    with open(db_data_file, 'r') as read_handle:
        dictionary_reader = DictReader(read_handle)
        list_of_rows = list(dictionary_reader)
    for data in list_of_rows:
        if data["Date Recorded"] != "" and data["Rainfall"] != "":
            day, month, year = data["Date Recorded"].split("-")
            rain_record = Rainfall()
            rain_record.location = data["Location"]
            rain_record.rainfall = data["Rainfall"]
            rain_record.date_recorded = date(int(year), int(month),
                                             int(day))
            session.add(rain_record)
            session.commit()
            count += 1
    return f"{count} Records Added"


if __name__ == "__main__":  # running our app.py
    app.run(debug=True)

#
# To Run the application in DEVELOPMENT mode,
# Open a terminal, and make sure you are in the project folder
# then... execute these two commands:
# set FLASK_ENV=development
# python3 -m flask run
#
