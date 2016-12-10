#!/usr/bin/env python

# Copyright (C) 2016 Mirjalol Norqulov
#

# 
'''import os
import bot
import telebot
from flask import Flask, request
from telebot import types


application = Flask(__name__, instance_path=os.environ['OPENSHIFT_PYTHON_DIR'])
update_queue, bot_instance = bot.setup(webhook_url='https://{}/{}'.format(
    os.environ['OPENSHIFT_GEAR_DNS'],
    bot.TOKEN
))


@application.route('/')
def not_found():
    """Server won't respond in OpenShift if we don't handle the root path."""
    return ''


@application.route('/' + bot.TOKEN, methods=['GET', 'POST'])
def webhook():
    if request.json:
        #update_queue.put(Update.de_json(request.json, bot_instance))
        update = telebot.types.Update.de_json(request.json)
        bot.bot.process_new_messages([update.message])
    return ''


if __name__ == '__main__':
    ip = os.environ['OPENSHIFT_PYTHON_IP']
    port = int(os.environ['OPENSHIFT_PYTHON_PORT'])
    application.run(host=ip, port=port)
'''


from bot import bot

if __name__ == '__main__':
    bot.polling(none_stop = True)

