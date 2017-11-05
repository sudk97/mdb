import csv,sqlite3
conn=sqlite3.connect('PMDB.db')
cur=conn.cursor()
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
conn.commit()
i=1


with open('movie_metadata.csv', 'rt', encoding='UTF8') as csvfile:
	reader = csv.DictReader(csvfile , delimiter=',')
	for row in reader:
	
		cur.execute("INSERT INTO MOVIES( ID,\
			MOVIE_TITLE,\
			ACTOR_1_FBLIKES,\
			ACTOR_2_FBLIKES,\
			ACTOR_3_FBLIKES,\
			CAST_TOTAL_FBLIKES,\
			MOVIE_FBLIKES,\
			DIRECTOR_FBLIKES,\
			ACTOR_1_NAME,\
			ACTOR_2_NAME,\
			ACTOR_3_NAME,\
			DIRECTOR_NAME,\
			NUM_VOTES,\
			TITLE_YEAR,\
			FACENUM,\
			BUDGET,\
			GROSS,\
			CONTENT_RATING,\
			NUM_CRITICS_REVIEWS,\
			NUM_USERS_REVIEWS,\
			PLOT_KEYWORDS,\
			ASPECT_RATIO,\
			MOVIE_LINK,\
			COUNTRY,\
			COLOR,\
			DURATION,\
			LANGUAGE,\
			IMDB_SCORE,\
			GENRES) \
			VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);" %(\
			i,\
			row['movie_title'],\
			row['actor_1_facebook_likes'],\
			row['actor_2_facebook_likes'],\
			row['actor_3_facebook_likes'],\
			row['cast_total_facebook_likes'],\
			row['movie_facebook_likes'],\
			row['director_facebook_likes'],\
			row['actor_1_name'],\
			row['actor_2_name'],\
			row['actor_3_name'],\
			row['director_name'],\
			row['num_voted_users'],\
			row['title_year'],\
			row['facenumber_in_poster'],\
			row['budget'],\
			row['gross'],\
			row['content_rating'],\
			row['num_critic_for_reviews'],\
			row['num_user_for_reviews'],\
			row['plot_keywords'],\
			row['aspect_ratio'],\
			row['movie_imdb_link'],\
			row['country'],\
			row['color'],\
			row['duration'],\
			row['language'],\
			row['imdb_score'],\
			row['genres']))
		
		conn.commit()
		i+=1

conn.close()
		














