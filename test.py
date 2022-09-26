import requests
import json
import string

# response = requests.get("https://api.decentraland.org/v2/tiles?x1={}&y1={}&x2={}&y2={}".format(10,10,15,15))
response = requests.get('https://api.decentraland.org/v2/parcels/{}/{}'.format(-18, -118))

print(response.status_code)
# response -> json
print(response.json())
print('----------------------------------------------------------------------------------')
print('----------------------------------------------------------------------------------')
properties = json.loads(response.text)
print(properties)

