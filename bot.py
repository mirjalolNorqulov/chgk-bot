#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2016 Mirjalol Norqulov
#

import telebot
import requests
import json
import bs4
from telebot import types

#API TOKEN
TOKEN = '237816678:AAEg8NJtmsUCUuyg7nFokTYVt1w5vN4EW8M'

open_book = '\xF0\x9F\x93\x96'
key = '\xF0\x9F\x94\x91'
red_question = '\xE2\x9D\x93'

bot = telebot.TeleBot(TOKEN)

markup = types.ReplyKeyboardMarkup(row_width = 2)
button = types.KeyboardButton("{0} Savol".format(open_book))
markup.add(button)


@bot.message_handler(commands = ['start'])
def response_to_start(message):
	text = """Bilimdonlarga savollar\n Buyruqlar:\n /start - Botni ishga tushirish
	/savol - Savol olish
	/javob - Agar savol olingan bo'lsa javobini olish
	"""
	bot.send_message(message.chat.id, text = text, reply_markup = markup)

	
@bot.message_handler(commands = ['savol'])
@bot.message_handler(func = lambda message:message.text == ("{0} Savol".format(open_book)).decode('utf-8'))
def give_question(message):
	question = get_question()

	text = u"{0} ".format(red_question.decode('utf-8')) + question['question']
	
	# If there is image in question send image
	if question['img_source']:
		bot.send_message(message.chat.id, text = question['img_source'])
	
	answer_button = types.KeyboardButton("{0} Javob".format(key))
	
	markup = types.ReplyKeyboardMarkup(row_width = 2)	
	markup.add(button, answer_button)
	answer = question['answer']
	msg = bot.send_message(message.chat.id, text = text, reply_markup = markup)
	bot.register_next_step_handler(msg, lambda m: answer_question(m, answer))

'''@bot.message_handler(func = lambda message:message.text == ("{0} Javob".format(key)).decode('utf-8'))
def answer_question(message):
	bot.send_message(message.chat.id, text = answer)
'''

def answer_question(message, answer):
	if message.text == ("{0} Javob".format(key)).decode('utf-8') or message.text == '/javob' or message.text == '/javob@norqulov_bot':
		bot.send_message(message.chat.id, text = answer)
	else:
		bot.register_next_step_handler(message, lambda m: answer_question(m, answer))
	
	


	
def get_question():
	try:
		r = requests.get('http://db.chgk.info/random')
	except requests.HTTPError:
		return "Xatolik sodir bo'ldi, noqulaylik uchun uzur. Qayta urinib ko'ring"
	except requests.ConnectionError:
		return "Serverga ulanishda xatolik sodir bo'ldi, noqulaylik uchun uzur. Qayta urinib ko'ring"
	except ProxyError:
		return "Xatolik sodir bo'ldi, noqulaylik uchun uzur. Qayta urinib ko'ring"
	except requests.Timeout:
		return "Savolni olishda serverdan javob bo'lmadi, noqulaylik uchun uzur. Qayta urinib ko'ring"
	except:
		return "Xatolik sodir bo'ldi, noqulaylik uchun uzur. Qayta urinib ko'ring"
	
	
	soup = bs4.BeautifulSoup(r.text, 'html.parser')
	random_question = soup.find('div', attrs = {'class': 'random_question'})
	print '\n\nRQ:', random_question
	image = random_question.find('img')
	img_source = None
	if image:
		img_source = image['src']
	
	text = random_question.get_text()
	
	question_separator = u'Вопрос 1:'
	answer_separator = u'Ответ:'
	
	where_were = text.split(question_separator)[0]
	text = text.split(question_separator)[1]
	
	question = u'Вопрос: ' + text.split(answer_separator)[0]
	question = question.replace(u'...', u'')
	answer = u'Ответ: ' + text.split(answer_separator)[1]
	
	
	
	return {
		'where_were': where_were,
		'question': question,
		'answer': answer, 
		'img_source': img_source
	}
	

