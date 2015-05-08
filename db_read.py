import sqlite3
from datetime import timedelta, datetime

from db_sql import connect

def delta_time(values, last):
    delta = ( datetime(values[0]['year'], values[0]['month'], values[0]['day'], 
                       values[0]['hour'], values[0]['minute']) - 
              datetime(values[last]['year'], values[last]['month'], values[last]['day'], 
                       values[last]['hour'], values[last]['minute']) )
    return(delta)
    
def last_index(values, period):
    last = -1
    delta = delta_time(values, last)
    while delta > timedelta(**period) and (len(values) + last) > 1:
        last -= 1
        delta = delta_time(values, last)
    return last

def read_current():
    c, conn = connect()
    sensors = ['temp_out', 'temp_in', 'humidity_out', 'humidity_in', 'wind_d',
               'wind_v', 'rain', 'pressure_in']
    weather = {}
    for sensor in sensors:
        c.execute("""SELECT * FROM weather WHERE sensor = ? ORDER BY 
                     date DESC LIMIT 1""", (sensor,))
        weather[sensor] = c.fetchone()

    weather['rain_last_hour'] = {'value' : 0}
    c.close()
    return weather

def read_data(sensor, start_date, end_date):
    c, conn = connect()
    
    c.execute("""SELECT * FROM weather WHERE sensor = ? BETWEEN ? AND ?
                 ORDER BY date""", 
              (sensor, start_date, end_date, ))
    rows = c.fetchall()
    data = {'labels' : [], 'values' : []}
    for row in rows:
        data['labels'].append(row['date'])
        data['values'].append(row['value'])
    data['labels'].reverse()
    data['values'].reverse()
    if sensor == "rain":
        x = data['values']
        data['values'] = [ x[i]-x[i+1] for i in range(len(x)-1) ]
        data['labels'].pop(1)
    return data
