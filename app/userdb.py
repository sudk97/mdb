import sqlite3
conn=sqlite3.connect('database.db')
conn.execute('create table users (userid integer primary key autoincrement,first_name text, last_name text, email text,password text);')
conn.commit()
conn.execute('create table reviews(revid integer primary key autoincrement,movietitle text, userid integer, comments text,ratings real);')
conn.commit()
conn.close()