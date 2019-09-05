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
        msg = bot.send_message(chat_id, 'Неверная группа')
        bot.register_next_step_handler(msg, process_group_step)
        return
    user = db.Users.create(tg_username=message.from_user.username, tg_id=message.from_user.id, id_group=int(text))
    db.commit()
    msg = bot.send_message(chat_id, 'Я все сохранил')
    bot.register_next_step_handler(msg, start_command)


@bot.message_handler(commands=['start'])
def start_command(message):
    print(message, message.from_user)
    print(type(message), type(message.from_user))
    tg_id = message.from_user.id
    print(tg_id)
    row = db.Users.query.filter_by(tg_id=tg_id).first()
    if not row:
        rows = db.Groups.all()
        msg = bot.send_message(tg_id, "\
                        Привет, кажется ты еще не зарегистрирован\nВыбери свою группу:\n" + '\n'.join(
            [
                '{id} - > {name}'.format(id=group.id, name=group.name)
                for group in rows
            ]
        ))
        bot.register_next_step_handler(msg, process_group_step)
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[telebot.types.KeyboardButton(name) for name in ['Я побегал!', 'Получить свою статистику']])
    admin_group = db.Groups.query.filter_by(name='Преподаватели').first()
    if row.id_group == admin_group.id:
        keyboard.add(*[telebot.types.KeyboardButton(name) for name in ['Получить статистику']])
    msg = bot.send_message(tg_id, "Привет, {name}!\nЧем займемся сегодня?".format(name=row.tg_username))
