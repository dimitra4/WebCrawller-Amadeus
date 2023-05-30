# Install the Python library from https://pypi.org/project/amadeus
from amadeus import Client, ResponseError
from datetime import datetime, timedelta
import csv
import os
import pymongo

# create the connection with Amadeus API
amadeus = Client(
    client_id='vnDUfBsJ5s7B1R8p03tjoI2xHLfVkMa9',
    client_secret='y5KuO0tRpy4CVlPp'
)

# list = [{'type': 'flight-offer', 'id': '1', 'source': 'GDS', 'instantTicketingRequired': False, 'nonHomogeneous': False, 'oneWay': False, 'lastTicketingDate': '2023-05-22', 'lastTicketingDateTime': '2023-05-22', 'numberOfBookableSeats': 4, 'itineraries': [{'duration': 'PT3H30M', 'segments': [{'departure': {'iataCode': 'ATH', 'at': '2023-05-28T10:40:00'}, 'arrival': {'iataCode': 'CDG', 'terminal': '0', 'at': '2023-05-28T13:10:00'}, 'carrierCode': 'GQ', 'number': '900', 'aircraft': {'code': '32N'}, 'operating': {'carrierCode': 'GQ'}, 'duration': 'PT3H30M', 'id': '147', 'numberOfStops': 0, 'blacklistedInEU': False}]}], 'price': {'currency': 'EUR', 'total': '71.19', 'base': '33.00', 'fees': [{'amount': '0.00', 'type': 'SUPPLIER'}, {'amount': '0.00', 'type': 'TICKETING'}], 'grandTotal': '71.19'}, 'pricingOptions': {'fareType': ['PUBLISHED'], 'includedCheckedBagsOnly': False}, 'validatingAirlineCodes': ['GQ'], 'travelerPricings': [{'travelerId': '1', 'fareOption': 'STANDARD', 'travelerType': 'ADULT', 'price': {'currency': 'EUR', 'total': '71.19', 'base': '33.00'}, 'fareDetailsBySegment': [{'segmentId': '147', 'cabin': 'ECONOMY', 'fareBasis': 'VILJOW', 'brandedFare': 'JOY', 'class': 'V', 'includedCheckedBags': {'quantity': 0}}]}]}, {'type': 'flight-offer', 'id': '2', 'source': 'GDS', 'instantTicketingRequired': False, 'nonHomogeneous': False, 'oneWay': False, 'lastTicketingDate': '2023-05-23', 'lastTicketingDateTime': '2023-05-23', 'numberOfBookableSeats': 9, 'itineraries': [{'duration': 'PT24H20M', 'segments': [{'departure': {'iataCode': 'ATH', 'at': '2023-05-28T11:45:00'}, 'arrival': {'iataCode': 'OSL', 'at': '2023-05-28T14:40:00'}, 'carrierCode': 'DY', 'number': '1885', 'aircraft': {'code': '73H'}, 'operating': {'carrierCode': 'DY'}, 'duration': 'PT3H55M', 'id': '113', 'numberOfStops': 0, 'blacklistedInEU': False}, {'departure': {'iataCode': 'OSL', 'at': '2023-05-29T08:40:00'}, 'arrival': {'iataCode': 'CDG', 'terminal': '1', 'at': '2023-05-29T11:05:00'}, 'carrierCode': 'DY', 'number': '1494', 'aircraft': {'code': '73H'}, 'operating': {'carrierCode': 'DY'}, 'duration': 'PT2H25M', 'id': '114', 'numberOfStops': 0, 'blacklistedInEU': False}]}], 'price': {'currency': 'EUR', 'total': '103.98', 'base': '71.00', 'fees': [{'amount': '0.00', 'type': 'SUPPLIER'}, {'amount': '0.00', 'type': 'TICKETING'}], 'grandTotal': '103.98', 'additionalServices': [{'amount': '45.00', 'type': 'CHECKED_BAGS'}]}, 'pricingOptions': {'fareType': ['PUBLISHED'], 'includedCheckedBagsOnly': False}, 'validatingAirlineCodes': ['DY'], 'travelerPricings': [{'travelerId': '1', 'fareOption': 'STANDARD', 'travelerType': 'ADULT', 'price': {'currency': 'EUR', 'total': '103.98', 'base': '71.00'}, 'fareDetailsBySegment': [{'segmentId': '113', 'cabin': 'ECONOMY', 'fareBasis': 'QKCALF', 'brandedFare': 'LOWFARE', 'class': 'Q', 'includedCheckedBags': {'quantity': 0}}, {'segmentId': '114', 'cabin': 'ECONOMY', 'fareBasis': 'HLF', 'brandedFare': 'LOWFARE', 'class': 'H', 'includedCheckedBags': {'quantity': 0}}]}]}, {'type': 'flight-offer', 'id': '3', 'source': 'GDS', 'instantTicketingRequired': False, 'nonHomogeneous': False, 'oneWay': False, 'lastTicketingDate': '2023-05-23', 'lastTicketingDateTime': '2023-05-23', 'numberOfBookableSeats': 9, 'itineraries': [{'duration': 'PT7H25M', 'segments': [{'departure': {'iataCode': 'ATH', 'at': '2023-05-28T12:35:00'}, 'arrival': {'iataCode': 'OSL', 'at': '2023-05-28T15:25:00'}, 'carrierCode': 'SK', 'number': '4638', 'aircraft': {'code': '73H'}, 'operating': {'carrierCode': 'SK'}, 'duration': 'PT3H50M', 'id': '133', 'numberOfStops': 0, 'blacklistedInEU': False}, {'departure': {'iataCode': 'OSL', 'at': '2023-05-28T16:50:00'}, 'arrival': {'iataCode': 'CDG', 'terminal': '1', 'at': '2023-05-28T19:00:00'}, 'carrierCode': 'SK', 'number': '839', 'aircraft': {'code': '73H'}, 'operating': {'carrierCode': 'SK'}, 'duration': 'PT2H10M', 'id': '134', 'numberOfStops': 0, 'blacklistedInEU': False}]}], 'price': {'currency': 'EUR', 'total': '108.98', 'base': '24.00', 'fees': [{'amount': '0.00', 'type': 'SUPPLIER'}, {'amount': '0.00', 'type': 'TICKETING'}], 'grandTotal': '108.98', 'additionalServices': [{'amount': '35.00', 'type': 'CHECKED_BAGS'}]}, 'pricingOptions': {'fareType': ['PUBLISHED'], 'includedCheckedBagsOnly': False}, 'validatingAirlineCodes': ['SK'], 'travelerPricings': [{'travelerId': '1', 'fareOption': 'STANDARD', 'travelerType': 'ADULT', 'price': {'currency': 'EUR', 'total': '108.98', 'base': '24.00'}, 'fareDetailsBySegment': [{'segmentId': '133', 'cabin': 'ECONOMY', 'fareBasis': 'OEOGHT', 'brandedFare': 'GOLIGHT', 'class': 'O', 'includedCheckedBags': {'quantity': 0}}, {'segmentId': '134', 'cabin': 'ECONOMY', 'fareBasis': 'OEOGHT', 'brandedFare': 'GOLIGHT', 'class': 'O', 'includedCheckedBags': {'quantity': 0}}]}]}]

listOfDestinations = [{'name': 'LISBON', 'iataCode': 'LIS', 'region': 'Portugal'},
    {'name': 'ROME', 'iataCode': 'ROM', 'region': 'Italy'},
    {'name': 'BARCELONA', 'iataCode': 'BCN', 'region': 'Spain'}, {'name': 'THIRA', 'iataCode': 'JTR', 'region': 'Greece'},
    {'name': 'VIENNA', 'iataCode': 'VIE', 'region': 'Austria'}, {'name': 'ISTANBUL', 'iataCode': 'IST', 'region': 'Turkey'},
    {'name': 'AMSTERDAM', 'iataCode': 'AMS', 'region': 'Netherlads'},
    {'name': 'MYKONOS', 'iataCode': 'JMK', 'region': 'Greece'}, {'name': 'PARIS', 'iataCode': 'PAR', 'region': 'France'},
    {'name': 'MADRID', 'iataCode': 'MAD', 'region': 'Spain'}]

# csv header
fieldnames = ['id', 'price', 'departureIataCode', 'departureName', 'departureIataCodeValidation','flightDate','destinationIataCode',
              'destinationName', 'destinationRegion', 'dateInserted', 'timeInserted', 'countOfOffers', 'arrival',
              'carrierCode', 'numberOfFlight', 'departureTime', 'arrivalTime', 'duration', 'totalStops' ]

today = datetime.now()
# tomorrow = today + timedelta(1)
# today = "2023-05-28"
print("Today's date:", today)

def api_call():
    try:
        # create the connection with MongoDB Atlas
        client = pymongo.MongoClient(
            'mongodb+srv://demetrakostala:VTQ7WvS3033c2WcW@clusterwebcrawler.o3bvkic.mongodb.net/?retryWrites=true&w=majority')
        mydb = client.flight_data_db
        flight_data = mydb.flight_data
        print(flight_data)

        # create an empty list
        print("\n\n---------------------------------------------------------------")
        addToList = []
        for j in listOfDestinations:
            # print(j['iataCode'])
            # print(today.strftime("%Y-%m-%d"))
            response = amadeus.shopping.flight_offers_search.get(originLocationCode='ATH',
                                                                destinationLocationCode=j['iataCode'],
                                                                departureDate=today.strftime("%Y-%m-%d"),
                                                                adults=1)
            list = response.data
            print(list)
            print(response.body)
            countOfOffers = len(list)
            for i in list:

                dictionary = {}
                res = dict((k, i[k]) for k in ['price', 'itineraries']
                        if k in i)
                print(res)
                dictionary['id'] = i['id']
                dictionary['price'] = res['price']['total']
                dictionary['departureIataCode'] = 'ATH'
                dictionary['departureName'] = 'ATHENS'
                dictionary['flightDate'] = today.strftime("%d/%m/%Y")
                dictionary['destinationIataCode'] = j['iataCode']
                dictionary['destinationName'] = j['name']
                dictionary['destinationRegion'] = j['region']
                dictionary['dateInserted'] = today.strftime("%d/%m/%Y") # dd/mm/YY
                dictionary['timeInserted'] = today.strftime("%H:%M")
                dictionary['countOfOffers'] = countOfOffers
                dictionary['duration'] = res['itineraries'][0]['duration']
                dictionary['totalStops'] = len(res['itineraries'][0]['segments'])-1

                for r in res['itineraries'][0]['segments'][0:1]:
                    print("in r1", r)
                    res2 = dict((k, r[k]) for k in ['departure']
                                if k in r)
                    dictionary['departureTime'] = res2['departure']['at']

                  # 'departureTime', 'arrivalTime', 'duration', 'totalStops'
                for r in res['itineraries'][0]['segments'][-1:]:
                    print("r", r)
                    res1 = dict((k, r[k]) for k in ['arrival', 'carrierCode', 'number', 'departure', 'numberOfStops']
                                if k in r)
                    dictionary['departureIataCodeValidation'] = res1['departure']['iataCode']
                    dictionary['arrival'] = res1['arrival']['iataCode']
                    dictionary['carrierCode'] = res1['carrierCode']
                    dictionary['numberOfFlight'] = res1['number']
                    dictionary['arrivalTime'] = res1['arrival']['at']

                # dict_copy = dict.copy()
                print(dictionary)
                # addToList.append(dict_copy)

                # create the query to check if document exists in mongoDB
                query = {"$and": [{"price": dictionary['price']},
                                  {"carrierCode": dictionary['carrierCode']},
                                  {"departureIataCode": dictionary['departureIataCode']},
                                  {"departureIataCodeValidation": dictionary['departureIataCodeValidation']},
                                  {"numberOfFlight": dictionary['numberOfFlight']},
                                  {"destinationIataCode": dictionary['destinationIataCode']},
                                  {"flightDate": dictionary['flightDate']},
                                  {"arrival": dictionary['arrival']}]}

                count = flight_data.count_documents(query)
                # if not exists then append to list, to csv, to google sheets
                print(count)
                if count == 0:
                    # add to mongoDB
                    x = flight_data.insert_one(dictionary)
                    addToList.append(dictionary)

        print(addToList)
        print("len list is ", len(addToList))

        if len(addToList) > 0:
            # WRIGHT IN CSV
            with open('country_new.csv', 'a', encoding='UTF8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
                if os.stat("country_new.csv").st_size == 0:
                    writer.writeheader()
                writer.writerows(addToList)

    except ResponseError as error:
        raise




