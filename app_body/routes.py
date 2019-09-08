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
        date = int(json_['message']['date'])
        global messages
        if chat_id in messages:
            if messages and messages[chat_id]['date'] >= date \
                    and ('text' not in json_['message'] or json_['message']['text'] == messages[chat_id]['data']):
                return ''
        messages[chat_id] = dict(date=date, data=json_['message']['text'] if 'text' in json_['message'] else None)
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        abort(403)
