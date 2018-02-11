from flask import Flask, render_template, request, flash, redirect,session
from app import app
import sqlite3
from random import randint

@app.route('/')
def index():
    return render_template("start.html")

@app.route('/home',  methods =['GET', 'POST'])
def home():
	if request.method == 'GET':
		if 'userid' in session:
			con = sqlite3.connect("Movie.db")
			cur = con.cursor()
			rows=cur.execute("select * from Movies limit 0, 10")
			return render_template("home.html", rows=rows)
		else:
			return redirect("http://localhost:5000/login")

@app.route('/movie/<movie_id>',  methods =['GET', 'POST'])
def movie(movie_id):
	if request.method == 'GET':
		if 'userid' in session:
			con = sqlite3.connect("Movie.db")
			cur = con.cursor()
			rows=cur.execute("select * from Movies where Id=%s;" % movie_id)
			con1=sqlite3.connect("database.db")
			cur1 = con1.cursor()
			cur2=con.cursor()
			recom=cur2.execute("select * from Movies order by 'Movie Title' limit %d, %d" % (randint(5,15),randint(30,50)))
			reviews=cur1.execute("select * from reviews where movieid=%s;" % movie_id)
			return render_template("movie.html",rows=rows,reviews=reviews,recom=recom,reviewform=reviewform())
		else:
			return redirect("http://localhost:5000/login")

	elif request.method == 'POST':
		if 'userid' in session:
			addreview(request.form['comments'],request.form['rate'],movie_id)
			con = sqlite3.connect("Movie.db")
			cur = con.cursor()
			rows=cur.execute("select * from Movies where Id=%s;" % movie_id)
			cur2=con.cursor()
			recom=cur2.execute("select * from Movies limit %d, %d" % (randint(10,15),randint(20,30)))
			con1=sqlite3.connect("database.db")
			cur1 = con1.cursor()
			reviews=cur1.execute("select * from reviews where movieid=%s;" % movie_id)
			return render_template("movie.html",rows=rows,reviews=reviews,recom=recom,reviewform=reviewform())
		else:
			return redirect("http://localhost:5000/login")




@app.route('/logout',  methods =['GET', 'POST'])
def logout():
	session.pop('userid',None)
	return render_template("start.html")

@app.route('/search',  methods =['GET', 'POST'])
def search():
	if request.method == 'POST':
		if 'userid' in session:
			con = sqlite3.connect("Movie.db")
			cur = con.cursor()
			if request.form['year']!="":
				rows=cur.execute("select * from Movies where [Release Date]= %s;" % request.form['year'])
			else:
				rows=cur.execute("select * from Movies where [Movie Title] like '%s';" % request.form['name'])
			return render_template("search.html",searchform=searchform(),rows=rows)
		else:
			return redirect("http://localhost:5000/login")
	else:
		return render_template("search.html",searchform=searchform())

@app.route('/profile',  methods =['GET', 'POST'])
def profile():
	if request.method == 'GET':
		if 'userid' in session:
			print ("\n\n\n\n\n\n",session['userid'])
			user_id = session['userid']
			con = sqlite3.connect("database.db")
			con1 = sqlite3.connect("database.db")
			cur = con.cursor()
			cur1 = con1.cursor()
			rows=cur1.execute("select * from reviews where userid='%s';" % user_id)
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

def addreview(cm,rt,mi):
	conn=sqlite3.connect('database.db')
	conn.execute("insert into reviews (movieid,userid,comments,ratings) values('%s','%s','%s','%s');" % (mi,session['userid'],cm,rt))
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

class reviewform(Form):
	comments = TextField("Comments: ")
	rate = RadioField('Rate: ', choices = [(2,'1'),(4,'2'),(6,'3'),(8,'4'),(10,'5')])
	def validate(self):
		return (True)


class searchform(Form):
	name = TextField("Movie title: ")
	year = TextField("Year: ")
	def validate(self):
		return (True)

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

