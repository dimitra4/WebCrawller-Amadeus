# Install the Python library from https://pypi.org/project/amadeus
from amadeus import Client, ResponseError

amadeus = Client(
    client_id='vnDUfBsJ5s7B1R8p03tjoI2xHLfVkMa9',
    client_secret='y5KuO0tRpy4CVlPp'
)

print(amadeus)

try:
    print("1")
    response = amadeus.shopping.flight_offers_search.get()
    #response = amadeus.shopping.flight_destinations.get(origin='MAD')
    print(response.data)
    print(response.body)
    print(response.result)

except ResponseError as error:
    print(error)







