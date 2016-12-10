#!/usr/bin/env python

# Copyright (C) 2016 Mirjalol Norqulov
#

# 
import os

import bot
import telebot
from flask import Flask, request
from telebot import types


application = Flask(__name__)

# Empty webserver index, return nothing, just http 200
@application.route('/', methods=['GET', 'HEAD'])
def index():
    return ''

@application.route('/' + bot.TOKEN, methods=['GET', 'POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().encode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.bot.process_new_messages([update.message])
        return ''
    else:
        flask.abort(403)


if __name__ == '__main__':
    application.run(host='http://mybot-m-pro.44fs.preview.openshiftapps.com/',
        port=8443,
        debug=True)
    bot.bot.polling(none_stop = True)
