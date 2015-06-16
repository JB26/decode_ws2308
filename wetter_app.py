'''Webapp to visualize the data'''
from mako.lookup import TemplateLookup
import cherrypy
import json
from datetime import datetime, timedelta

from db_read import read_current, read_data, read_ev

MYLOOKUP = TemplateLookup(directories=['html'], output_encoding='utf-8',
                          input_encoding='utf-8', encoding_errors='replace')

DEFAULT_TYPE = "hours"
DEFAULT_NUMBER = 24
COLLECTING_START = datetime(2015, 5, 9)

def get_period(number, _type, start_date, end_date):
    '''Convert input to start_date, end_date'''
    if number != None and _type != None:
        end_date = datetime.now()
        try:
            start_date = end_date - timedelta(**{_type:int(number)})
        except ValueError:
            return (None, None, "Plese check your input")
    elif start_date != None and end_date != None:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M")
            end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M")
        except ValueError:
            return (None, None, "Plese check your input2")
    else:
        end_date = datetime.now()
        start_date = end_date - timedelta(**{DEFAULT_TYPE:DEFAULT_NUMBER})
    return (start_date, end_date, None)

class Weather(object):
    '''The webapp'''

    @cherrypy.expose
    def index(self):
        '''Show current weather'''
        mytemplate = MYLOOKUP.get_template("index.html")
        weather = read_current()
        start_date, end_date, error = get_period(24, 'hours', None, None)
        weather_max = read_ev(start_date, end_date, 'max')
        weather_min = read_ev(start_date, end_date, 'min')
        return mytemplate.render(weather=weather, weather_max=weather_max,
                                 weather_min=weather_min, current="index")

    @cherrypy.expose
    def stats(self, start_date=None, end_date=None):
        '''Show statistics'''
        mytemplate = MYLOOKUP.get_template("index.html")
        if start_date == None:
            start_date = COLLECTING_START
        if end_date == None:
            end_date = datetime.now()
        weather_max = read_ev(start_date, end_date, 'max')
        weather_min = read_ev(start_date, end_date, 'min')
        if weather_max['temp_in']['value'] == None:
            return("Kein gültiger Zeitraum ausgewählt.\n" +
                   "Dies kann vor allem passieren wenn ein " +
                   "kleiner Bereich ganz links ausgewählt wurde.")
        return mytemplate.render(weather_max=weather_max,
                                 weather_min=weather_min, current="stats")

    @cherrypy.expose
    def json_statistic(self, sensor, number=None, _type=None,
                       start_date=None, end_date=None):
        '''Return data as json'''
        sensors = sensor.split('.')
        start_date, end_date, error = get_period(number, _type, start_date,
                                                 end_date)
        if start_date < COLLECTING_START:
            start_date = COLLECTING_START
        weather_max_sql = read_ev(start_date, end_date, 'max')
        weather_min_sql = read_ev(start_date, end_date, 'min')
        weather_max = {}
        weather_min = {}
        if error != None:
            return error
        else:
            data = []
            for sensor in sensors:
                data += read_data(sensor, start_date, end_date)
                if sensor not in ['wind_d', 'wind_d_avg', 'rain']:
                    weather_max[sensor] = {'value':
                                           weather_max_sql[sensor]['value'],
                                           'date':
                                           weather_max_sql[sensor]['date']}
                    weather_min[sensor] = {'value':
                                           weather_min_sql[sensor]['value'],
                                           'date':
                                           weather_min_sql[sensor]['date']}
            data_return = {'data' : data, 'max': weather_max,
                           'min': weather_min}
            return json.dumps(data_return)

if __name__ == '__main__':
    cherrypy.quickstart(Weather(), '/', 'app.conf')
