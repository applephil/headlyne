#CREDITS & ACKNOWLEDGEMENTS
#ALCHEMYAPI: http://www.alchemyapi.com
#DATADESK'S PYTHON-GOOGLEGEOCODER PACKAGE: https://github.com/datadesk/python-googlegeocoder
#BEAUTIFULSOUP: http://www.crummy.com/software/BeautifulSoup/
#D3.JS: 

from __future__ import print_function
from alchemyapi import AlchemyAPI
import pdb
import json
import pprint
import urllib2
from bs4 import BeautifulSoup
from googlegeocoder import GoogleGeocoder

# Step 1: Create the AlchemyAPI Object, Establish List Array

alchemyapi = AlchemyAPI()
geocoder = GoogleGeocoder()
reddit_url = 'http://www.reddit.com/r/worldnews'
article_list = []
urls = []
locations = []
relevance = []
master_locations = []
coordinates = []

# this analyzes a URL for entities, then prepares them for geocoding


def run_alchemy_entity_per_link(articleurl):
    response = alchemyapi.entities('url', articleurl) 
    if response['status'] == 'OK':
        for entity in response['entities']:
            if entity['type'] in entity == 'Country' or entity['type'] == 'Region' or entity['type'] == 'City' or entity['type'] == 'StateOrCountry' or entity['type'] == 'Continent':
                if entity.get('disambiguated'):
                    locations.append(entity['disambiguated']['name'])
                    relevance.append(entity['relevance'])
                else:
                    locations.append(entity['text'])
                    relevance.append(entity['relevance'])         
                print('text: ', entity['text']) # for testing
                print('type: ', entity['type']) # for testing
                print('relevance: ', entity['relevance']) # for testing
            else:
                locations.append('Not a Location')
                relevance.append('0.0')
        print('Here are the unfiltered nouns and their relevance')
        for item in locations:
            print(item)
        for item in relevance:
            print(item)
        if relevance:
            max_pos = relevance.index(max(relevance)) # get nth position of the highest relevancy score
            master_locations.append(locations[max_pos]) #Use n to get nth position of all location names and store that location name to master_locations
            locations[:] = []
            relevance[:] = []
    else:
        print('Error in entity extraction call: ', response['statusInfo'])
        master_locations.append('Pacific Ocean')


def google(address):
    #pdb.set_trace()
    for address in master_locations:
        try:
            search = geocoder.get(address)

        except ValueError:
            coordinates.append(['0', '0'])
            continue 

        first_result = search[0]
        output =  [ 
            first_result.geometry.location.lat, 
            first_result.geometry.location.lng, 
        ]
        coordinates.append(map(str, output))

# Entity Test

run_alchemy_entity_per_link('http://www.telesurtv.net/english/news/Leaks-Show-US-Planned-Espionage-to-Protect-Dominance-20140906-0009.html')

####TESTING MODULE####

print('Here is the final decided location')
for item in master_locations:
    print(item)

google(master_locations)
print(coordinates)
