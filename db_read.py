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
    
    c.execute("""SELECT date, value FROM weather WHERE sensor = ? 
                 AND date BETWEEN ? AND ?
                 ORDER BY date""", 
              (sensor, start_date, end_date, ))
    rows = c.fetchall()
    data = [['x_' + sensor],['data_' + sensor]]
    for row in rows:
        data[0].append(row['date'][:-10])
        data[1].append(row['value'])
    if sensor == "rain":
        if len(data[1]) > 3:
            x = data[1]
            data[1] = [data[1][0]] + [ x[i+1]-x[i] for i in range(1,len(x)-1) ]
            data[0].pop(1)
        else:
            data[1] = 0
    if limit_points != 0 and len(data[1][1:]) > limit_points:
        step_width = int(len(data[1][1:])/limit_points) + 1
        if sensor == "rain":
            values = [ np.sum(data[1][i:i+step_width])
                       for i in range(1,len(data[1]), step_width) ]
        else:
            values = [ np.mean(data[1][i:i+step_width])
                       for i in range(1,len(data[1]), step_width) ]

        data[1] = [data[1][0]] + list(np.round(values,decimals=2))
        data[0] = [data[0][0]] + data[0][int(step_width/2)+1::step_width]
    return data
