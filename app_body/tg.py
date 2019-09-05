import calendar
from datetime import datetime, timedelta

from app_body import Contants, db

import telebot
from sqlalchemy.sql import func, and_

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
    start_command(message)


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
    try:
        total = float(text)
    except ValueError:
        total = None
    if m.text == 'Вернуться на главную!':
        start_command(m)
    elif total:
        db.RunHistory.create(id_user=user.id, total=total)
        msg = bot.send_message(tg_id, 'Я все сохранил!')
        db.commit()
        start_command(m)
    else:
        msg = bot.send_message(tg_id, 'Укажи циферку в км')
        bot.register_next_step_handler(msg, save_run)


def get_user_stat(m):
    tg_id = m.from_user.id
    user = db.Users.query.filter_by(tg_id=tg_id).first()
    if m.text == 'Получить свою статистику' or m.text == 'за сегодня' or m.text == 'за неделю' or m.text == 'за месяц' \
            or m.text == 'за все время':
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            *[telebot.types.KeyboardButton(name) for name in
              ['за месяц', 'за неделю',
               'за сегодня', 'за все время', 'Вернуться на главную!']])
        dt = datetime.now()
        if m.text == 'Получить свою статистику' or m.text == 'за сегодня':
            start = dt.replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=1) - timedelta(seconds=1)
        elif m.text == 'за неделю':
            start = dt - timedelta(days=dt.weekday())
            end = start + timedelta(days=6)
        elif m.text == 'за месяц':
            start = dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=calendar.monthrange(dt.year, dt.month)[1] - 1)
        else:
            start = dt.replace(year=2000)
            end = dt.replace(year=3000)
        row = db.session.query(func.sum(db.RunHistory.total).label("total"),
                               func.max(db.RunHistory.total).label("max")).filter(
            and_(and_(
                db.RunHistory.sh_dt >= start, db.RunHistory.sh_dt <= end),
                db.RunHistory.id_user == user.id
            )).first()

        msg = bot.send_message(tg_id,
                               "За период с {start_dt} по {end_dt} ты пробежал: {total} км\n"
                               "Из них максимальная дистанция: {max} км".format(
                                   total=row[0] if row[0] else 0, max=row[1] if row[1] else 0,
                                   start_dt=start.strftime('%Y-%m-%d'), end_dt=end.strftime('%Y-%m-%d'), )
                               , reply_markup=keyboard)
        bot.register_next_step_handler(msg, get_user_stat)
    elif m.text == 'Вернуться на главную!':
        start_command(m)
    else:
        main_page(m)


def get_all_stat(m):
    tg_id = m.from_user.id
    user = db.Users.query.filter_by(tg_id=tg_id).first()
    if m.text == 'Получить статистику' or m.text == 'за сегодня' or m.text == 'за неделю' or m.text == 'за месяц' \
            or m.text == 'за все время':
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            *[telebot.types.KeyboardButton(name) for name in
              ['за месяц', 'за неделю',
               'за сегодня', 'за все время', 'Вернуться на главную!']])
        dt = datetime.now()
        if m.text == 'Получить статистику' or m.text == 'за сегодня':
            start = dt.replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=1) - timedelta(seconds=1)
        elif m.text == 'за неделю':
            start = dt - timedelta(days=dt.weekday())
            end = start + timedelta(days=6)
        elif m.text == 'за месяц':
            start = dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=calendar.monthrange(dt.year, dt.month)[1] - 1)
        else:
            start = dt.replace(year=2000)
            end = dt.replace(year=3000)
        row = db.session.query(func.sum(db.RunHistory.total).label("total"),
                               func.max(db.RunHistory.total).label("max")).filter(
            and_(
                db.RunHistory.sh_dt >= start, db.RunHistory.sh_dt <= end)
        ).first()

        msg = bot.send_message(tg_id,
                               "За период с {start_dt} по {end_dt} все пробежали: {total} км\n"
                               "Из них максимальная дистанция : {max} км".format(
                                   total=row[0] if row[0] else 0, max=row[1] if row[1] else 0,
                                   start_dt=start.strftime('%Y-%m-%d'), end_dt=end.strftime('%Y-%m-%d'))
                               , reply_markup=keyboard)
        bot.register_next_step_handler(msg, get_all_stat)
    elif m.text == 'Вернуться на главную!':
        start_command(m)
    else:
        main_page(m)


@bot.message_handler(content_types=['text'])
def main_page(m):
    tg_id = m.from_user.id
    user = db.Users.query.filter_by(tg_id=tg_id).first()
    if m.text == 'Я побегал!':
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[telebot.types.KeyboardButton(name) for name in ['Вернуться на главную!']])
        msg = bot.send_message(tg_id, "Сколько км ты пробежал за сегодня? ",
                               reply_markup=keyboard)
        bot.register_next_step_handler(msg, save_run)

    elif m.text == 'Получить свою статистику':
        get_user_stat(m)
    elif m.text == 'Получить статистику':
        get_all_stat(m)
    else:
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[telebot.types.KeyboardButton(name) for name in ['Вернуться на главную!']])
        msg = bot.send_message(tg_id, "По-моему, ты ошибся!",
                               reply_markup=keyboard)
        bot.register_next_step_handler(msg, start_command)
