#!/usr/bin/env bash
set FLASK_APP=my_client_app.py
set FLASK_ENV=development
python -m flask run --port=5000
