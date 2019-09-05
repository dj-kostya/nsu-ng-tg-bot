from app_body import Contants, db

import telebot

bot = telebot.TeleBot(Contants.TG_BOT_TOKEN)


def process_group_step(message):
    try:
        print(message)
        rows = db.Groups.all()
        msg = bot.reply_to(message, "\
                Привет, кажется ты еще не зарегистрирован\nВыбери свою группу:" + '\n'.join(
            [
                '{id} - > {name}'.format(id=group.id, name=group.name)
                for group in rows
            ]
        ))
    except Exception as e:
        bot.reply_to(message, 'oooops')


@bot.message_handler(commands=['start'])
def start_command(message):
    print(message, message.from_user)
    print(type(message), type(message.from_user))
    tg_id = message.from_user.id
    print(tg_id)
    row = db.Users.query.filter_by(tg_id=tg_id).first()
    if not row:
        msg = bot.send_message(tg_id, 'Привет, %s' % message.from_user.username)
        bot.register_next_step_handler(msg, process_group_step)
