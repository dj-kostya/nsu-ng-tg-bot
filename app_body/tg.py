from app_body import Contants, db

import telebot

bot = telebot.TeleBot(Contants.TG_BOT_TOKEN)


def process_group_step(message):
    try:
        msg = bot.reply_to(message, 'How old are you?')
        # bot.register_next_step_handler(msg, process_group_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


@bot.message_handler(commands=['start'])
def start_command(message):
    tg_id = message['from_user']['id']
    row = db.Users.query.filter_by(tg_id=tg_id).first()
    if not row:
        rows = db.Groups.all()
        print(rows)
        msg = bot.reply_to(message, """\
        Привет, кажется ты еще не зарегистрирован
        What's your name?
        """)
        bot.register_next_step_handler(msg, process_group_step)
