#CREDITS & ACKNOWLEDGEMENTS
#ALCHEMYAPI: http://www.alchemyapi.com
#DATADESK'S PYTHON-GOOGLEGEOCODER PACKAGE: https://github.com/datadesk/python-googlegeocoder
#BEAUTIFULSOUP: http://www.crummy.com/software/BeautifulSoup/
#REDDIT r/worldnews: http://www.reddit.com/r/worldnews

from __future__ import print_function
from alchemyapi import AlchemyAPI
import pdb
import json
#import webapp2
import jinja2
import time
import pprint
import urllib2
from bs4 import BeautifulSoup
from googlegeocoder import GoogleGeocoder

# Step 1: Create the AlchemyAPI Object, Establish List Array, Set up Jinja2

alchemyapi = AlchemyAPI()
geocoder = GoogleGeocoder()
#jinja_environment = jinja2.Environment(
#    loader=jinja2.FileSystemLoader('templates'))

#class Marker():

#def __init__(self, latlng, title, url):
#    coords = str(latlng).split(',')
#    self.lat = coords[0]
#    self.lng = coords[1]
#    self.title = title
#    self.url = url

#class MainHandler(webapp2.RequestHandler):
 #   def get(self):
 #       markers = []
 #       for marker in list_of_markers:
 #           markers.append(Marker(latlng="coordinates go here in format 'latitude, longitude", title="Marker title goes here")

  #      for marker in markers:
   #         t_dict = {}
    #        t_dict['m_title'] = marker.title
     #       t_dict['m_lat'] = marker.lat
      #      t_dict['m_lng'] = marker.lng
       #     temp.append(t_dict)
       # json_markers = json.dumps(temp)

        #template_values = {'markers' :json_markers}

        #template = jinja_environment.get_template('index.html')
         #   self.response.out.write(template.render(template_values))

#Initialize the webapp

#application = webapp2.WSGIApplication([('/', MainHandler)], debug=False)

reddit_url = 'http://www.reddit.com/r/worldnews'

# Step 2: Define methods to generate each article's URL, Titles, and Geocode

def get_alchemy_title(articleurl):
    article_list = []
    response = alchemyapi.entities('url', articleurl, { 'showSourceText':1, 'sourceText':'xpath', 'xpath':'//*[contains(@class,"title may-blank")][1]' })
    if response['status'] == 'OK':
        text = response['text']
        titles = text.split('\n\n')
        return titles
    else:
        print('Error in entity extraction call: ', response['statusInfo'])
    return []

# this analyzes a URL for entities, then prepares them for geocoding

def google(address):
    try:
        search = geocoder.get(address)
        first_result = search[0]
        output =  [ 
            float(first_result.geometry.location.lat), 
            float(first_result.geometry.location.lng), 
        ]
        output_unicode = unicode(output)
        coordinates = (output_unicode)
        print(coordinates)

    except ValueError:
        error_address = [0, 0]
        error_address_unicode = unicode(error_address)
        coordinates = (error_address_unicode) 
        print(coordinates)
    return coordinates


def run_alchemy_entity_per_link(articleurl):
    locations = []
    relevance = []
    master_location = False
    response = alchemyapi.entities('url', articleurl) 
    if response['status'] == 'OK':

        for entity in response['entities']:
            if entity['type'] == 'Country' or entity['type'] == 'Region' or entity['type'] == 'City' or entity['type'] == 'StateOrCountry' or entity['type'] == 'Continent':

                currentRelevance = float(entity['relevance'])

                if entity.get('disambiguated'):
                    locations.append(entity['disambiguated']['name'])
                    relevance.append(currentRelevance)

                else:
                    locations.append(entity['text'])
                    relevance.append(currentRelevance)

            else:
                else_message = 'Not a Location'
                not_location_unicode = unicode(else_message)
                locations.append(not_location_unicode)
                relevance.append(0.0)

        if relevance:   
            max_pos = relevance.index(max(relevance)) # get nth position of the highest relevancy score
            master_location = (locations[max_pos]) #Use n to get nth position of all location names and store that location name to master_locations

    else:
        print('Error in entity extraction call: ', response['statusInfo'])
        neutral_location = 'Pacific Ocean'
        neutral_location_decoded = unicode(neutral_location)
        master_location = neutral_location_decoded
    
    return master_location

def get_all_links(page):
    urls = []
    coordinates = []
    master_locations = []
    html = urllib2.urlopen(page).read()
    soup = BeautifulSoup(html)
    for a in soup.find_all('a', 'title may-blank ', href=True):
        urls.append(a['href'])
        master_location = run_alchemy_entity_per_link(a['href'])
        coordinates.append(google(master_location))
        time.sleep(0.1)
    return coordinates, urls

def get_all_markers():
    markers = []
    titles = get_alchemy_title(reddit_url)
    print(len(titles))
    geos, links = get_all_links(reddit_url) 
    print(len(geos))
    print(len(links))

    for title, link, geo in zip(titles, links, geos):
        markers.append(
            {'title': title, 'link': link, 'geo': geo})
    print(markers)
    return markers

if __name__ == "__main__":
    print(get_all_markers())