from flask import Flask, render_template, request, jsonify
import pymysql
from pymysql.cursors import DictCursor
from datetime import datetime, timedelta
import json
import logging

logging.basicConfig(level=logging.DEBUG)


app = Flask(__name__)

def get_dynamic_data():
    mydb_dynamic = pymysql.connect(
        host="",
        user="",
        password="",
        database="DBikeDynamicV2"
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

    dynamic_data = mycursor.fetchall()
    mycursor.close()
    mydb_dynamic.close()

    return dynamic_data

@app.route('/')
def main_page():
    dynamic_data = get_dynamic_data()

    return render_template('index.html', dynamic_data=dynamic_data)

# retrieves the bike station data from the DBikeStatic and DBikeDynamicV2 databases, merges the data into a list of dictionaries, and returns the data as a JSON response.
@app.route("/bike_stations")
def bike_stations():
    # Fetch the dynamic data
    dynamic_data = get_dynamic_data()

    # Fetch the static data
    mydb_static = pymysql.connect(
        host="",
        user="",
        password="",
        database="DBikeStatic"
    )

    mycursor = mydb_static.cursor(DictCursor)
    mycursor.execute("SELECT * FROM Stations")

    static_data = mycursor.fetchall()
    mycursor.close()
    mydb_static.close()

    # Merge the static and dynamic data into a single list
    bike_data = []
    for static_station, dynamic_station in zip(static_data, dynamic_data):
        bike_data.append({
            "number": static_station["Number"],
            "name": static_station["Name"],
            "latitude": static_station["Latitude"],
            "longitude": static_station["Longitude"],
            "capacity": dynamic_station["Capacity"],
            "available_bikes": dynamic_station["AvailableBike"],
            "status": dynamic_station["Status"],
            "banking": static_station["Banking"]
        })

    # Return the data as JSON
    return jsonify(bike_data)

# retrieves data for the specified bike station from the DBikeDynamicV2 database and returns the data as a JSON response.
@app.route('/station_data/<int:station_id>')
def station_data(station_id):
    # Connect to the dynamic database
    mydb = pymysql.connect(
        host="",
        user="",
        password="",
        database="DBikeDynamicV2"
    )

    mycursor = mydb.cursor(DictCursor)

    def get_hourly_availability_data(station_id, day_start, day_end):
        mycursor.execute("""
            SELECT HOUR(DateTime) AS Hour, AVG(AvailableBike) AS AverageAvailableBike
            FROM Dynamic
            WHERE ID = %s AND DateTime >= %s AND DateTime <= %s
            GROUP BY HOUR(DateTime)
            ORDER BY Hour
        """, (station_id, day_start, day_end))

        data = mycursor.fetchall()

        labels = [f"{x['Hour']:02d}:00" for x in data]
        values = [x["AverageAvailableBike"] for x in data]

        # trialling new time format. Commented out version shows times in 1,8,14,20 format instead of 14:00 for example. Can return to this point when we're dressing up the site.
        # labels = [x["Hour"] for x in data]
        # values = [x["AverageAvailableBike"] for x in data]

        return {"labels": labels, "data": values}

    now = datetime.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = now
    yesterday_start = today_start - timedelta(days=1)
    yesterday_end = today_start - timedelta(seconds=1)
    day_before_yesterday_start = yesterday_start - timedelta(days=1)
    day_before_yesterday_end = yesterday_start - timedelta(seconds=1)

    today_data = get_hourly_availability_data(station_id, today_start, today_end)
    yesterday_data = get_hourly_availability_data(station_id, yesterday_start, yesterday_end)
    day_before_yesterday_data = get_hourly_availability_data(station_id, day_before_yesterday_start, day_before_yesterday_end)

    mycursor.close()
    mydb.close()

    return jsonify({
        "today": today_data,
        "yesterday": yesterday_data,
        "dayBeforeYesterday": day_before_yesterday_data,
    })


@app.route('/average_station_data/<int:station_number>', methods=['GET'])
def average_station_data(station_number):
    # Connect to the dynamic database
    mydb = pymysql.connect(
        host="",
        user="",
        password="",
        database="DBikeDynamicV2"
    )

    cur = mydb.cursor(DictCursor)

    # Get the current day of the week (0 = Monday, 1 = Tuesday, etc.)
    current_day = datetime.today().weekday()

    query = '''
    SELECT HOUR(DateTime) AS hour, AVG(AvailableBike) as avg_available_bikes
    FROM Dynamic
    WHERE ID = %s AND WEEKDAY(DateTime) = %s
    GROUP BY hour
    ORDER BY hour
    '''

    cur.execute(query, (station_number, current_day))
    results = cur.fetchall()

    cur.close()
    mydb.close()

    # Convert the results to the format expected by the chart
    labels = []
    data = []
    for row in results:
        hour = row["hour"]
        avg_available_bikes = row["avg_available_bikes"]
        labels.append(f"{int(hour)}:00")
        data.append(avg_available_bikes)

    return jsonify({"labels": labels, "data": data})







if __name__ == '__main__':
    app.run(debug=True)

