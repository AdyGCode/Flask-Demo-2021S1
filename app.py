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
from flask import Flask, render_template, jsonify

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from RainDB import Base, db_filename, Rainfall, db_data_file

app = Flask(__name__)

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
    """Convert an SQLAlchemy set fo records into a list

    :param records:
    :return: list
    """
    result_list = []
    for row in records:
        result_list.append(object_as_dict(row))
    return result_list


@app.route("/")  # http://localhost:5000/
def hello_world():
    return render_template('index.html',
                           page="home")


@app.route('/splash')  # http://localhost:5000/splash
def splash():
    # current_date = datetime.now().date()
    # current_time = datetime.now().time()
    current_date = datetime.now().strftime("%d %B, %Y")
    current_time = datetime.now().strftime("%I:%M %p")
    return render_template('splash.html',
                           page="splash",
                           the_date=current_date,
                           the_time=current_time)


@app.route("/clock")
def clock():
    return render_template('clock.html',
                           page='clock')


@app.route("/about")
def about_app():
    return render_template('about.html',
                           page="about")


@app.route("/rainfall")
def rainfall_page():
    session = sessionmaker(bind=engine)()
    rain_records = list(session.query(Rainfall).all())
    total_rain = 0
    mean_rain = 0
    number_of_days = len(rain_records)
    if number_of_days > 0:
        for data in rain_records:
            total_rain += data.rainfall
        mean_rain = total_rain / number_of_days
    return render_template('db-rainfall.html',
                           page="rainfall",
                           rainfall=rain_records,
                           days=number_of_days,
                           total_rain=total_rain,
                           mean_rain=round(mean_rain, 3))


@app.route("/api/rain/<int:days>")
def api_rain(days):
    return api_rain_days_from(days, 1)


@app.route("/api/rain/<int:days>/<int:start>")
def api_rain_days_from(days, start):
    if start > 0:
        start -= 1
    session = sessionmaker(bind=engine)()
    resultproxy = session.query(Rainfall).limit(days) \
        .offset(start).all()
    rain_records = records_to_list(resultproxy)
    return jsonify(rain_records)


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


# ---------------------------------------
# Sample routes with simple demos showing results such as paths,
# passing values and type specifications in URL data


@app.route("/hello")
def greeting():
    return "<h1>Hello there</h1>"


@app.route("/hello/<name>")  # http://localhost:5000/hello/a_name
def hello(name):
    return f"<h1>Hello there, {name}</h1>"


@app.route("/numbers/<int:maximum>")
def show_numbers(maximum):
    output = ""
    for number in range(1, maximum + 1):
        output += f"{number:>5}"
    return output


@app.route('/user/<username>')
def show_user_profile(username):
    return 'User %s' % escape(username)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post %d' % post_id


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    return 'Subpath %s' % escape(subpath)


if __name__ == "__main__":  # running our app.py
    app.run(debug=True, host="127.0.0.1", port="5000")

#
# To Run the application in DEVELOPMENT mode,
# Open a terminal, and make sure you are in the project folder
# then... execute these two commands:
# set FLASK_ENV=development
# python3 -m flask run
#
