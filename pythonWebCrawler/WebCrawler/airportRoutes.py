# Install the Python library from https://pypi.org/project/amadeus
from amadeus import Client, ResponseError
import csv
import pymongo

amadeus = Client(
    client_id='vnDUfBsJ5s7B1R8p03tjoI2xHLfVkMa9',
    client_secret='y5KuO0tRpy4CVlPp'
)

client = pymongo.MongoClient('mongodb://localhost:27017')

mydb = client.WebCrawler

collections = mydb.list_collection_names()

print(mydb)
print(collections)

countries = mydb.Countries

print(countries)

# csv header
fieldnames = ['name', 'iataCode']

try:
    '''
    What are the destinations served by BLR airport?
    '''
    response = amadeus.airport.direct_destinations.get(departureAirportCode='MAD')
    list = response.data
    print(response.body)
    print(response.result)
    print(list[0]['name'])

    # create an empty list
    addToList = []

    for i in list:
        res = dict((k, i[k]) for k in ['name', 'iataCode']
                   if k in i)
        print(res)
        print(res['iataCode'])
        if res.get('iataCode') != countries.find({"iataCode": res['iataCode']})[0].get('iataCode'):
            print("yes")

        for doc1 in countries.find({"iataCode": res['iataCode']}):
            print(doc1['iataCode'])
            print(countries.find({"iataCode": res['iataCode']})[0].get('iataCode'))

        addToList.append(res)
    #print(countries.find({"iataCode": "AGP"}))
    print(addToList)

    # add to mongoDB
    # x = countries.insert_many(addToList)
    # # print list of the _id values of the inserted documents:
    # print(x.inserted_ids)
    # # delete from mongoDB
    # countries.delete_many({})
    # print(del.deleted_count, " documents deleted.")

    # WRIGHT IN CSV
    # with open('country_iatacodes.csv', 'a', encoding='UTF8', newline='') as f:
    #     writer = csv.DictWriter(f, fieldnames=fieldnames)
    #     writer.writeheader()
    #     for i in list:
    #         res = dict((k, i[k]) for k in ['name', 'iataCode']
    #                    if k in i)
    #         print(res)
    #         writer.writerow(res)

except ResponseError as error:
    raise