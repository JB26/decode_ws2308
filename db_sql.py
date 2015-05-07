import sqlite3
from datetime import datetime

def connect():
    conn = sqlite3.connect('weather.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    return c, conn

c, conn = connect()
c.execute('''create table if not exists weather(year int, month int, 
                                                day int, hour int, 
                                                minute int, sensor text,
                                                value real, date text)''')
sql = "INSERT INTO weather VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

def write_db(weather):
    year = datetime.now().strftime("%Y")
    month = datetime.now().strftime("%m")
    day = datetime.now().strftime("%d")
    hour = datetime.now().strftime("%H")
    minute = datetime.now().strftime("%M")
    date = year + "-" + month + "-" + day + "T" + hour + ":" + minute
    
    for sensor, value in weather.items():
        c.execute(sql, ( int(year), int(month), int(day), int(hour),
                         int(minute), sensor, value, date) )
    conn.commit()
