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
default_number = 10

def get_period(number, _type, start_date, end_date):
    if number != None and _type != None:
        end_date = datetime.now()
        try:
            start_date = end_date - timedelta(**{_type:int(number)})
        except:
            return (None, None, "Plese check your input")
    elif start_date != None and end_date != None:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M")
            end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M")
        except:
            return (None, None, "Plese check your input2")
    else:
        end_date = datetime.now()
        start_date = end_date - timedelta(**{default_type:default_number})
    return (start_date, end_date, None)

class bibthek(object):

    @cherrypy.expose
    def index(self, number=None, _type=None, start_date=None, end_date=None):
        mytemplate = mylookup.get_template("index.html")
        weather = read_current()
        if (number==None and _type==None
            and start_date==None and end_date==None):
            number = default_number
            _type = default_type
        translated_time = [["minutes","Minuten"],["hours","Stunden"],
                           ["days","Tage"],["months","Monate"],
                           ["years","Jahre"]]
        start, end, error = get_period(number, _type, start_date, end_date)
        if error != None:
            return error
        else:
            return mytemplate.render(weather=weather, number=number,
                                     _type=_type, start_date=start_date,
                                     end_date=end_date,
                                     translated_time=translated_time,
                                     start=start, end=end)
        
    @cherrypy.expose
    def json_statistic(self, sensor, number=None, _type=None, 
                       start_date=None, end_date=None):

        start_date, end_date, error = get_period(number, _type, start_date,
                                                 end_date)
        if error != None:
            return error
        else:
            data = read_data(sensor, start_date, end_date)
            return(json.dumps(data))

if __name__ == '__main__':
    cherrypy.quickstart(bibthek(), '/', 'app.conf')
