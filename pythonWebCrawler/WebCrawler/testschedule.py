import schedule
from airportRoutes import api_call

schedule.every(10).seconds.do(api_call)
while True:
  schedule.run_pending()
