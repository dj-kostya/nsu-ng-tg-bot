import json

import telebot
from flask import Flask, request, abort
from app_body import bot, Contants

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return "!", 200


messages = {}


@app.route(Contants.WEBHOOK_PATH, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        json_ = json.loads(json_string)
        chat = json_['message']['chat']
        chat_id = chat['id']
        date = json_['message']['date']
        print(chat_id, date)
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        abort(403)
