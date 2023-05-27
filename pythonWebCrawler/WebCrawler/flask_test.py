from flask import Flask, redirect, url_for, render_template, request
import requests
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from airportRoutes import api_call
app = Flask(__name__)



def schedule_call():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=api_call, trigger="interval", seconds=3600)
    scheduler.start()
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

@app.route('/')
def index():
    return 'Hello wrold'

@app.route("/login", methods= ["POST", "GET"])
def login():
    if request.method == "POST" :
        user = request.form["nm"]
        return redirect(url_for("user", usr=user))
    else:
        return render_template("login.html")

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
    schedule_call()