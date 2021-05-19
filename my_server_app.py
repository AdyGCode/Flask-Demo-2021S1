# --------------------------------------------------------------
# File:     /my_server_app.py
# Project:  Flask-Demo
# Author:   Adrian Gould <Adrian.Gould@nmtafe.wa.edu.au>
# Created:  14/04/2021
# Purpose:  ...
#
# Renamed app.py to my_server_app.py and removed client based
# code, except for some basic details
# --------------------------------------------------------------
from datetime import date

from flask import Flask, jsonify, render_template
from flask_cors import CORS, cross_origin
from sqlalchemy import create_engine, desc, inspect
from sqlalchemy.orm import sessionmaker

from csv import DictReader
from RainDB import Base, db_data_file, db_filename, Rainfall

MyServerApp = Flask(__name__)
MyServerCors = CORS(MyServerApp,
                    resources={r"/api/*": {"origins": "*"}})
MyServerApp.config['CORS_HEADERS'] = 'Content-Type'

engine = create_engine(f"sqlite:///{db_filename}")
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


def object_as_dict(obj):
    """Convert an object to a dictionary

    :param obj:
    :return: dictionary
    """
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


def records_to_list(records):
    """Convert an SQLAlchemy set of records into a list

    :param records:
    :return: list
    """
    result_list = []
    for row in records:
        result_list.append(object_as_dict(row))
    return result_list


# API requests
@MyServerApp.route("/api/rain/<int:days>")
@cross_origin()
def api_rain(days):
    return api_rain_days_from(days, 1)


@MyServerApp.route("/api/rain/<int:days>/<int:start>")
@cross_origin()
def api_rain_days_from(days, start):
    if start > 0:
        start -= 1
    session = sessionmaker(bind=engine)()
    # organise the data in reverse order
    reverse_data_query = session.query(Rainfall) \
        .order_by(desc(Rainfall.date_recorded))
    # now retrieve the number of records required
    result_proxy = reverse_data_query.limit(days).offset(start).all()
    rain_records = records_to_list(result_proxy)
    rain_json = jsonify(rain_records)
    return rain_json


# Normal page requests
@MyServerApp.route("/")  # http://localhost:5000/
@cross_origin()
def hello_world():
    return render_template('index.html',
                           page="home",
                           system_name="Server")


@MyServerApp.route("/about")
def about_app():
    return render_template('server-about.html',
                           page="about",
                           system_name="Server", )


@MyServerApp.route("/seed-rainfall")
@cross_origin()
def seed_rain():
    session = sessionmaker(bind=engine)()
    count = 0
    with open(db_data_file, 'r') as read_handle:
        dictionary_reader = DictReader(read_handle)
        list_of_rows = list(dictionary_reader)
    for data in list_of_rows:
        # Product code,Bureau of Meteorology station number,Year,Month,Day,
        # Rainfall amount (millimetres),Period over which rainfall was
        # measured (days),Quality
        if data["Quality"] != "" \
                and data["Rainfall amount (millimetres)"] != "":
            day = data["Day"]
            month = data["Month"]
            year = data["Year"]
            rain_record = Rainfall()
            rain_record.location = data[
                "Bureau of Meteorology station number"]
            rain_record.rainfall = data["Rainfall amount (millimetres)"]
            rain_record.date_recorded = date(int(year), int(month),
                                             int(day))
            session.add(rain_record)
            session.commit()
            count += 1
    return render_template('server-seed.html',
                           page="seed",
                           records=count,
                           system_name="Server", )


# captures all incorrect page requests
@MyServerApp.route("/<anything>")
def error_404(anything=""):
    return render_template('404.html',
                           page="404",
                           system_name="Server",)


if __name__ == "__main__":  # running our app.py
    # as this is a demo, we prime the database with values then start the
    # application
    MyServerApp.run(debug=True, host="127.0.0.1", port="5050")

#
# To Run the application in DEVELOPMENT mode,
# Open a terminal, and make sure you are in the project folder
# then... execute these two commands:
# set FLASK_ENV=development
# python3 -m flask run --port=5050
#
