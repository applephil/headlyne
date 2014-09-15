

from __future__ import print_function
from alchemyapi import AlchemyAPI
import json

demo_text = 'Yesterday dumb Bob destroyed my fancy iPhone in beautiful Denver, Colorado. I guess I will have to head over to the Apple Store and buy a new one.'
demo_url = 'http://www.npr.org/2013/11/26/247336038/dont-stuff-the-turkey-and-other-tips-from-americas-test-kitchen'
demo_html = '<html><head><title>Python Demo | AlchemyAPI</title></head><body><h1>Did you know that AlchemyAPI works on HTML?</h1><p>Well, you do now.</p></body></html>'
image_url = 'http://demo1.alchemyapi.com/images/vision/football.jpg'
reddit_url = 'http://www.reddit.com/r/worldnews'


#Create the AlchemyAPI Object
alchemyapi = AlchemyAPI()

locations = []

relevance = []

master_locations = []

response = alchemyapi.entities('url', reddit_url, {'sourceText':'xpath', 'xpath':'//*[contains(@class,"title may-blank")]' }) 

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

			print('text: ', entity['text']) # for testing

			print('type: ', entity['type']) # for testing

			print('relevance: ', entity['relevance']) # for testing

			print('type of relevance', type(currentRelevance))

		else:

			locations.append('Not a Location')

			relevance.append(0.0)

	print('Here are the unfiltered nouns and their relevance')

	it = 0

	for item in locations:
		print(item)
		print(relevance[it])
		it = it + 1
		print('')

	if relevance:

		max_pos = relevance.index(max(relevance)) # get nth position of the highest relevancy score

		master_locations.append(locations[max_pos]) #Use n to get nth position of all location names and store that location name to master_locations

else:

	print('Error in entity extraction call: ', response['statusInfo'])

	master_locations.append('Pacific Ocean')

print('the master location is');
for loc in master_locations:
	print(loc)
