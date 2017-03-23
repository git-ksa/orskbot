# -*- coding: utf-8 -*-" 
import sqlite3

con = sqlite3.connect('calcs.db')
cur = con.cursor()

# создать таблицу(или файл) если не существует
try:
 cur.execute('CREATE TABLE calcs (calc VARCHAR(20) PRIMARY KEY, who VARCHAR(50), datetime DATE ,text VARCHAR(1024))')
 con.commit()
except:
 print('EXCEPT: create table')
else:
 print('TABLE CREATED')

try:
 cur.execute('INSERT INTO calcs (calc,who,datetime, text) VALUES("pc", "Serg K.", CURRENT_TIMESTAMP,"calc 1")')
 con.commit()
except:
 print('EXCEPT: insert into table')
else:
 print('ROW INSERTED')

calc = "pc"

cur.execute('SELECT count(1) FROM calcs where lower(calc) = lower("'+calc+'")')
cur.execute('SELECT count(1) FROM calcs')
for row in cur:
    print ('Rows:'+str(row[0]))
#    rowcount = row[0]

cur.execute('SELECT * FROM calcs where lower(calc) = lower("'+calc+'")')
#cur.execute('SELECT * FROM calcs')
#print (len(cur.fetchall()))

for row in cur:
    print ('Calc:', row[0])
    print ('Who:', row[1])
    print ('Date:', row[2])
    print ('Text:', row[3])
cur.execute('UPDATE calcs set datetime=CURRENT_TIMESTAMP, who="Serg K.", text="+79051111111" where lower(calc) = "'+calc+'"')
con.commit()

print ('========================')

cur.execute('SELECT * FROM calcs where lower(calc) = lower("'+calc+'")')
for row in cur:
    print ('Calc:', row[0])
    print ('Who:', row[1])
    print ('Date:', row[2])
    print ('Text:', row[3])

con.close()