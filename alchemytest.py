from alchemyapi import AlchemyAPI
import json

alchemyapi = AlchemyAPI()

article_list = []

def run_alchemy_api(articleurl):
    response = alchemyapi.entities('url',articleurl, { 'showSourceText':1, 'sourceText':'xpath', 'xpath':'//*[contains(@class,"title may-blank")][1]' })
    if response['status'] == 'OK':
        print('This is the decode test,')
        print(response['text']) # <---- this is what I want to organize into a list
        text = response['text']
        titles = text.split('\n\n')
        article_list.append(titles)

    else:
        print('Error in entity extraction call: ', response['statusInfo'])

run_alchemy_api('http://www.reddit.com/r/worldnews/')
print article_list