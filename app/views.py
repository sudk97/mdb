from flask import Flask, render_template, request, flash, redirect,session
from app import app
import sqlite3
@app.route('/')
def index():
    return render_template("start.html")

@app.route('/home',  methods =['GET', 'POST'])
def home():
	if request.method == 'GET':
		con = sqlite3.connect("Movie.db")
		cur = con.cursor()
		rows=cur.execute("select * from Movies limit 0, 10")
		return render_template("home.html", rows=rows)


@app.route('/profile',  methods =['GET', 'POST'])
def profile():
	if request.method == 'GET':
		if 'userid' in session:
			print ("\n\n\n\n\n\n",session['userid'])
			user_id = session['userid']
			con = sqlite3.connect("database.db")
			cur = con.cursor()
			rows=cur.execute("select * from reviews where userid='%s';" % user_id)
			userdetails=cur.execute("select * from users where userid='%s';" % user_id)
			return render_template("profile.html", rows=rows, userdetails=userdetails)
		else:
			return redirect("http://localhost:5000/login")

@app.route('/login' , methods =['GET', 'POST'])
def login():
	lform=loginform()
	rform=registerform()

	if request.method == 'POST':
		if request.form['submit']=="Log In":
			if lform.validate() == False:
				flash("Invalid Input")
				return redirect("http://localhost:5000/login")
			else:


				if check(request.form['eid'],request.form['pwd'])==True:
					conn=sqlite3.connect('database.db')
					cur=conn.execute("select userid from users where email='%s';" % request.form['eid'])
					for r in cur:
						session['userid']= r[0]
						break
					print ("\n\n\n\n\n\n",session['userid'])
					return redirect("http://localhost:5000/home")
				else:
					flash("Invalid Input")
					return redirect("http://localhost:5000/login")

		else:
			if rform.validate() == False:
				flash("Invalid Input")
				return redirect("http://localhost:5000/login")
			else:
				try:
					register(request.form['firstname'],request.form['lastname'],request.form['email'],request.form['password'])
					flash("Registration Successful ! Log In to continue")
					return redirect("http://localhost:5000/login")
				except Exception as ex:
					flash("Sorry, there was an error. Try again. " + str(ex))
					return redirect("http://localhost:5000/login")
				
	elif request.method == 'GET':
		return render_template('login.html', loginform = loginform(), registerform=registerform())


def register(fn,ln,en,pd):
	conn=sqlite3.connect('database.db')
	conn.execute("insert into users (first_name,last_name,email,password) values('%s','%s','%s','%s');" % (fn,ln,en,pd))
	conn.commit()
	conn.close()
	return

def check(en,pd):
	conn=sqlite3.connect('database.db')
	cur=conn.execute("select email,password from users;")
	for row in cur:
		if en==row[0]:
			if pd==row[1]:
				conn.close()
				return True
			else:
				conn.close()
				return False
	conn.close()

from flask_wtf import Form
import re
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField, PasswordField
from wtforms import validators, ValidationError

class loginform(Form):
	eid = TextField("Email Address*")
	pwd = PasswordField("Password*")

	def validate(self):
		match=re.match( r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', self.eid.data)
		print (match,self.eid.data)
		valpass=True
		if match==None:
			match=False
		else:
			match=True
		if len(self.pwd.data)<5:
			valpass=False
		return (match & valpass)


class registerform(Form):
	firstname = TextField("First Name*")
	lastname = TextField("Last Name*")
	email = TextField("Email Address*")
	password = PasswordField("Password*")
	submit = SubmitField("Register")
	def validate(self):
		match=re.search(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', self.email.data)
		res = super(registerform, self).validate()
		valpass=True
		if match==None:
			match=False
		else:
			match=True
		if len(self.password.data)<5:
			valpass=False
		return ( match & valpass)

