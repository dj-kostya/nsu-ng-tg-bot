from app_body import Contants, db

import telebot

bot = telebot.TeleBot(Contants.TG_BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start_command(message):
    print('message')


bot.polling()
