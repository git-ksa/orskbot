#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import pytz
import random
import datetime
import telebot
import requests
import xmltodict
from pytz import timezone
from datetime import time

import config

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['wc', 'пч'])
@bot.message_handler(regexp="^.пч$")
@bot.message_handler(regexp="^.ч$")
@bot.message_handler(regexp="^.чп$")
def send_weather(message):
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?id=1508291&units=metric&mode=xml&appid=7cad4e5a16fc989137d9dcaa7d726ff8')
    if r.status_code == 200:
        doc = xmltodict.parse(r.text)
        temperature = doc['current']['temperature']['@value']
    else:
        temperature = 'хз сколько там за бортом, наденьте шарф'

    tz = 'Asia/Yekaterinburg'
    fmt = '%Y-%m-%d %H:%M:%S'
    utc = datetime.datetime.utcnow()
    now = timezone(tz).fromutc(utc)
    time_str = timezone(tz).fromutc(utc).strftime(fmt)
    now_time = now.time()
    if now_time <= time(22,00) and now_time >= time(11,00):
        station = '9900854'
    else:
        station = '9900846'

    user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
    s = requests.Session()
    r = s.get('https://yandex.ru/maps/api/masstransit/getStopInfo', headers = user_agent)
    r_dict = r.json()
    token = r_dict.get('csrfToken')

    url = 'https://yandex.ru/maps/api/masstransit/getStopInfo?csrfToken=' + token + '&host_config[hostname]=yandex.ru&id=stop__' + station + '&locale=ru_RU&mode=prognosis'
    r = s.get(url, headers = user_agent)
    r_dict = r.json()

    try:
        station_name = r_dict['data']['properties']['name']
        current_time = r_dict['data']['properties']['currentTime']
    except KeyError:
        bot.send_message(message.chat.id, 'За бортом: ', temperature) 
        bot.send_message(message.chat.id, 'C пепелацем произошла какая-то хуйня...')
        return

    fmt = '%H:%M:%S'
    local = pytz.timezone('Europe/Moscow')
    naive = datetime.datetime.strptime(current_time, '%a %b %d %Y %H:%M:%S GMT+0300 (MSK)')
    local_time = local.localize(naive, is_dst=None)
    current_time = local_time.astimezone(pytz.timezone('Asia/Yekaterinburg'))

    message_list = []
    message_list.append('Галактика: ' + station_name)
    message_list.append('Местное время: ' + current_time.strftime(fmt))
    message_list.append('За бортом: ' + temperature)

    try:
        for item in r_dict['data']['properties']['StopMetaData']['Transport']:
            if item['name'] == '22':
                count = 0;
                if 'Events' in item['BriefSchedule']:
                    for i in item['BriefSchedule']['Events']:
                        estimate_time = datetime.datetime.strptime(i['Estimated']['value'], '%Y-%m-%dT%H:%M:%S+05:00')
                        local = pytz.timezone('Asia/Yekaterinburg')
                        local_time = local.localize(estimate_time, is_dst=None)
                        delta_time = local_time - current_time
                        hours, remainder = divmod(delta_time.seconds, 3600)
                        minutes, seconds = divmod(remainder, 60)
                        if minutes > 30: continue
                        count += 1
                        message_list.append('Пепелац №22 прибывает через: ' + str(minutes) + ' мин. ' + str(seconds) + ' сек. на ' + str(count) + ' путь')
                if count == 0: message_list.append('Пепелац №22 пока не прибывает, ждите')
    except KeyError:
        bot.send_message(message.chat.id, 'За бортом: ', temperature)
        bot.send_message(message.chat.id, 'C пепелацем произошла какая-то хуйня...')
        return
    msg = ''
    for item in message_list:
        msg += item + '\n'
    bot.send_message(message.chat.id, msg)

@bot.message_handler(commands=['w', 'п'])
@bot.message_handler(regexp="^.п$")
#@bot.message_handler(regexp="^п$")
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
        bot.send_message(message.chat.id, "Произошла какая-то хуйня (URL: http://pc.ornpz.ru/meteo/temperature1day.png)...") 

    # get temperature
    r = requests.get('http://pc.ornpz.ru/meteo/meteo.xml')
    if r.status_code == 200:
        doc = xmltodict.parse(r.text)
            
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

@bot.message_handler(commands=['wm', 'пм'])
@bot.message_handler(regexp="^.пм$")
#@bot.message_handler(regexp="^пм$")
def send_weather(message):
    # get temperature MSK
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?id=524901&units=metric&mode=xml&appid=7cad4e5a16fc989137d9dcaa7d726ff8')
    if r.status_code == 200:
        doc = xmltodict.parse(r.text)
        value = doc['current']['temperature']['@value']
        print('MSK T:' + value)
        bot.send_message(message.chat.id,'MSK T: ' + value)
    else:
        bot.send_message(message.chat.id, u"cannot get content of ( URL: http://api.openweathermap.org/data/2.5/weather?id=524901&units=metric&mode=xml&appid=7cad4e5a16fc989137d9dcaa7d726ff8)... ERROR:" + str(r.status))

@bot.message_handler(commands=['wy', 'пя'])
@bot.message_handler(regexp="^.пя$")
@bot.message_handler(regexp="^пя$")
def send_weather(message):
    # get temperature MSK
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?id=468902&units=metric&mode=xml&appid=7cad4e5a16fc989137d9dcaa7d726ff8')
    if r.status_code == 200:
        doc = xmltodict.parse(r.text)
        value = doc['current']['temperature']['@value']
        print('YAR T:' + value)
        bot.send_message(message.chat.id,'YAR T: ' + value)
    else:
        bot.send_message(message.chat.id, u"cannot get content of ( URL: http://api.openweathermap.org/data/2.5/weather?id=468902&units=metric&mode=xml&appid=7cad4e5a16fc989137d9dcaa7d726ff8)... ERROR:" + str(r.status))



@bot.message_handler(commands=['ku', 'ку'])
@bot.message_handler(regexp="^(ку|\.ку|ku|\.ku|re|\.re)$")
def send_ku(message):
    tz = 'Asia/Yekaterinburg'
    fmt = '%Y-%m-%d %H:%M:%S'
    utc = datetime.datetime.utcnow()
    time_str = timezone(tz).fromutc(utc).strftime(fmt)
    bot.send_message(message.chat.id, time_str)


@bot.message_handler(regexp="^(ку|\.ку|ku|\.ku|re|\.re) ([А-Яa-я]*)")
def send_ku_town(message):
    tz = 'Asia/Yekaterinburg'

    if re.search(r'Орск|Orsk', message.text):
        tz = 'Asia/Yekaterinburg'

    if re.search(r'Москва|Moscow|Питер|Piter|СПб', message.text):
        tz = 'Europe/Moscow'

    fmt = '%Y-%m-%d %H:%M:%S'
    utc = datetime.datetime.utcnow()
    time_str = timezone(tz).fromutc(utc).strftime(fmt)
    bot.send_message(message.chat.id, time_str)

@bot.message_handler(commands=['сиськи'])
@bot.message_handler(regexp="^(сиськи|\.сиськи)$")
def send_cucki(message):
   if message.chat.id != -1001046809592 and message.chat.id != -242669552:
     f = open('cucbka.dat')
     links = f.read().split('\n')
     f.close()
 
     i = random.randint(0, len(links) - 1)
     url = "https://blog.stanis.ru/" + links[i]
     bot.send_message(message.chat.id, url)
   else:
    tz = 'Europe/Moscow'
    fmt = '%Y-%m-%d %H:%M:%S'
    utc = datetime.datetime.utcnow()
    now = timezone(tz).fromutc(utc)
    time_str = timezone(tz).fromutc(utc).strftime(fmt)
    now_time = now.time()
    if now_time <= time(7,00) or now_time >= time(18,30):
      f = open('cucbka.dat')
      links = f.read().split('\n')
      f.close() 

      i = random.randint(0, len(links) - 1)
      url = "https://blog.stanis.ru/" + links[i]
      bot.send_message(message.chat.id, url)
    else:
      print (time_str+'с 7:00 по 18:30 MSK сиськи не показываю. Пишите в приват. @OPCKBot ')
      bot.send_message(message.chat.id, 'с 7:00 по 18:30 MSK сиськи не показываю. Пишите в приват @OPCKBot')

bot.polling(none_stop=True)