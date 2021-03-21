import json
import sqlite3


with open('ready/Портовый.json') as f:
    data = json.load(f)


day = 0
month = 1
year = 1
id = 1
con = sqlite3.connect('db/base.db')
cur = con.cursor()
for i in range(len(data)):
    dayInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if day < dayInMonth[month - 1]:
        day += 1
    else:
        day = 1
        if month < 12:
            month += 1
        else:
            year += 1
            month = 1
            day = 1

    print(day, month, year)
    cur.execute("""INSERT INTO data VALUES(?,?,?,?,?,?)""", [id, 1, day, month, year, data[i]])
    id += 1

con.commit()
con.close()