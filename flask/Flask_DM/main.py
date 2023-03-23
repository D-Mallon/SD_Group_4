from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route("/<name>")
def home(name):
    return render_template("index.html", content=["Tim", "Bob", "Joe"])



# @app.route("/<name>")
# def user(name):
#     return f"Hello {name}!"

if __name__ == "__main__":
    app.run(debug = True)