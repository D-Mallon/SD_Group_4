import requests
import json
import mysql.connector
import datetime

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

#creates initial db
sqldb = """
CREATE DATABASE IF NOT EXISTS openweatherapi;
"""

mycursor.execute(sqldb)
mydb.commit()
mycursor.close()
mydb.close()

#recconects with proper db
mydb = mysql.connector.connect(
host = "",
user="",
password = "",
database = "openweatherapi")
mycursor = mydb.cursor()

#creates tables in db
sqltables = """
CREATE TABLE IF NOT EXISTS Weather(
Main VARCHAR(256),
Temp FLOAT(24),
Humidity FLOAT(24),
WindSpeed FLOAT(24),
DateTime DATETIME
);
"""
mycursor.execute(sqltables)

#varaibles
main = weatherdata.get("weather")[0].get("main")
temp = weatherdata.get("main").get("temp")
humidity = weatherdata.get("main").get("humidity")
wind = weatherdata.get("wind").get("speed")
datetime = datetime.datetime.now()
print(main)
print(temp)
print(humidity)
print(wind)
print(datetime)

#inserts varaibles into openweather table
sqlupdate = """
INSERT INTO Weather (Main, Temp, Humidity, WindSpeed, Datetime) 
VALUES (%s,%s,%s,%s,%s)
"""

val = (main, temp, humidity, wind, datetime)

mycursor.execute(sqlupdate, val)
mydb.commit()
print(f"Added {mycursor.rowcount} row of data")
mycursor.close()
mydb.close()
