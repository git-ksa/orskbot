#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 Scripts parse links for cuckI pictures =) 
 and write to file cucbka.dat
"""
import time

import requests
from lxml import html, etree

MIN_PAGE = 731
MAX_PAGE = 821

f = open('cucbka.dat', 'a')
for page in range(MIN_PAGE, MAX_PAGE + 1):
    print("Proccess page: " + str(page))
    
    r = requests.get('https://blog.stanis.ru/?action=sch&searchby=category&what=4&page=' + str(page))
    if r.status_code == 200:
        tree = html.fromstring(r.text)
        links = tree.xpath('//div[@class="pic"]/img/@src')
        f.write("\n".join(links))
    if page != MAX_PAGE:
        f.write("\n")
        time.sleep(2)

f.close()