from __future__ import print_function
from alchemyapi import AlchemyAPI
import json
import time
import pprint
import urllib2
from bs4 import BeautifulSoup
from googlegeocoder import GoogleGeocoder

alchemyapi = AlchemyAPI()
geocoder = GoogleGeocoder()
reddit_url = 'http://www.reddit.com/r/worldnews'
article_list = []
urls = []
locations = []
relevance = []
master_locations = []
coordinates = []

def run_alchemy_title(articleurl):
    response = alchemyapi.entities('url', articleurl, { 'showSourceText':1, 'sourceText':'xpath', 'xpath':'//*[contains(@class,"title may-blank")][1]' })
    if response['status'] == 'OK':
        text = response['text']
        titles = text.split('\n\n')
        article_list.append(titles)
        print('')
    else:
        print('Error in entity extraction call: ', response['statusInfo'])

def google(address):
    for item in address:
        try:
            search = geocoder.get(item)
            first_result = search[0]
            output =  [ 
                first_result.geometry.location.lat, 
                first_result.geometry.location.lng, 
            ]
            output_unicode = unicode(output)
            coordinates.append(output_unicode)
            time.sleep(0.1)

        except ValueError:
            error_address = ['0', '0']
            error_address_unicode = unicode(error_address)
            coordinates.append(error_address_unicode)
            time.sleep(0.1)
            continue 

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
            else:
                else_message = 'Not a Location'
                not_location_unicode = unicode(else_message)
                locations.append(not_location_unicode)
                relevance.append('0.0')
        if relevance:
            max_pos = relevance.index(max(relevance)) 
            master_locations.append(locations[max_pos]) 
            locations[:] = []
            relevance[:] = []
    else:
        print('Error in entity extraction call: ', response['statusInfo'])
        neutral_location = 'Pacific Ocean'
        neutral_location_decoded = unicode(neutral_location)
        master_locations.append(neutral_location_decoded)

def get_all_links(page):
    html = urllib2.urlopen(page).read()
    soup = BeautifulSoup(html)
    for a in soup.find_all('a', 'title may-blank ', href=True):
        urls.append(a['href'])
        run_alchemy_entity_per_link(a['href'])

run_alchemy_title(reddit_url) 
get_all_links(reddit_url) 
google(master_locations)

return article_list, urls, coordinates

