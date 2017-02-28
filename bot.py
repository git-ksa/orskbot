# -*- coding: utf-8 -*-
import time
import datetime

import telebot
import requests
import xmltodict
from pytz import timezone

import config

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['w', 'п'])
@bot.message_handler(regexp="^.п$")
@bot.message_handler(regexp="^п$")
def send_weather(message):
    r = requests.get('http://pc.ornpz.ru/meteo/temperature1day.png')
    if r.status_code == 200:
        f = open('out.jpg', 'wb')
        f.write(r.content)
        f.close()

        bot.send_chat_action(message.chat.id, 'upload_photo')
        img = open('out.jpg', 'rb')
        bot.send_photo(message.chat.id, img)
        img.close()
    else:
        bot.send_message(message.chat.id, "Произошла какаято хуйня (URL: http://pc.ornpz.ru/meteo/temperature1day.png)...") 

    # get temperature
    r = requests.get('http://pc.ornpz.ru/meteo/meteo.xml')
    if r.status_code == 200:
        f = open('meteo.xml', 'wb')
        f.write(r.content)
        f.close()

        with open('meteo.xml') as fd:
            doc = xmltodict.parse(fd.read())
            
        for section in doc['points']['point']:
            key = section.get('@name', None)
            # направление ветра
            #if key == 'PointName01':
            #    value = section.get('@value', None)
            #    print 'P:'+value

            # температура
            if key == 'PointName05':       
                value = section.get('@value', None)
                print('T:' + value)
                bot.send_message(message.chat.id,'T: ' + value)
    else:
        bot.send_message(message.chat.id, u"cannot get content of ( URL: http://pc.ornpz.ru/meteo/meteo.xml)... ERROR:" + str(r.status))


@bot.message_handler(commands=['ku', 'ку'])
@bot.message_handler(regexp="^.ку$")
@bot.message_handler(regexp="^ку$")
def send_ku(message):
    tz = 'Asia/Yekaterinburg'
    fmt = '%Y-%m-%d %H:%M:%S'
    utc = datetime.datetime.utcnow()
    ural = timezone(tz).fromutc(utc)
    ural_string = ural.strftime(fmt)
    print(ural_string)
    bot.send_message(message.chat.id, ural_string)
    #bot.reply_to(message, ural_string)


bot.polling(none_stop=True)