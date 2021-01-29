import requests
import pprint

details_url = 'https://maps.googleapis.com/maps/api/place/details/json'
params = {
    'key': "AIzaSyDddVDWwqLQWv0lnZbEAD6Up9SF2EYH-6I",
    'place_id': "ChIJs39O21L_3IkRlCHtdxLUhUc",
    'fields': "formatted_address,geometry,place_id,name,vicinity"
} 


response = requests.get(details_url, params).json()
pprint.pprint(response)