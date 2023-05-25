# Install the Python library from https://pypi.org/project/amadeus
from amadeus import Client, ResponseError

amadeus = Client(
    client_id='vnDUfBsJ5s7B1R8p03tjoI2xHLfVkMa9',
    client_secret='y5KuO0tRpy4CVlPp'
)

print(amadeus)

def first_request():
    try:
        print("1")
        response = amadeus.shopping.flight_offers_search.get()
        #response = amadeus.shopping.flight_destinations.get(origin='MAD')
        print(response.data)
        print(response.body)
        print(response.result)

    except ResponseError as error:
        print(error)

#https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode=ATH&destinationLocationCode=PAR&departureDate=2023-05-28&adults=1&nonStop=false&max=250

def flights_req():
    try:
        response = amadeus.shopping.flight_offers_search.get(originLocationCode='MAD',
                destinationLocationCode='BOS',
                departureDate='2023-05-05',
                adults='1')
        print(response.data)
        print(response.body)
        print(response.result)
    except ResponseError as error:
        print(error)




flights_req()












