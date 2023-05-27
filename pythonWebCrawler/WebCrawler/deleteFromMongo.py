import pymongo
from datetime import datetime

client = pymongo.MongoClient('mongodb+srv://demetrakostala:VTQ7WvS3033c2WcW@clusterwebcrawler.o3bvkic.mongodb.net/?retryWrites=true&w=majority')

mydb = client.flight_data_db
flight_data = mydb.flight_data

flight_data.delete_many({})