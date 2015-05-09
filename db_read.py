import sqlite3
from datetime import timedelta, datetime

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

def read_data(sensor, start_date, end_date):
    c, conn = connect()
    
    c.execute("""SELECT * FROM weather WHERE sensor = ? 
                 AND date BETWEEN ? AND ?
                 ORDER BY date""", 
              (sensor, start_date, end_date, ))
    rows = c.fetchall()
    data = {'labels' : [], 'values' : []}
    for row in rows:
        data['labels'].append(row['date'][:-10])
        data['values'].append(row['value'])
    if sensor == "rain":
        if len(data['values']) > 2:
            x = data['values']
            data['values'] = [ x[i+1]-x[i] for i in range(0,len(x)-1) ]
            data['labels'].pop(1)
        else:
            data['values'] = None
            data['labels'] = None
    return data
