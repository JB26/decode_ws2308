import sqlite3
from datetime import timedelta, datetime
from time import mktime, strptime
import numpy as np

from db_sql import connect

def read_current():
    c, conn = connect()
    sensors = ['temp_out', 'temp_in', 'humidity_out', 'humidity_in', 'wind_d',
               'wind_v', 'rain', 'pressure_in']
    weather = {}
    for sensor in sensors:
        c.execute("""SELECT * FROM weather WHERE sensor = ? ORDER BY 
                     date DESC LIMIT 1""", (sensor,))
        weather[sensor] = c.fetchone()

    c.execute("""SELECT * FROM weather WHERE sensor = ? 
                 AND date BETWEEN ? AND ?
                 ORDER BY date""", 
              ('rain', datetime.now() - timedelta(minutes = 61), 
               datetime.now(), ))
    rows = c.fetchall()
    if len(rows) > 2:
        rain_last_hour = rows[-1]['value'] - rows[0]['value']
    else:
        rain_last_hour = "Nan"
    weather['rain_last_hour'] = {'value' : rain_last_hour}
    c.close()
    return weather

def read_data(sensor, start_date, end_date, limit_points = 0):
    c, conn = connect()
    
    c.execute("""SELECT * FROM weather WHERE sensor = ? 
                 AND date BETWEEN ? AND ?
                 ORDER BY date""", 
              (sensor, start_date, end_date, ))
    rows = c.fetchall()
    data = {'values' : [], 'key' : sensor}
    for row in rows:
        data['values'].append({'x' : int(mktime(strptime(row['date'][:-7], "%Y-%m-%d %H:%M:%S"))), 'y' : row['value']})
    if sensor == "rain":
        if len(data['values']) > 2:
            x = data['values']
            data['values'] = [ x[i+1]-x[i] for i in range(0,len(x)-1) ]
            data['labels'].pop(1)
        else:
            data['values'] = None
            data['labels'] = None

    #if limit_points != 0 and len(data['values']) > limit_points:
        #step_width = int(len(data['values'])/limit_points) + 1
        #values = [ np.mean(data['values'][i:i+step_width])
        #           for i in range(0,len(data['values']), step_width) ]

        #data['values'] = [range(len(values)), list(np.round(values,decimals=2))]
        #data['labels'] = data['labels'][int(step_width/2)::step_width]
        #del data['labels']
    return data
