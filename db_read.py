'''Read data'''
from datetime import timedelta, datetime
import numpy as np

import db_sql

def read_current():
    '''Read current values'''
    sensors = ['temp_out', 'temp_in', 'humidity_out', 'humidity_in', 'wind_d',
               'wind_v', 'rain', 'pressure_in']
    weather = {}
    for sensor in sensors:
        rows = db_sql.read_db(sensor,
                              (datetime.now() - timedelta(minutes=61)),
                              datetime.now())
        weather[sensor] = rows[0]
        if sensor == 'rain':
            if len(rows) > 2:
                rain_last_hour = rows[0]['value'] - rows[-1]['value']
            else:
                rain_last_hour = "Nan"
            weather['rain_last_hour'] = {'value' : rain_last_hour}
    return weather

def read_ev(start_date, end_date, extrem):
    '''Read extrem values'''
    sensors = ['temp_out', 'temp_in', 'humidity_out', 'humidity_in', 'wind_v',
               'pressure_in']
    weather = {}
    for sensor in sensors:
        weather[sensor] = db_sql.read_ev_sql(sensor, start_date, end_date,
                                             extrem)
    return weather

def read_data(sensor, start_date, end_date):
    '''Read data for given period'''
    if sensor == 'wind_d_avg':
        sensor = 'wind_d'
        special = 'wind_d_avg'
    else:
        special = ''

    if (end_date - start_date) > timedelta(hours=(15*24)):
        table = 'avg_6h'
    elif (end_date - start_date) > timedelta(hours=25):
        table = 'avg_30m'
    else:
        table = 'weather'
    rows = db_sql.read_db(sensor, start_date, end_date, table)
    data = [['x_' + sensor], ['data_' + sensor]]
    for row in rows:
        data[0].append(row['date'][:16])
        data[1].append(row['value'])
    if sensor == "rain":
        if len(data[1]) > 2:
            temp = data[1]
            data[1] = [data[1][0]] + [temp[i]-temp[i+1]
                                      for i in range(1, len(temp)-1)]
            data[0].pop(1)
        elif len(data[1]) == 2:
            data[1][1] = 0

    if special == 'wind_d_avg' and len(data[1]) > 1:
        wind_d_avg = np.unique(np.round(np.array(data[1][1:])*2)/2,
                               return_counts=True)
        data[0] = ['x_wind_d_avg'] + list(wind_d_avg[0])
        sum_wind = wind_d_avg[1].sum()
        if sum_wind != 0:
            data[1] = (['data_wind_d_avg'] +
                       [int(x/sum_wind*1000)/10 for x in wind_d_avg[1]])
        else:
            data[1] = ['data_wind_d_avg'] + [0]*16

    if len(data[1]) == 1:
        data = [None]
    return data
