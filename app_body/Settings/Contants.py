import os

FLASK_HOST = '0.0.0.0'
FLASK_DEFAULT_PORT = '80'

TG_BOT_TOKEN = os.environ.get('TG_TOKEN')

WEBHOOK_URL = 'https://hidden-oasis-74904.herokuapp.com'
WEBHOOK_PATH = '/%s/' % TG_BOT_TOKEN

RUN_ALL = 9864
