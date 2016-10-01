from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import task

try:
	client = MongoClient()
	db = client.provakil
except ConnectionFailure as e:
	print "Could not connect to mongo instance"
	print repr(e)

input_list = task.inputs()	
lists = task.get_case_status(input_list[0],input_list[1],input_list[2])
db.cases.drop()
if not lists:
             print "Sorry ! No data found"
else:
	for case in lists:
		db.cases.insert(case)

	print "Data Inserted!!!!"
