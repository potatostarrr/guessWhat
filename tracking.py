from flask import Flask, url_for, session,render_template,flash, request
from users import SignupForm, User,db, SigninForm, SignoutForm
app = Flask(__name__)
app.config.from_object("config_")
db.init_app(app)



@app.route("/", methods = ['GET', 'POST'])
def index():
    signupform = SignupForm()
    signinform = SigninForm()
    signoutform = SignoutForm()
    session['score'] = 0
    if request.method == 'POST':
        if signupform.validate():
            newuser = User(signupform. register_username.data,  signupform.register_password.data)
            db.session.add(newuser)
            db.session.commit()
            session['score'] = newuser.score
            session['username'] = newuser.username
            return render_template("extend.html", question = app.config["QUESTION"], order = app.config['ORDER'],
                                signoutform = signoutform, session = session)

        elif signinform.validate():
            user = User.query.filter_by(username = signinform.username.data.lower()).first()
            session['score'] = user.score
            session['username'] = user.username
            return render_template("extend.html", question = app.config["QUESTION"], order = app.config['ORDER'],
                                  signoutform = signoutform, session = session)
        elif signoutform.validate_on_submit():
            session.pop("username", None)
            session['score'] = 0
            return render_template("extend.html", question = app.config["QUESTION"],order = app.config['ORDER'], signinform = signinform,
                                  signupform=signupform, session = session)
    return render_template("extend.html", question = app.config["QUESTION"], signupform = signupform, signinform = signinform,
                            session = session, signoutform = signoutform)










if __name__ == "__main__":
    app.run()