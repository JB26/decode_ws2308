import sqlite3
from datetime import datetime

conn = sqlite3.connect('weather.db')
c = conn.cursor()
c.execute('''create table if not exists weather(year int, month int, day int, 
                                                hour int, minute int, 
                                                sensor text, value real)''')
sql = "INSERT INTO weather VALUES (?, ?, ?, ?, ?, ?, ?)"

def write_db(weather):
    year = int(datetime.now().strftime("%Y"))
    month = int(datetime.now().strftime("%m"))
    day = int(datetime.now().strftime("%d"))
    hour = int(datetime.now().strftime("%H"))
    minute = int(datetime.now().strftime("%M"))
    for sensor, value in weather.items():
        c.execute(sql, (year, month, day, hour, minute, sensor, value))
    conn.commit()
    c.execute('select * from weather')
    for row in c:
        print(row)
