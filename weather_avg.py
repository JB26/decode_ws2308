import numpy as np

import db_sql
from datetime import datetime, timedelta

def write_avg():
    db_sql.init()
    sensors = ['temp_out', 'temp_in', 'humidity_out', 'humidity_in', 'wind_d',
               'wind_v', 'rain', 'pressure_in']

    weather = list()
    for sensor in sensors:
        last = db_sql.read_avg_last('avg_30m', sensor)
        if last != []:
            start_date = str_to_date(last[0]['date']) + timedelta(minutes=15)
        else:
            start_date = datetime(2000, 1, 1, 0, 0)
        end_date = datetime.now()
        rows = db_sql.read_db(sensor, start_date, end_date)
        if len(rows) < 30:
            return "Not enough (new) values in db"
        start = str_to_date(rows[0]['date']) # We're going back in time
        if start.minute < 15:
            end = datetime(start.year, start.month, start.day,
                           start.hour-1, 45)
        elif start.minute > 44:
            end = datetime(start.year, start.month,
                           start.day, start.hour, 45)
        else:
            end = datetime(start.year, start.month, start.day, start.hour, 15)
    
        values = []
        for row in rows:
            if str_to_date(row['date']) > end:
                values.append(row['value'])
            else:
                if sensor == "rain":
                    avg = values[int(len(values)/2)]
                else:
                    avg = np.round(np.mean(values), decimals=2)
                weather.append( (sensor, avg, end+timedelta(minutes=15), ) ) 
                values = [row['value']]
                end -= timedelta(minutes=30)
    db_sql.write_many_db(weather, 'avg_30m')
    return None
        

def str_to_date(date_str):
    return datetime.strptime(date_str[:19], "%Y-%m-%d %H:%M:%S")

if __name__ == "__main__":
    error = write_avg()
    if error != None:
        print(error)
