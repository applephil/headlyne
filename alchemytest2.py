from __future__ import print_function
from alchemyapi import AlchemyAPI
import json

alchemyapi = AlchemyAPI()
reddit_url = 'http://www.reddit.com/r/worldnews'
article_list = []
urls = []
locations = []
relevance = []
master_locations = []
geocodes = []

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
                #print('text: ', entity['text']) # for testing
                #print('type: ', entity['type']) # for testing
                #print('relevance: ', entity['relevance']) # for testing
                #if 'score' in entity['sentiment']:
                    #print('sentiment score: ' + entity['sentiment']['score'])
                    #print('')
            else:
                locations.append('No Location')
                relevance.append('0')
    else:
        print('Error in entity extraction call: ', response['statusInfo'])
    
    print('')
    print('SCIENCE BITCHES')
    print(relevance)
    #max_pos = relevance.index(max(relevance)) # get nth position of the highest relevancy score
    #print('')
    #master_locations.append(locations[max_pos]) #Use n to get nth position of location and store that location name to master_locations

run_alchemy_entity_per_link('http://www.ibtimes.co.uk/dutch-politician-geert-wilders-if-youre-waving-isis-flag-youre-waving-exit-ticket-leave-1464224/')

for item in locations:
    print(item)

for item in relevance:
    print(item)

for item in master_locations:
    print(item)