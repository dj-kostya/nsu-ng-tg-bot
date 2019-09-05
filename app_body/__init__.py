import os

from flask import Flask, request
from app_body.Settings import Contants
from .BD import db

from .routes import app
from .tg import bot, init
debug = os.environ.get('DATABASE_URL') is None
db.set_session()
init()

