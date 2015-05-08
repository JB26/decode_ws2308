import sqlite3
from datetime import datetime

def connect():
    conn = sqlite3.connect('weather.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    return c, conn

c, conn = connect()
c.execute('''create table if not exists weather(sensor text, value real, 
                                                date timestamp)''')
sql = "INSERT INTO weather VALUES (?, ?, ?)"

def write_db(weather):
    
    for sensor, value in weather.items():
        c.execute(sql, ( sensor, value, datetime.now()) )
    conn.commit()
