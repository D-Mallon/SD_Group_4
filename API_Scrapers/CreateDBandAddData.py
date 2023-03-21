import mysql.connector
import requests
import json
import datetime

#Connect to MySQLServer
mydb = mysql.connector.connect(
  host="dbdatabase.csgc5rg5crt4.us-east-1.rds.amazonaws.com",
  user="admin",
  password="COMP30830Group4!"
)

#Create DB if not already exists
mycursor = mydb.cursor()
try:
  mycursor.execute("CREATE DATABASE DBikeDynamic")
  mycursor.execute("use DBikeDynamic; CREATE TABLE DynamicBikeData (ID INT, AvailableBike INT, Capacity INT, Status VARCHAR(255),Location VARCHAR(255),DateTime DATETIME)")
except:
   print('Database already exists')

numls = [42, 30, 54, 108, 20, 56, 6, 18, 32, 52, 48, 13, 43, 31, 98, 14, 1, 23, 106, 
112, 68, 74, 87, 84, 90, 11, 17, 45, 114, 72, 63, 113, 91, 99, 9, 67, 116, 55, 62, 5, 97, 61, 77, 73, 4, 49, 19, 7, 60, 102, 38, 53, 58, 66, 104, 101, 115, 47, 117, 8, 27, 16, 96, 82, 76, 71, 79, 69, 25, 51, 37, 59, 95, 94, 105, 36, 93, 22, 50, 110, 12, 34, 78, 2, 75, 111, 26, 65, 15, 86, 35, 10, 100, 24, 64, 109, 85, 107, 33, 44, 89, 57, 80, 41, 3, 40, 29, 103, 28, 39, 83, 92, 21, 
88]

for i in numls:
    response = requests.get(f"https://api.jcdecaux.com/vls/v1/stations/{i}?apiKey=cd0f042a0fe994456333c463ac937795b92de9eb&contract=dublin")
    data = response.text
    data = json.loads(data)
    availableBikes = data['available_bikes']
    location = str(data['position']['lat'])+str(data['position']['lng'])
    capacity = data['bike_stands']
    status = data['status']
    id = data['number']
    date = datetime.datetime.now()
    sql = "INSERT INTO DBikeDynamic.DynamicBikeData VALUES (%s,%s,%s,%s,%s,%s)" 
    val  = (id,availableBikes,capacity,status,location,date)

    mycursor.execute(sql,val,multi=True)
    mydb.commit()
