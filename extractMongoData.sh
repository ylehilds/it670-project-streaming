
#show dbs

#instructions on how to see the data in mongo via terminal
#conceptually:
#mongo
#use <desired_database_name>
#db.<desired_collection>.find({}).pretty()

#example:
#mongo
#use thanksgiving
#db.stream.find({}).pretty()

#how to clear a collection:
#use thanksgiving
#db.stream.remove( { } )
#db.dropDatabase()
mongoexport --host localhost --db presidential_candidates_2020 --collection stream --type=csv --out presidential_candidates_2020.csv --fields tweet_id,user_id,user_name,text,candidate,url,retweet_count,favorite_count,polarity,subjectivity,sentiment,description,location,coords,geo,name,user_created,followers,created,bg_color,images
