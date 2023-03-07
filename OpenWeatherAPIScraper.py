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

#creates initial tables in the db
sqltables = """
CREATE DATABASE IF NOT EXISTS openweatherapi;
USE openweatherapi;
CREATE TABLE IF NOT EXISTS Weather(
Main VARCHAR(256),
Temp FLOAT(24),
Humidity FLOAT(24),
WindSpeed FLOAT(24),
DateTime DATE
)
"""
mycursor.execute(sqltables, multi=True)

#varaibles
main = weatherdata.get("weather")[0].get("main")
temp = weatherdata.get("main").get("temp")
humidity = weatherdata.get("main").get("humidity")
wind = weatherdata.get("wind").get("speed")
datetime = date.today()

#inserts varaibles into openweather table
sqlupdate = f"""
USE openweatherapi;
INSERT INTO Weather (
Main,
Temp,
Humidity,
WindSpeed,
DateTime
)
VALUES (
{main},
{temp},
{humidity},
{wind},
{datetime}
)
"""

mycursor.execute(sqlupdate, multi=True)
mydb.commit()
print(mycursor.rowcount)
