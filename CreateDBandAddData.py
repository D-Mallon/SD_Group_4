import mysql.connector
import requests
import json


#Connect to MySQLServer
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="UCD22GRMA"
)

#Create DB if not already exists
mycursor = mydb.cursor()
try:
    mycursor.execute("CREATE DATABASE comp30830project")
    mycursor.execute("use comp30830project; CREATE TABLE DynamicBikeData (AvailableBike INT, Capacity INT, Status VARCHAR(255),Location VARCHAR(255))")
except:
    print("DataBase already exists")


#Dublin Bikes Data Pull
r = requests.get("https://api.jcdecaux.com/vls/v1/stations",
params={"apiKey":'cd0f042a0fe994456333c463ac937795b92de9eb',
"contract": "dublin"})
(json.loads(r.text))

response = requests.get("https://api.jcdecaux.com/vls/v1/stations/42?apiKey=cd0f042a0fe994456333c463ac937795b92de9eb&contract=dublin")
data = response.text
BikeData = json.loads(data)

for i in range(1,43):
    response = requests.get(f"https://api.jcdecaux.com/vls/v1/stations/{i}?apiKey=cd0f042a0fe994456333c463ac937795b92de9eb&contract=dublin")
    data = response.text
    data = json.loads(data)
    availableBikes = data['available_bikes']
    location = str(data['position']['lat'])+str(data['position']['lng'])
    capacity = data['bike_stands']
    status = data['status']

    sql = "INSERT INTO comp30830project.DynamicBikeData VALUES (%s,%s,%s,%s)" 
    val  = (availableBikes,capacity,status,location)

    mycursor.execute(sql,val)
    mydb.commit()
