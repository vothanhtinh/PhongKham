from saleapp import app
from flask import render_template


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/introduce")
def introduce():
    return render_template("introduce.html")
@app.route("/booking")
def booking():
    return render_template("booking.html")
@app.route("/login")
def login():
    return render_template("login.html")


if __name__=="__main__":
    app.run(debug=True)