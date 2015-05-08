import sqlite3
from datetime import timedelta, datetime

from db_sql import connect

def delta_time(values, last):
    delta = ( datetime(values[0]['year'], values[0]['month'], values[0]['day'], 
                       values[0]['hour'], values[0]['minute']) - 
              datetime(values[last]['year'], values[last]['month'], values[last]['day'], 
                       values[last]['hour'], values[last]['minute']) )
    return(delta)

def read_current():
    c, conn = connect()
    sensors = ['temp_out', 'temp_in', 'humidity_out', 'humidity_in', 'wind_d',
               'wind_v', 'rain', 'pressure_in']
    weather = {}
    for sensor in sensors:
        c.execute("""SELECT * FROM weather WHERE sensor = ? ORDER BY 
                     date DESC LIMIT 1""", (sensor,))
        weather[sensor] = c.fetchone()
    c.execute("""SELECT * FROM weather WHERE sensor = ? ORDER BY 
                 date DESC LIMIT 6""", ('rain',) )
    rain_6 = c.fetchall()
    last = -1
    delta = delta_time(rain_6, last)
    while delta > timedelta(minutes=61) and (len(rain_6) + last) > 1:
        last -= 1
        delta = delta_time(rain_6, last)
    if (len(rain_6) + last) < 2:
        rain_last_hour = 0
    else:
        rain_last_hour = rain_6[0]['value'] - rain_6[last]['value']
    weather['rain_last_hour'] = {'value' : round(rain_last_hour,1)}
    c.close()
    return weather

def read_data(sensor, period={'hours':1}):
    c, conn = connect()
    minutes = timedelta(**period).total_seconds()/60
    if sensor == "rain":
        count = int(minutes/10)
    else:
        count = int(minutes/2)
    c.execute("""SELECT * FROM weather WHERE sensor = ? ORDER BY 
                 date DESC LIMIT ?""", (sensor, count, ))
    rows = c.fetchall()
    last = -1
    delta = delta_time(rows, last)
    while delta > timedelta(**period) and (len(rows) + last) > 1:
        last -= 1
        delta = delta_time(rows, last)
    data = {'labels' : [], 'values' : []}
    for row in rows[0:len(rows) + last + 1]:
        data['labels'].append(row['minute'])
        data['values'].append(row['value'])
    data['labels'].reverse()
    data['values'].reverse()
    if sensor == "rain":
        x = data['values']
        data['values'] = [ x[i]-x[i+1] for i in range(len(x)-1) ]
        data['labels'].pop(1)
    return data
