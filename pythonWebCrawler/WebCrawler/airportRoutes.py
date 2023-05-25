# Install the Python library from https://pypi.org/project/amadeus
from amadeus import Client, ResponseError
from datetime import datetime
import csv
import os
# import pymongo


# list = [{'type': 'flight-offer', 'id': '1', 'source': 'GDS', 'instantTicketingRequired': False, 'nonHomogeneous': False, 'oneWay': False, 'lastTicketingDate': '2023-05-22', 'lastTicketingDateTime': '2023-05-22', 'numberOfBookableSeats': 4, 'itineraries': [{'duration': 'PT3H30M', 'segments': [{'departure': {'iataCode': 'ATH', 'at': '2023-05-28T10:40:00'}, 'arrival': {'iataCode': 'CDG', 'terminal': '0', 'at': '2023-05-28T13:10:00'}, 'carrierCode': 'GQ', 'number': '900', 'aircraft': {'code': '32N'}, 'operating': {'carrierCode': 'GQ'}, 'duration': 'PT3H30M', 'id': '147', 'numberOfStops': 0, 'blacklistedInEU': False}]}], 'price': {'currency': 'EUR', 'total': '71.19', 'base': '33.00', 'fees': [{'amount': '0.00', 'type': 'SUPPLIER'}, {'amount': '0.00', 'type': 'TICKETING'}], 'grandTotal': '71.19'}, 'pricingOptions': {'fareType': ['PUBLISHED'], 'includedCheckedBagsOnly': False}, 'validatingAirlineCodes': ['GQ'], 'travelerPricings': [{'travelerId': '1', 'fareOption': 'STANDARD', 'travelerType': 'ADULT', 'price': {'currency': 'EUR', 'total': '71.19', 'base': '33.00'}, 'fareDetailsBySegment': [{'segmentId': '147', 'cabin': 'ECONOMY', 'fareBasis': 'VILJOW', 'brandedFare': 'JOY', 'class': 'V', 'includedCheckedBags': {'quantity': 0}}]}]}, {'type': 'flight-offer', 'id': '2', 'source': 'GDS', 'instantTicketingRequired': False, 'nonHomogeneous': False, 'oneWay': False, 'lastTicketingDate': '2023-05-23', 'lastTicketingDateTime': '2023-05-23', 'numberOfBookableSeats': 9, 'itineraries': [{'duration': 'PT24H20M', 'segments': [{'departure': {'iataCode': 'ATH', 'at': '2023-05-28T11:45:00'}, 'arrival': {'iataCode': 'OSL', 'at': '2023-05-28T14:40:00'}, 'carrierCode': 'DY', 'number': '1885', 'aircraft': {'code': '73H'}, 'operating': {'carrierCode': 'DY'}, 'duration': 'PT3H55M', 'id': '113', 'numberOfStops': 0, 'blacklistedInEU': False}, {'departure': {'iataCode': 'OSL', 'at': '2023-05-29T08:40:00'}, 'arrival': {'iataCode': 'CDG', 'terminal': '1', 'at': '2023-05-29T11:05:00'}, 'carrierCode': 'DY', 'number': '1494', 'aircraft': {'code': '73H'}, 'operating': {'carrierCode': 'DY'}, 'duration': 'PT2H25M', 'id': '114', 'numberOfStops': 0, 'blacklistedInEU': False}]}], 'price': {'currency': 'EUR', 'total': '103.98', 'base': '71.00', 'fees': [{'amount': '0.00', 'type': 'SUPPLIER'}, {'amount': '0.00', 'type': 'TICKETING'}], 'grandTotal': '103.98', 'additionalServices': [{'amount': '45.00', 'type': 'CHECKED_BAGS'}]}, 'pricingOptions': {'fareType': ['PUBLISHED'], 'includedCheckedBagsOnly': False}, 'validatingAirlineCodes': ['DY'], 'travelerPricings': [{'travelerId': '1', 'fareOption': 'STANDARD', 'travelerType': 'ADULT', 'price': {'currency': 'EUR', 'total': '103.98', 'base': '71.00'}, 'fareDetailsBySegment': [{'segmentId': '113', 'cabin': 'ECONOMY', 'fareBasis': 'QKCALF', 'brandedFare': 'LOWFARE', 'class': 'Q', 'includedCheckedBags': {'quantity': 0}}, {'segmentId': '114', 'cabin': 'ECONOMY', 'fareBasis': 'HLF', 'brandedFare': 'LOWFARE', 'class': 'H', 'includedCheckedBags': {'quantity': 0}}]}]}, {'type': 'flight-offer', 'id': '3', 'source': 'GDS', 'instantTicketingRequired': False, 'nonHomogeneous': False, 'oneWay': False, 'lastTicketingDate': '2023-05-23', 'lastTicketingDateTime': '2023-05-23', 'numberOfBookableSeats': 9, 'itineraries': [{'duration': 'PT7H25M', 'segments': [{'departure': {'iataCode': 'ATH', 'at': '2023-05-28T12:35:00'}, 'arrival': {'iataCode': 'OSL', 'at': '2023-05-28T15:25:00'}, 'carrierCode': 'SK', 'number': '4638', 'aircraft': {'code': '73H'}, 'operating': {'carrierCode': 'SK'}, 'duration': 'PT3H50M', 'id': '133', 'numberOfStops': 0, 'blacklistedInEU': False}, {'departure': {'iataCode': 'OSL', 'at': '2023-05-28T16:50:00'}, 'arrival': {'iataCode': 'CDG', 'terminal': '1', 'at': '2023-05-28T19:00:00'}, 'carrierCode': 'SK', 'number': '839', 'aircraft': {'code': '73H'}, 'operating': {'carrierCode': 'SK'}, 'duration': 'PT2H10M', 'id': '134', 'numberOfStops': 0, 'blacklistedInEU': False}]}], 'price': {'currency': 'EUR', 'total': '108.98', 'base': '24.00', 'fees': [{'amount': '0.00', 'type': 'SUPPLIER'}, {'amount': '0.00', 'type': 'TICKETING'}], 'grandTotal': '108.98', 'additionalServices': [{'amount': '35.00', 'type': 'CHECKED_BAGS'}]}, 'pricingOptions': {'fareType': ['PUBLISHED'], 'includedCheckedBagsOnly': False}, 'validatingAirlineCodes': ['SK'], 'travelerPricings': [{'travelerId': '1', 'fareOption': 'STANDARD', 'travelerType': 'ADULT', 'price': {'currency': 'EUR', 'total': '108.98', 'base': '24.00'}, 'fareDetailsBySegment': [{'segmentId': '133', 'cabin': 'ECONOMY', 'fareBasis': 'OEOGHT', 'brandedFare': 'GOLIGHT', 'class': 'O', 'includedCheckedBags': {'quantity': 0}}, {'segmentId': '134', 'cabin': 'ECONOMY', 'fareBasis': 'OEOGHT', 'brandedFare': 'GOLIGHT', 'class': 'O', 'includedCheckedBags': {'quantity': 0}}]}]}]

listOfDestinations = [{'name': 'MYKONOS', 'iataCode': 'JMK'}] #, {'name': 'PARIS', 'iataCode': 'PAR'} ,
                    #    {'name': 'ROME', 'iataCode': 'ROM'}, {'name': 'MADRID', 'iataCode': 'MAD'}]
                      # {'name': 'BARCELONA', 'iataCode': 'BCN'}, {'name': 'THIRA', 'iataCode': 'JTR'},
                      # {'name': 'IRAKLEION', 'iataCode': 'HER'}, {'name': 'ISTANBUL', 'iataCode': 'IST'},
                      # {'name': 'AMSTERDAM', 'iataCode': 'AMS'}, {'name': 'LISBON', 'iataCode': 'LIS'}]

amadeus = Client(
    client_id='vnDUfBsJ5s7B1R8p03tjoI2xHLfVkMa9',
    client_secret='y5KuO0tRpy4CVlPp'
)

# client = pymongo.MongoClient('mongodb://localhost:27017')
# mydb = client.WebCrawler
# collections = mydb.list_collection_names()
# print(mydb)
# print(collections)
# countries = mydb.Countries
# print(countries)
# csv header
fieldnames = ['id', 'price', 'departureIataCode', 'departureName', 'flightDate', 'destinationIataCode',
              'destinationName', 'dateInserted', 'timeInserted', 'countOfOffers', 'arrival',
              'carrierCode', 'numberOfFlight']

today = datetime.now()
print("Today's date:", today)

def api_call():
    try:
        # create an empty list
        print("\n\n---------------------------------------------------------------")
        addToList = []
        Dict = {}
        for j in listOfDestinations:
            # print(j['iataCode'])
            # print(today.strftime("%Y-%m-%d"))
            response = amadeus.shopping.flight_offers_search.get(originLocationCode='ATH',
                                                                destinationLocationCode=j['iataCode'],
                                                                departureDate=today.strftime("%Y-%m-%d"),
                                                                adults=1,
                                                                max=150)
            list = response.data
            print(list)
            print(response.body)
            count = len(list)
            for i in list:
                res = dict((k, i[k]) for k in ['price', 'itineraries']
                        if k in i)
                Dict['id'] = i['id']
                Dict['price'] = res['price']['total']
                Dict['departureIataCode'] = 'ATH'
                Dict['departureName'] = 'ATHENS'
                Dict['flightDate'] = today.strftime("%d/%m/%Y")
                Dict['destinationIataCode'] = j['iataCode']
                Dict['destinationName'] = j['name']
                Dict['dateInserted'] = today.strftime("%d/%m/%Y") # dd/mm/YY
                Dict['timeInserted'] = today.strftime("%H:%M")
                Dict['countOfOffers'] = count

                # print(Dict)
                #
                # print(res['itineraries'][0]['segments'][-1:])

                for r in res['itineraries'][0]['segments'][-1:]:
                    res1 = dict((k, r[k]) for k in ['arrival', 'carrierCode', 'number']
                                if k in r)
                    Dict['arrival'] = res1['arrival']['iataCode']
                    Dict['carrierCode'] = res1['carrierCode']
                    Dict['numberOfFlight'] = res1['number']

                dict_copy = Dict.copy()

                # if res.get('iataCode') != countries.find({"iataCode": res['iataCode']})[0].get('iataCode'):
                #     print("yes")

                # for doc1 in countries.find({"iataCode": res['iataCode']}):
                #     print(doc1['iataCode'])
                #     print(countries.find({"iataCode": res['iataCode']})[0].get('iataCode'))
                print(Dict)
                addToList.append(dict_copy)

        print(addToList)

        # add to mongoDB
        # x = countries.insert_many(addToList)
        # # print list of the _id values of the inserted documents:
        # print(x.inserted_ids)
        # # delete from mongoDB
        # countries.delete_many({})
        # print(del.deleted_count, " documents deleted.")

        # WRIGHT IN CSV

        with open('country_new.csv', 'a', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if( os.stat("country_new.csv").st_size == 0 ):
                writer.writeheader()
            writer.writerows(addToList)
            # for i in list:
            #     res = dict((k, i[k]) for k in ['name', 'iataCode']
            #                if k in i)
            #     print(res)
            #     writer.writerow(res)

    except ResponseError as error:
        raise



