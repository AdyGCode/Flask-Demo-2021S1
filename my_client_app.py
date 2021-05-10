# --------------------------------------------------------------
# File:     /my_client_app.py
# Project:  Flask-Demo
# Author:   Adrian Gould <Adrian.Gould@nmtafe.wa.edu.au>
# Created:  14/04/2021
# Purpose:  ...
#
# Copied from the previous app.py, removed the non-client
# content, such as SQLAlchemy, database access etc
# --------------------------------------------------------------
from datetime import date, datetime
from html import escape

from flask import app, Flask, jsonify, render_template


MyClientApp = Flask(__name__)


@MyClientApp.route("/")  # http://localhost:5000/
def hello_world():
    return render_template('index.html',
                           page="home")


@MyClientApp.route("/clock")
def clock():
    return render_template('clock.html',
                           page='clock')


@MyClientApp.route("/about")
def about_app():
    return render_template('about.html',
                           page="about")


@MyClientApp.route("/rainfall")
def rainfall_page():
    '''
    Show the rainfall data (n days) via AJAX)
    :return:
    '''
    return render_template('rainfall.html',
                           page="rainfall",
                           )


@MyClientApp.route("/rainfall/chart")
def rainfall_chart_page():
    return "Not Yet Defined"


if __name__ == "__main__":  # running our app.py
    MyClientApp.run(debug=True, host="127.0.0.1", port="5000")

#
# To Run the application in DEVELOPMENT mode,
# Open a terminal, and make sure you are in the project folder
# then... execute these two commands:
# set FLASK_ENV=development
# python3 -m flask run
#
