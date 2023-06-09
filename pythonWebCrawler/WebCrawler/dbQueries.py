import pymongo

# create the connection with MongoDB Atlas
client = pymongo.MongoClient(
        'mongodb+srv://demetrakostala:VTQ7WvS3033c2WcW@clusterwebcrawler.o3bvkic.mongodb.net/?retryWrites=true&w=majority')
mydb = client.flight_data_db
flight_data = mydb.flight_data
# print(flight_data)

# Retrieve all documents from the collection
documents = flight_data.find()

# Print the contents of each document
# for document in documents:
#     print(document)


def findUniqueCarrierCodeForDest(dest):
        query = { "destinationName": dest}
        results = flight_data.distinct("carrierCode", query)
        return results

# results = findUniqueCarrierCodeForDest("ROME")
# print(results)

def findUniqueTotalStopsForDest(dest):
        query = {"destinationName": dest}
        results = flight_data.distinct("totalStops", query)
        return results

# results1 = findUniqueTotalStopsForDest("MADRID")
# print(results1)

def findTotalStopsForDestAggregated(dest):
        pipeline = [
                {
                '$match': {
                    'destinationName': dest,
                        }
                },
                {
                '$group': {
                    '_id': '$totalStops',
                    'count': { '$sum': 1 }
                        }
                },
                {
                '$sort': {
                    'count': -1
                        }
                }
        ]
        # Perform the aggregation
        result = flight_data.aggregate(pipeline)
        list =[]
        # Iterate over the result and print the output
        for doc in result:
                list.append(doc)

        return list

# findTotalStopsForDestAggregated("LISBON")


