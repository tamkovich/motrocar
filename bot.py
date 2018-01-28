# -*- coding: utf-8 -*-

import config
import telebot
import os
import random
import urllib.request as urllib2
from bs4 import BeautifulSoup
from urllib.request import urlopen

token = ''

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def handler_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('/start', '/stop')
    user_markup.row('расписание')
    bot.send_message(message.from_user.id, 'Здравствуй, ' + message.from_user.first_name , reply_markup=user_markup)

@bot.message_handler(commands=['stop'])
def handler_start(message):
    hide_markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, 'Введите /start для получения расписания', reply_markup=hide_markup)

@bot.message_handler(content_types=['text'])
def handler_text(message):
    if message.text == 'расписание':
        s = urlopen('http://mrk-bsuir.by').read()
        soup = BeautifulSoup(s, 'html.parser')

        for link in soup.find_all('a'):
            x = str(link.get('href'))
            if ('pdf' in x) and ('upload' not in x):
                break

        bot.send_chat_action(message.from_user.id, 'upload_document')
        bot.send_document(message.from_user.id, x)

bot.polling(none_stop=True)




