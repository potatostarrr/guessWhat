from flask import Flask, redirect, url_for, session,render_template
from flask_oauth import OAuth



app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()