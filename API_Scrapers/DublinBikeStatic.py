import requests
import json
import mysql.connector
import configparser

config = configparser.ConfigParser()
#config.read('/home/ubuntu/git/SD_Group_4/config.ini')
config.read('/Users/eoin/Documents/GitHub/SD_Group_4/config.ini')

google_maps_api_key = config.get('api_keys', 'GOOGLE_MAPS_API_KEY')
db_host = config.get('Database', 'db_host')
db_user = config.get('Database', 'db_user')
db_password = config.get('Database', 'db_password')
db_database_static = config.get('Database', 'staticDatabase')
db_database_dynamic = config.get('Database', 'dynamicDatabase')
bike_api = config.get('api_keys', 'bike_api')


#"https://api.jcdecaux.com/vls/v1/stations",
#"apiKey":'',
#"contract": "dublin"})

#station numbers for dublin
numls = [42, 30, 54, 108, 20, 56, 6, 18, 32, 52, 48, 13, 43, 31, 98, 14, 1, 23, 106, 
112, 68, 74, 87, 84, 90, 11, 17, 45, 114, 72, 63, 113, 91, 99, 9, 67, 116, 55, 62, 5, 97, 61, 77, 73, 4, 49, 19, 7, 60, 102, 38, 53, 58, 66, 104, 101, 115, 47, 117, 8, 27, 16, 96, 82, 76, 71, 79, 69, 25, 51, 37, 59, 95, 94, 105, 36, 93, 22, 50, 110, 12, 34, 78, 2, 75, 111, 26, 65, 15, 86, 35, 10, 100, 24, 64, 109, 85, 107, 33, 44, 89, 57, 80, 41, 3, 40, 29, 103, 28, 39, 83, 92, 21, 
88]

#Connector information for main RDS database
mydb = mysql.connector.connect(
host = db_host,
user= db_user,
password = db_password)
mycursor = mydb.cursor()

#creates initial db
sqldb = """
CREATE DATABASE IF NOT EXISTS DBikeStatic;
"""

mycursor.execute(sqldb)
mydb.commit()
mycursor.close()
mydb.close()

#recconects with proper db
mydb = mysql.connector.connect(
host = db_host,
user=db_user,
password = db_password,
database = "DBikeStatic")
mycursor = mydb.cursor()

#creates tables in dbikestatic
sqltables = """
CREATE TABLE IF NOT EXISTS Stations(
Number INT,
Name VARCHAR(256),
Latitude FLOAT(53),
Longitude FLOAT(53),
Banking BOOLEAN
);
"""
mycursor.execute(sqltables)

#Clears table to prep for refresh on static data
sqldel = """
TRUNCATE TABLE Stations;
"""

mycursor.execute(sqldel)


#Iterates through list of station numbers, retreives data and uploads to table
for item in numls:

    res = requests.get(f"https://api.jcdecaux.com/vls/v1/stations/{item}?apiKey={bike_api}&contract=dublin")
    data = json.loads(res.text)
    
    number = data.get('number')
    name = data.get('name')
    lat = data.get('position').get('lat')
    lon = data.get('position').get('lng')
    banking = data.get('banking')

    sqlupdate = """
    INSERT INTO Stations (Number, Name, Latitude, Longitude, Banking)
    VALUES (%s,%s,%s,%s,%s);
    """
    val = (number, name, lat, lon, banking)

    mycursor.execute(sqlupdate, val)
    print(f"Added {mycursor.rowcount} row of data")

mydb.commit()
mycursor.close()
mydb.close()
