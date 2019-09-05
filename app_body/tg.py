from app_body import Contants, db

import telebot

bot = telebot.TeleBot(Contants.TG_BOT_TOKEN)


def process_group_step(message):
    chat_id = message.chat.id
    text = message.text
    if not text.isdigit():
        msg = bot.send_message(chat_id, 'Группа должна быть числом')
        bot.register_next_step_handler(msg, process_group_step)
        return
    if not db.Groups.find(int(text)):
        msg = bot.send_message(chat_id, 'Не верная группа')
        bot.register_next_step_handler(msg, process_group_step)
        return
    user = db.Users.create(tg_username=message.from_user.username, tg_id=message.from_user.id, id_role=int(text),
                           id_group=1)
    db.commit()
    msg = bot.send_message(chat_id, 'Я все созхранил')
    bot.register_next_step_handler(msg, start_command)


@bot.message_handler(commands=['start'])
def start_command(message):
    print(message, message.from_user)
    print(type(message), type(message.from_user))
    tg_id = message.from_user.id
    print(tg_id)
    row = db.Users.query.filter_by(tg_id=tg_id).first()
    if not row:
        rows = db.Groups.create()
        msg = bot.send_message(tg_id, "\
                        Привет, кажется ты еще не зарегистрирован\nВыбери свою группу:\n" + '\n'.join(
            [
                '{id} - > {name}'.format(id=group.id, name=group.name)
                for group in rows
            ]
        ))
        bot.register_next_step_handler(msg, process_group_step)
