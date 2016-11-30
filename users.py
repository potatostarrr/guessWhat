from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, url_for, session,render_template,flash, request
from flask_wtf import Form
from wtforms import StringField,  SubmitField, ValidationError, PasswordField, validators
from werkzeug.security import generate_password_hash, check_password_hash



db = SQLAlchemy()

#create user class
class User(db.Model):
  #start with table name and all column should be dump into database
  __tablename__ = 'users'
  uid = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(100), unique = True)
  pwdhash = db.Column(db.String(54))
  score = db.Column(db.Integer)

  #initialnize
  def __init__(self, username, password):
    self.username = username.title()
    self.set_password(password)
    self.score = 0

  #we only store hashed password
  def set_password(self, password):
    self.pwdhash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)

#create sign up form
class SignupForm(Form):
  register_username = StringField("Username", [validators.DataRequired("Please enter your name.")])
  register_password = PasswordField('Password', [validators.DataRequired("Please enter a password.")])
  submit = SubmitField("Create account")
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
  # create validate function for this form
  def validate(self):
    if not Form.validate(self):
      print("1")
      return False
    if not Form.is_submitted(self):
        return False
    #select user from database
    user = User.query.filter_by(username = self.register_username.data.lower()).first()
    if user:
      self.register_username.errors.append("That email is already taken")
      return False
    else:
      return True

#create signinForm
class SigninForm(Form):
    username = StringField("Username", [validators.DataRequired("please enter your name")])
    password = PasswordField("Password", [validators.DataRequired("Please enter you password")])
    submit = SubmitField("Login")
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
    def validate(self):
        if not Form.validate(self):
            return False
        if not Form.is_submitted(self):
            return False
        user = User.query.filter_by(username = self.username.data.lower()).first()
        if user and user.check_password(self.password.data):
            return True
        return False

class SignoutForm(Form):
    submit = SubmitField("Signout")