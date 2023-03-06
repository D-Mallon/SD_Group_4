import requests
import json
import mysql.connector

#Connector information for main RDS database
mydb = mysql.connector.connect(
host = "",
user="",
password = "")
mycursor = mydb.cursor()

#Openweather API connection and loading data
weatherurl="https://api.openweathermap.org/data/2.5/weather?q=Dublin,IE&appid=648a779d29f9bffe54fe92440bd0a303"
weatherreq = requests.get(weatherurl)
weatherdata = json.loads(weatherreq.text)

mycursor.execute("Insert sql")
