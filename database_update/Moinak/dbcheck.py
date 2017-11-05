import sqlite3
conn=sqlite3.connect('Movie.db')
cur=conn.execute('select * from Movies')
keys = [description[0] for description in cur.description]
print (keys,"\n\n")
for row in cur:
	print (row)
conn.commit()
conn.close()