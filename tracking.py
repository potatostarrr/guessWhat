from flask import Flask, redirect, url_for, session,render_template,flash, request
from flask_oauth import OAuth
from search import getsuggestions
from users import SignupForm, User,db, SigninForm, SignoutForm
import search
app = Flask(__name__)
app.config.from_object("config_")
db.init_app(app)



@app.route("/", methods = ['GET', 'POST'])
def index():
    getsuggestions(app.config["QUESTION"], app)
    signupform = SignupForm()
    signinform = SigninForm()
    signoutform = SignoutForm()
    if request.method == 'POST':
        if signupform.validate():
            newuser = User(signupform. register_username.data,  signupform.register_password.data)
            db.session.add(newuser)
            db.session.commit()
            session['score'] = newuser.score
            session['username'] = newuser.username
            return render_template("extend.html", question = app.config["QUESTION"], one = app.config['ONE'],
                               six = app.config['SIX'], order = app.config['ORDER'],signinform = signinform,
                                signoutform = signoutform, session = session)
        elif signinform.validate():
            user = User.query.filter_by(username = signinform.username.data.lower()).first()
            session['score'] = user.score
            session['username'] = user.username
            return render_template("extend.html", question = app.config["QUESTION"], one = app.config['ONE'],
                               six = app.config['SIX'], order = app.config['ORDER'], signinform = signinform,
                                  signoutform = signoutform, session = session)
        elif signoutform.validate_on_submit():
            session.pop("username", None)
            session.pop("score", None)
            return render_template("extend.html", question = app.config["QUESTION"], one = app.config['ONE'],
                               six = app.config['SIX'], order = app.config['ORDER'], signinform = signinform,
                                  signupform=signupform, session = session)
        else:
            temp = request.form['answer']
            if temp in app.config['ONE'] or temp in app.config['SIX']:
                if temp in app.config['ONE']:
                    order = app.config['ONE'].index(temp)
                elif temp in app.config['SIX']:
                    order = app.config['SIX'].index(temp)+5
                app.config['ORDER'].append(order)
                return render_template("extend.html", question = app.config["QUESTION"], one = app.config['ONE'],
                               six = app.config['SIX'], order = app.config['ORDER'],signinform = signinform,
                                  signupform=signupform, signoutform=signoutform)
            else:
                error = "Keep Trying!"
                return render_template("extend.html", question = app.config["QUESTION"], one = app.config['ONE'],
                               six = app.config['SIX'], error = error, order = app.config['ORDER'],
                                        signinform = signinform,
                                  signupform=signupform, signoutform=signoutform)



    return render_template("extend.html", question = app.config["QUESTION"], one = app.config['ONE'],
                           six = app.config['SIX'], signupform = signupform, signinform = signinform,
                            signoutform=signoutform, session = session)










if __name__ == "__main__":
    app.run()