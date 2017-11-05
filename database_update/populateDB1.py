import sqlite3

conn=sqlite3.connect('PMDB.db')
cur=conn.cursor()

"""
cur.execute('''CREATE TABLE MOVIES ( 
	ID TEXT PRIMARY KEY NOT NULL,
	MOVIE_TITLE TEXT,
	ACTOR_1_FBLIKES TEXT,
	ACTOR_2_FBLIKES TEXT,
	ACTOR_3_FBLIKES TEXT,
	CAST_TOTAL_FBLIKES TEXT,
	MOVIE_FBLIKES TEXT,
	DIRECTOR_FBLIKES TEXT,
	ACTOR_1_NAME TEXT,
	ACTOR_2_NAME TEXT,
	ACTOR_3_NAME TEXT,
	DIRECTOR_NAME TEXT,
	NUM_VOTES TEXT,
	TITLE_YEAR TEXT,
	FACENUM TEXT,
	BUDGET TEXT,
	GROSS TEXT,
	CONTENT_RATING TEXT,
	NUM_CRITICS_REVIEWS TEXT,
	NUM_USERS_REVIEWS TEXT,
	PLOT_KEYWORDS TEXT,
	ASPECT_RATIO TEXT,
	MOVIE_LINK TEXT,
	COUNTRY TEXT,
	COLOR TEXT,
	DURATION TEXT,
	LANGUAGE TEXT,
	IMDB_SCORE TEXT,
	GENRES TEXT
	);''')
"""
conn.commit()
i=0


with open('movie_metadata.csv', 'rt', encoding='utf-8') as csvfile:
	reader = csvfile.readlines()
	reader=[x.strip() for x in reader]
	for line in reader:
		if i==0:
			i+=1
			continue
		try:
			row=line.split(',')
			cur.execute("INSERT INTO MOVIES( ID,\
			COLOR,\
			DIRECTOR_NAME,\
			NUM_CRITICS_REVIEWS,\
			DURATION,\
			DIRECTOR_FBLIKES,\
			ACTOR_3_FBLIKES,\
			ACTOR_2_NAME,\
			ACTOR_1_FBLIKES,\
			GROSS,\
			GENRES,\
			ACTOR_1_NAME,\
			MOVIE_TITLE,\
			NUM_VOTES,\
			CAST_TOTAL_FBLIKES,\
			ACTOR_3_NAME,\
			FACENUM,\
			PLOT_KEYWORDS,\
			MOVIE_LINK,\
			NUM_USERS_REVIEWS,\
			LANGUAGE,\
			COUNTRY,\
			CONTENT_RATING,\
			BUDGET,\
			TITLE_YEAR,\
			ACTOR_2_FBLIKES,\
			IMDB_SCORE,\
			ASPECT_RATIO,\
			MOVIE_FBLIKES\
			) \
			VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);" % i,tuple(row))
			i+=1
		except Exception as ex:
			print("Error",ex)
conn.close()