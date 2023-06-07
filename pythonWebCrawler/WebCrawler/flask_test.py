from flask import Flask, redirect, url_for, render_template, request
import requests
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from airportRoutes import api_call
from airfair_pred import predictPrice
app = Flask(__name__)


scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(func=api_call, trigger="interval", seconds=7200)
scheduler.start() 
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

@app.route('/')
def index():
    api_call()
    return 'Hello wrold'

@app.route("/search", methods= ["POST", "GET"])
def search():
    print("edw")
    if request.method == "POST" :
        selected_date = request.form.get('selected_date')
       
        selected_date = dt.strptime(selected_date, '%m/%d/%Y')
        sday=selected_date.day
        smonth= selected_date.month

        country = request.form.get('country')
        stops = request.form.get('stops')
        stops =  1 if stops ==1 else 0

        print( selected_date, country, stops  )

        avg_price = predictPrice(sday, smonth, country, stops)
        
        return render_template("prediction.html", result1 = selected_date , result2 = country, result3 =avg_price)
    else:
        return render_template("search.html")


@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"

@app.route('/refresh-tableau', methods=['POST'])
def refresh_tableau():
    # Specify the details for the Tableau Server REST API
    tableau_server_url = 'http://your_tableau_server_url'
    username = 'your_username'
    password = 'your_password'
    data_source_id = 'your_data_source_id'

    # Construct the refresh API endpoint URL
    refresh_url = f'{tableau_server_url}/api/3.11/sites/default/dataSources/{data_source_id}/refresh'

    # Make the POST request to trigger the data source refresh
    response = requests.post(refresh_url, auth=(username, password))

    if response.status_code == 200:
        return 'Tableau data source refresh initiated successfully'
    else:
        return 'Failed to initiate Tableau data source refresh'


if __name__ == "__main__":
    app.debug = True
    app.run()
    
