from flask import Flask, render_template
import pymysql
from pymysql.cursors import DictCursor


app = Flask(__name__)

# see if this will cause issues. We are calling one database for static and another for the dynamic. A third will be required for the weather. Should these all be moved into the one db?

def get_dynamic_data():
    mydb_dynamic = pymysql.connect(
        host="",
        user="",
        password="",
        database=""
    )

    mycursor = mydb_dynamic.cursor(DictCursor)
    mycursor.execute("""
        SELECT *
        FROM Dynamic
        WHERE (ID, DateTime) IN (
            SELECT ID, MAX(DateTime)
            FROM Dynamic
            GROUP BY ID
        )
    """)
    data = mycursor.fetchall()
    mycursor.close()
    mydb_dynamic.close()

    return {row['ID']: row for row in data}

def get_bike_data():
    static_rows = get_static_data()
    dynamic_data = get_dynamic_data()
    bike_data = []

    for row in static_rows:
        station_dynamic_data = dynamic_data[row[0]]
        bike_data.append({
            'number': row[0],
            'name': row[1],
            'latitude': float(row[2]),
            'longitude': float(row[3]),
            'available_bikes': station_dynamic_data['AvailableBike'],
            'capacity': station_dynamic_data['Capacity']
        })

    return bike_data

def get_static_data():
    mydb_static = pymysql.connect(
        host="",
        user="",
        password="",
        database=""
    )

    mycursor = mydb_static.cursor()
    mycursor.execute("SELECT * FROM Stations")
    rows = mycursor.fetchall()
    mycursor.close()
    mydb_static.close()

    return rows



@app.route('/')
def index():
    bike_data = get_bike_data()
    return render_template("index.html", bike_data=bike_data)

if __name__ == '__main__':
    app.run(debug=True)
