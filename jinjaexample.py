from __future__ import print_function
import json
import webapp2
import jinja2

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates'))

class Marker():

def __init__(self, latlng, title, url):
    coords = str(latlng).split(',')
    self.lat = coords[0]
    self.lng = coords[1]
    self.title = title
    self.url = url

class MainHandler(webapp2.RequestHandler):
    def get(self):
        markers = []
        for marker in list_of_markers:
            markers.append(Marker(latlng="coordinates go here in format 'latitude, longitude", title="Marker title goes here")

        for marker in markers:
            t_dict = {}
            t_dict['m_title'] = marker.title
            t_dict['m_lat'] = marker.lat
            t_dict['m_lng'] = marker.lng
            temp.append(t_dict)
        json_markers = json.dumps(temp)

        template_values = {'markers' :json_markers}

        template = jinja_environment.get_template('index.html')
            self.response.out.write(template.render(template_values))

application = webapp2.WSGIApplication([('/', MainHandler)], debug=False)

article_list = [] #this will feed into 'title' in the init
urls = [] #this will feed into url in the init
coordinates = [] #this will feed into latlng in the init, as a list item of [X, Y]

#run extra python code to populate the 3 lists, article_list, urls, and coordinates