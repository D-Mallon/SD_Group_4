from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# Connect to the database
mydb = mysql.connector.connect(
  host="",
  user="",
  password="",
  database=""
)

# Define a route to display the data
@app.route("/")
def index():
    # Retrieve the data from the database
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Stations")
    data = mycursor.fetchall()
    mycursor.close()

    # Pass the data to the template and render it
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
