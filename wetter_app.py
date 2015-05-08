from mako.template import Template
from mako.lookup import TemplateLookup
import cherrypy
from cherrypy.lib import static
import json
from datetime import datetime, timedelta

from db_read import read_current, read_data

mylookup = TemplateLookup(directories=['html'], output_encoding='utf-8',
                          input_encoding='utf-8', encoding_errors='replace')

class bibthek(object):

    @cherrypy.expose
    def index(self):
        mytemplate = mylookup.get_template("index.html")
        weather = read_current()
        return mytemplate.render(weather=weather)
        
    @cherrypy.expose
    def json_statistic(self, sensor):
        end_date = datetime.now()
        start_date = end_date - timedelta(hours = 10)
        data = read_data(sensor, start_date, end_date)
        return(json.dumps(data))

if __name__ == '__main__':
    cherrypy.quickstart(bibthek(), '/', 'app.conf')
