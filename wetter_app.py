from mako.template import Template
from mako.lookup import TemplateLookup
import cherrypy
from cherrypy.lib import static
import json
from datetime import datetime, timedelta

from db_read import read_current, read_data

mylookup = TemplateLookup(directories=['html'], output_encoding='utf-8',
                          input_encoding='utf-8', encoding_errors='replace')

default_type = "hours"
default_number = 24

def get_period(number, _type, start_date, end_date):
    if number != None and _type != None:
        end_date = datetime.now()
        try:
            start_date = end_date - timedelta(**{_type:int(number)})
        except:
            return (None, None, "Plese check your input")
    elif start_date != None and end_date != None:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M")
            end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M")
        except:
            return (None, None, "Plese check your input2")
    else:
        end_date = datetime.now()
        start_date = end_date - timedelta(**{default_type:default_number})
    return (start_date, end_date, None)

class bibthek(object):

    @cherrypy.expose
    def index(self):
        mytemplate = mylookup.get_template("index.html")
        weather = read_current()
        return mytemplate.render(weather=weather, current="index" )

    @cherrypy.expose
    def stats(self, start_date=None, end_date=None):
        mytemplate = mylookup.get_template("index.html")
        return mytemplate.render(current="stats")

    @cherrypy.expose
    def json_statistic(self, sensor, number=None, _type=None, 
                       start_date=None, end_date=None, limit_points = 800):

        sensors = sensor.split('.')
        start_date, end_date, error = get_period(number, _type, start_date,
                                                 end_date)
        if error != None:
            return error
        else:
            data = []
            for sensor in sensors:
                data += read_data(sensor, start_date,
                                      end_date, limit_points)
            
            return(json.dumps(data))

if __name__ == '__main__':
    cherrypy.quickstart(bibthek(), '/', 'app.conf')
