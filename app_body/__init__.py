import os

from flask import Flask, request
from app_body.Settings import Contants
from .BD import db

from .routes import app

debug = os.environ.get('DATABASE_URL') is None
db.set_session()
admin_group = db.Groups.query.filter_by(name='Преподаватели').first()
from .tg import bot
