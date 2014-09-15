
from googlegeocoder import GoogleGeocoder
geocoder = GoogleGeocoder()

list_of_addresses = [
	    '1727 E 107th St, Los Angeles, CA', 
	    '317 Broadway, Los Angeles, CA'
	]

coordinates = []

def google(address):
	
	for address in list_of_addresses:
	    try:
	        search = geocoder.get(address)
	    except ValueError:
	        continue
	    first_result = search[0]
	    output =  [ 
	        first_result.geometry.location.lat, 
	        first_result.geometry.location.lng, 
	    ]
	    coordinates.append(map(str, output))

google(list_of_addresses)
print(coordinates)