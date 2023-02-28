import requests
import json
r = requests.get("https://api.jcdecaux.com/vls/v1/stations",
params={"apiKey":'cd0f042a0fe994456333c463ac937795b92de9eb',
"contract": "dublin"})
(json.loads(r.text))


response = requests.get("https://api.jcdecaux.com/vls/v1/stations/42?apiKey=cd0f042a0fe994456333c463ac937795b92de9eb&contract=dublin")
data = response.text
data = json.loads(data)
print(data)