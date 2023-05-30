import schedule
from airportRoutes import api_call


# schedule.every(2).hours.do(api_call)
# while True:
#   schedule.run_pending()

api_call()