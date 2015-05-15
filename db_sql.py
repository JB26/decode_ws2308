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

    c.execute('''create table if not exists avg_30m(sensor text, value real, 
                                                date timestamp)''')
    c.execute('''CREATE INDEX IF NOT EXISTS date_sensor_idx ON avg_30m(sensor, date DESC)''')

    conn.close()
    
def write_db(weather):
    c, conn = connect()
    sql = "INSERT INTO weather VALUES (?, ?, ?)"
    for sensor, value in weather.items():
        c.execute(sql, ( sensor, value, datetime.now()) )
    conn.commit()
    conn.close()

def write_many_db(weather, table):
    c, conn = connect()
    sql = "INSERT INTO " + table +" VALUES (?, ?, ?)"
    c.executemany(sql, weather )
    conn.commit()
    conn.close()

def read_db(sensor, start_date, end_date, table='weather'):
    c, conn = connect()
    sql = ('SELECT date, value FROM ' + table + ' WHERE sensor = ? AND' + 
           ' date BETWEEN ? AND ? ORDER BY date DESC')
    c.execute(sql, (sensor, start_date, end_date, ))
    rows = c.fetchall()
    c.close()
    return rows

def read_ev_sql(sensor, start_date, end_date, ev):
    c, conn = connect()
    sql = ('SELECT date, ' + ev + '(value) AS "value" FROM weather WHERE' +
           ' sensor = ? AND date BETWEEN ? AND ?')
    c.execute(sql, (sensor, start_date, end_date, ))
    row = c.fetchone()
    c.close()
    return row

def read_avg_last(table, sensor):
    c, conn = connect()
    sql = "SELECT date, value FROM " + table + " WHERE sensor = ? ORDER BY date DESC LIMIT 1"
    c.execute(sql, (sensor, ))
    rows = c.fetchall()
    c.close()
    return rows
