import os

FLASK_HOST = '0.0.0.0'
FLASK_DEFAULT_PORT = '80'

TG_BOT_TOKEN = os.environ.get('TG_TOKEN')

WEBHOOK_URL = 'https://hidden-oasis-74904.herokuapp.com'
WEBHOOK_PATH = '/%s/' % TG_BOT_TOKEN

HEROKU_URL = 'postgres://jeoxzxcnnwjpwm:665e2782f80ad8cb22251705fd562d021b9c382db5b879b3534f3e5b58a595d7@ec2-174' \
             '-129-27-3.compute-1.amazonaws.com:5432/dbhtjhshau6f6s'

RUN_ALL = 9864
