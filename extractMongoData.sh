#instructions on how to see the data in mongo via terminal
#conceptually:
#mongo
#use <desired_database_name>
#db.<desired_collection>.find({}).pretty()

#example:
#mongo
#use thanksgiving
#db.stream.find({}).pretty()

mongoexport --host localhost --db thanksgiving --collection stream --type=csv --out thanksgiving.csv --fields id,user,text