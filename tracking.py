from flask import Flask, redirect, url_for, session,render_template,flash, request
from flask_oauth import OAuth
import requests, json
import unicodedata
QUESTION = "i love my"
ONE = []
SIX = []
app = Flask(__name__)
app.config.from_object(__name__)

def getsuggestions(question):
    URL = "http://suggestqueries.google.com/complete/search?client=firefox&q=" + app.config["QUESTION"]
    headers = {'User-agent':'Mozilla/5.0'}
    response = requests.get(URL, headers=headers)
    result = json.loads(response.content.decode('utf-8'))
    if len(result[1])> 5:
         six = [unicodedata.normalize('NFKD', i).encode('ascii','ignore').replace("i love my", "").lstrip() \
                for i in result[1][5:]]
         app.config['SIX'] = six
    one = [unicodedata.normalize('NFKD', i).encode('ascii','ignore').replace("i love my", "").lstrip() \
                for i in result[1][:5]]
    app.config['ONE'] = one

@app.route("/", methods = ['GET', 'POST'])
def index():
    getsuggestions(app.config["QUESTION"])
    if request.method == 'POST':
        temp = request.form['answer']
        if temp in app.config['ONE'] or temp in app.config['SIX']:
            if temp in app.config['ONE']:
                order = app.config['ONE'].index(temp)+1
            elif temp in app.config['SIX']:
                order = app.config['ONE'].index(temp)+6
            return render_template("index.html", question = app.config["QUESTION"], one = app.config['ONE'],
                           six = app.config['SIX'], order = order)
        else:
            error = "Keep Trying!"
            return render_template("index.html", question = app.config["QUESTION"], one = app.config['ONE'],
                           six = app.config['SIX'], error = error)



    return render_template("index.html", question = app.config["QUESTION"], one = app.config['ONE'],
                           six = app.config['SIX'])






if __name__ == "__main__":
    app.run()