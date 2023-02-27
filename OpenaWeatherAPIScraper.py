#Bones of a OpenWeather API Scraper - Matt
import requests
import json

url="https://api.openweathermap.org/data/2.5/weather?q=Dublin,IE&appid=648a779d29f9bffe54fe92440bd0a303"

req = requests.get(url)
data = json.loads(req.text)
print(data)
