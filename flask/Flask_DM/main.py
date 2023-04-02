from flask import Flask, render_template
import pymysql
from pymysql.cursors import DictCursor


app = Flask(__name__)

# see if this will cause issues. We are calling one database for static and another for the dynamic. A third will be required for the weather. Should these all be moved into the one db?

def get_dynamic_data(station_id):
    mydb_dynamic = pymysql.connect(
        host="",
        user="",
        password="",
        database="DBikeDynamicV2"
    )

    mycursor = mydb_dynamic.cursor()
    mycursor.execute(f"SELECT * FROM Dynamic WHERE ID = {station_id} ORDER BY DateTime DESC LIMIT 1")
    data = mycursor.fetchone()
    mycursor.close()
    mydb_dynamic.close()

    return data

def get_static_data():
    mydb_static = pymysql.connect(
        host="",
        user="",
        password="",
        database="DBikeStatic"
    )

    mycursor = mydb_static.cursor()
    mycursor.execute("SELECT * FROM Stations")
    rows = mycursor.fetchall()
    mycursor.close()
    mydb_static.close()

    return rows

def get_bike_data():
    static_rows = get_static_data()
    bike_data = []

    for row in static_rows:
        dynamic_data = get_dynamic_data(row[0])
        bike_data.append({
            'number': row[0],
            'name': row[1],
            'latitude': float(row[2]),
            'longitude': float(row[3]),
            'available_bikes': dynamic_data[1],
            'capacity': dynamic_data[2]
        })

    return bike_data



@app.route('/')
def index():
    bike_data = get_bike_data()
    return render_template("index.html", bike_data=bike_data)

if __name__ == '__main__':
    app.run(debug=True)
