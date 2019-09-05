from datetime import datetime

from app_body import Contants, db

import telebot
from sqlalchemy.sql import func

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
    msg = bot.send_message(tg_id, "Привет, {name}!\nЧем займемся сегодня?".format(name=row.tg_username),
                           reply_markup=keyboard)
    bot.register_next_step_handler(msg, main_page)


def save_run(m):
    tg_id = m.from_user.id
    text = m.text.replace(',', '.')
    user = db.Users.query.filter_by(tg_id=tg_id).first()
    if m.text == 'Вернуться на главную!':
        start_command(m)
    elif text.isdigit():
        db.RunHistory.create(id_user=user.id, total=float(text))
        msg = bot.send_message(tg_id, 'Я все сохранил!')
        start_command(m)
    else:
        msg = bot.send_message(tg_id, 'Укажи циферку в км')
        bot.register_next_step_handler(msg, save_run)


def main_page(m):
    tg_id = m.from_user.id
    if m.text == 'Я побегал!':
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[telebot.types.KeyboardButton(name) for name in ['Вернуться на главную!']])
        msg = bot.send_message(tg_id, "Сколько км ты пробежал за сегодня? ",
                               reply_markup=keyboard)
        bot.register_next_step_handler(msg, save_run)
    elif m.text == 'Получить свою статистику' or m.text == 'Получить статистику за сегодня':
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            *[telebot.types.KeyboardButton(name) for name in
              ['Вернуться на главную!', 'Получить статистику за месяц', 'Получить статистику за неделю',
               'Получить статистику за сегодня', 'Получить статистику за конкретный день']])

        row = db.session.query(func.sum(db.RunHistory.total).label("total"),
                                  func.max(db.RunHistory.total).label("max")).filter(
            db.RunHistory.sh_dt >= datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)).first()
        print(row)
        msg = bot.send_message(tg_id, "Сколько км ты пробежал за сегодня? ",
                               reply_markup=keyboard)
        bot.register_next_step_handler(msg, save_run)
