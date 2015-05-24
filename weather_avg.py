import numpy as np

import db_sql
from datetime import datetime, timedelta

def write_avg():
    db_sql.init()
    sensors = ['temp_out', 'temp_in', 'humidity_out', 'humidity_in', 'wind_d',
               'wind_v', 'rain', 'pressure_in']

    for table in [{'table': 'avg_30m', 'delta_half': 15, 'read': 'weather'},
                {'table': 'avg_6h', 'delta_half': 3*60, 'read': 'avg_30m'}]:
        weather = list()
        for sensor in sensors:
            last = db_sql.read_avg_last(table['table'], sensor)
            if last != []:
                start_date = ( str_to_date(last[0]['date']) +
                                   timedelta(minutes=table['delta_half']) )
            else:
                start_date = datetime(2000, 1, 1, 0, 0)
            end_date = datetime.now()
            rows = db_sql.read_db(sensor, start_date, end_date, table['read'])
            if len(rows) < 30:
                print("Not enough (new) values in db")
                break
            start = str_to_date(rows[0]['date']) # We're going back in time
            if table['table'] == 'avg_30m':
                if start.minute < 15:
                    end = datetime(start.year, start.month, start.day,
                                   start.hour-1, 45)
                elif start.minute > 44:
                    end = datetime(start.year, start.month,
                                   start.day, start.hour, 45)
                else:
                    end = datetime(start.year, start.month, start.day, start.hour, 15)
            elif table['table'] == 'avg_6h':
                if start.hour < 3:
                    end = datetime(start.year, start.month, start.day-1, 21)
                elif start.hour < 9:
                    end = datetime(start.year, start.month, start.day, 3)
                elif start.hour < 15:
                    end = datetime(start.year, start.month, start.day, 9)
                elif start.hour < 21:
                    end = datetime(start.year, start.month, start.day, 15)
                else:
                    end = datetime(start.year, start.month, start.day, 21)
        
            values = []
            for row in rows:
                if str_to_date(row['date']) > end:
                    values.append(row['value'])
                elif values != []:
                    if sensor == "rain":
                        avg = values[int(len(values)/2)]
                    else:
                        avg = np.round(np.mean(values), decimals=2)
                    weather.append( (sensor, avg,
                            end + timedelta(minutes=table['delta_half']), ) ) 
                    values = [row['value']]
                    end -= timedelta(minutes=table['delta_half']*2)
        db_sql.write_many_db(weather, table['table'])
    return None
        

def str_to_date(date_str):
    return datetime.strptime(date_str[:19], "%Y-%m-%d %H:%M:%S")

if __name__ == "__main__":
    error = write_avg()
    if error != None:
        print(error)
