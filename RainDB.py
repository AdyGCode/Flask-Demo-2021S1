# --------------------------------------------------------------
# File:     /RainDB.py
# Project:  Flask-Demo
# Author:   Adrian Gould <Adrian.Gould@nmtafe.wa.edu.au>
# Created:  5/05/2021
# Purpose:  ...
#
# --------------------------------------------------------------

import os

from sqlalchemy import Column, Date, DateTime, Float, func, \
    Integer, String
from sqlalchemy.ext.declarative import declarative_base

db_folder = "./data/"
db_name = "rainfall.db"
db_filename = f"{db_folder}{db_name}"
db_csv_folder = "./csv/"
db_text_file = "IDCJAC0009_009225_1800_Data.csv"
db_data_file = f"{db_csv_folder}{db_text_file}"

# Check for the data folder and create if it is not present
if not os.path.isdir(db_folder):
    os.makedirs(db_folder, mode=0o755)

Base = declarative_base()


class Rainfall(Base):
    __tablename__ = "rainfall"
    id = Column(Integer, primary_key=True, autoincrement=True)
    rainfall = Column(Float)
    location = Column(String)
    date_recorded = Column(Date)
    created_at = Column(DateTime, server_default=func.now())

    def __init__(self):
        self.location = "UNKNOWN"
        self.date_recorded = "1000-01-01"
        self.rainfall = -999.99

    def __str__(self):
        return_string = f"{self.id:>6} {self.location:<40}" \
                        f"{self.date_recorded} {self.rainfall:>6.2f}"
        return return_string
