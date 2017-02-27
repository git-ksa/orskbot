# -*- coding: utf-8 -*-

import telebot
import config
import telnetlib
import requests.packages.urllib3
#requests.packages.urllib3.disable_warnings()
import time
import datetime
import urllib3
import pytz
import xmltodict

from telebot import types
from pytz import timezone

def listener(messages):
    for m in messages:
#        if (m.text.encode('utf-8') == '.п' or m.text == u'@OPCKBot .\u043f'):

#        markup = types.ReplyKeyboardMarkup(row_width=2)
#        itembtn1 = types.KeyboardButton('п')
#        itembtn2 = types.KeyboardButton('ку')
#        markup.add(itembtn1, itembtn2)

        if (m.text == u'.\u043f' or m.text == u'/\u043f' or m.text == u'@OPCKBot .\u043f' or m.text == u'/\u041f'):
# get text from telnet

#            bot.send_message(m.chat.id, "_", reply_markup=markup)

#            HOST = "pc.ornpz.ru"
#            tn = telnetlib.Telnet(HOST,90)
#            time.sleep(2)
#            tn_read =  tn.read_very_eager()
#            if  tn_read <> "":
#             bot.send_message(m.chat.id, tn_read + "\nhttp://pc.ornpz.ru/meteo/temperature1day.png")
            print u'Send .п text'
#              bot.send_message(m.chat.id, tn_read)
#            else:
#              bot.send_message(m.chat.id, "Произошла какаято хуйня (telnet: pc.ornpz.ru 90)...")

# get picture from url
            http = urllib3.PoolManager()
            r = http.request('GET', 'http://pc.ornpz.ru/meteo/temperature1day.png')
#            print r.status, r.data
            f = open('out.jpg','wb')
            f.write(r.data)
            f.close()
            print r.status

            if r.status == 200:
               print u'Send picture'
               bot.send_chat_action(m.chat.id, 'upload_photo')
               img = open('out.jpg', 'rb')
#              bot.send_photo(m.chat.id, img, reply_to_message_id=msgid)
               bot.send_photo(m.chat.id, img)
               img.close()
            else:
               bot.send_message(m.chat.id, "Произошла какаято хуйня (URL: http://pc.ornpz.ru/meteo/temperature1day.png)...") 
            # get temperature
            http = urllib3.PoolManager()
            r = http.request('GET', 'http://pc.ornpz.ru/meteo/meteo.xml')
            f = open('meteo.xml','wb')
            f.write(r.data)
            f.close()
            print r.status
            if r.status == 200:
              #     print u'Parse XML'
              with open('meteo.xml') as fd:
                doc = xmltodict.parse(fd.read())
              for section in doc['points']['point']:
                key = section.get('@name', None)
#        if key == 'PointName01':       # направление ветра
#           value = section.get('@value', None)            
#           print 'P:'+value
                if key == 'PointName05':       # температура
                 value = section.get('@value', None)            
                 print 'T:'+value
                 bot.send_message(m.chat.id,'T: '+value);
            else:
               bot.send_message(m.chat.id, u"cannot get content of ( URL: http://pc.ornpz.ru/meteo/meteo.xml)... ERROR:" + str(r.status))

        if (m.text == u'.\u043a\u0443' or m.text == u'@OPCKBot .\u043a\u0443' or m.text == u'/\u043a\u0443'):
             print u'Send .ку'
             tz = 'Asia/Yekaterinburg'
             fmt = '%Y-%m-%d %H:%M:%S'
             utc = datetime.datetime.utcnow()
             ural = timezone(tz).fromutc(utc)
             ural_string = ural.strftime(fmt)
             print ural_string
             bot.send_message(m.chat.id, ural_string)

#debug
        print m 
        print "\n" 
        print m.chat.id
        print "\n" 

if __name__ == '__main__':
    bot = telebot.TeleBot(config.token)
    bot.set_update_listener(listener)
    bot.polling(none_stop=True)
