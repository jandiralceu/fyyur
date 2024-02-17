import os

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.urandom(32)

DEBUG = True

FLASK_ENV = "development"

SQLALCHEMY_DATABASE_URI = "postgresql://docker:docker@localhost:5432/nanodegree"

SECRET_KEY = "exaYU1ieEgdGAbUH41J"

SQLALCHEMY_TRACK_MODIFICATIONS = False

