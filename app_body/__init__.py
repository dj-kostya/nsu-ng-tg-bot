import os

from flask import Flask, request
from app_body.Settings import Contants
from .BD import db


from .tg import bot
from .routes import app
debug = os.environ.get('DATABASE_URL') is None
db.set_session()
