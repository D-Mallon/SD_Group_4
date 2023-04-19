import mysql.connector
import requests
import json
import datetime
import configparser

config = configparser.ConfigParser()
#config.read('/home/ubuntu/git/SD_Group_4/config.ini')
config.read('/Users/dmallon/Desktop/GitHubRepositories/SD_Group_4/config.ini')

db_host = config.get('Database', 'db_host')
db_user = config.get('Database', 'db_user')
db_password = config.get('Database', 'db_password')
db_database_static = config.get('Database', 'staticDatabase')
db_database_dynamic = config.get('Database', 'dynamicDatabase')
bike_api = config.get('api_keys', 'bike_api')

#connects and creates database if not exists. 
try:
    mydb = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password
    )
    mycursor = mydb.cursor()

    #create db if not exists
    sqldb = """
    CREATE DATABASE IF NOT EXISTS DBikeDynamicV2;
    """
    mycursor.execute(sqldb)
    mydb.commit()
    mycursor.close()
    mydb.close() 
except:
   print('Database already exists')



#Connect to MySQLServer with proper db
mydb = mysql.connector.connect(
  host=db_host,
  user=db_user,
  password=db_password,
  database="DBikeDynamicV2"
)
mycursor = mydb.cursor()

#create table if not exists
try:
    sqltable = """
    CREATE TABLE IF NOT EXISTS Dynamic (
    ID INT, 
    AvailableBike INT, 
    Capacity INT, 
    Status VARCHAR(255), 
    Latitude FLOAT(53), 
    Longitude FLOAT(53),
    DateTime DATETIME);
    """
    mycursor.execute(sqltable)
    mydb.commit()
except:
    print("Table already exists")


numls = [42, 30, 54, 108, 20, 56, 6, 18, 32, 52, 48, 13, 43, 31, 98, 14, 1, 23, 106, 
112, 68, 74, 87, 84, 90, 11, 17, 45, 114, 72, 63, 113, 91, 99, 9, 67, 116, 55, 62, 5, 97, 61, 77, 73, 4, 49, 19, 7, 60, 102, 38, 53, 58, 66, 104, 101, 115, 47, 117, 8, 27, 16, 96, 82, 76, 71, 79, 69, 25, 51, 37, 59, 95, 94, 105, 36, 93, 22, 50, 110, 12, 34, 78, 2, 75, 111, 26, 65, 15, 86, 35, 10, 100, 24, 64, 109, 85, 107, 33, 44, 89, 57, 80, 41, 3, 40, 29, 103, 28, 39, 83, 92, 21, 
88]

for i in numls:
    response = requests.get(f"https://api.jcdecaux.com/vls/v1/stations/{i}?apiKey={bike_api}&contract=dublin")
    data = response.text
    data = json.loads(data)
    availableBikes = data['available_bikes']
    lat = data['position']['lat']
    lon = data['position']['lng']
    capacity = data['bike_stands']
    status = data['status']
    id = data['number']
    date = datetime.datetime.now()
    sql = """
    INSERT INTO Dynamic
    VALUES (%s,%s,%s,%s,%s,%s,%s);
    """ 
    val  = (id,availableBikes,capacity,status,lat,lon,date)

    mycursor.execute(sql,val)
    print(f"Added {mycursor.rowcount} row of data")
    mydb.commit()

mycursor.close()
mydb.close()    
