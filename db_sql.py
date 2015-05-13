import sqlite3
from datetime import datetime

def connect():
    conn = sqlite3.connect('weather.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    return c, conn

def init():
    c, conn = connect()
    c.execute('''create table if not exists weather(sensor text, value real, 
                                                date timestamp)''')
    c.execute('''CREATE INDEX IF NOT EXISTS date_sensor_idx ON weather(sensor, date DESC)''')
    conn.close()
    
def write_db(weather):
    c, conn = connect()
    sql = "INSERT INTO weather VALUES (?, ?, ?)"
    for sensor, value in weather.items():
        c.execute(sql, ( sensor, value, datetime.now()) )
    conn.commit()
    conn.close()

def read_db(sensor, start_date, end_date):
    c, conn = connect()
    sql = """SELECT date, value FROM weather WHERE sensor = ? AND
             date BETWEEN ? AND ? ORDER BY date DESC"""
    c.execute(sql, (start_date, end_date, sensor, ))
    rows = c.fetchall()
    c.close()
    return rows
