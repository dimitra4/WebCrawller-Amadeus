from flask import Flask, redirect, url_for, render_template, request
import requests
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from airportRoutes import api_call
from airfair_pred import predictPrice, train
from datetime import datetime as dt
app = Flask(__name__)


scheduler = BackgroundScheduler()
# daemon=True
scheduler.add_job(func=api_call, trigger="interval", hours=2, max_instances=1)
scheduler.add_job(func=train, trigger="interval", hours=5, max_instances=1)

scheduler.start()

# Shut down the schedulers when exiting the app
atexit.register(lambda: scheduler.shutdown())


@app.route("/", methods= ["POST", "GET"])
def search():
    if request.method == "POST" :
        form_selected_date=request.form.get('selected_date')
       
        selected_date = dt.strptime(form_selected_date, '%m/%d/%Y')
        sday=selected_date.day
        smonth= selected_date.month

        country = request.form.get('country')
        stops =  request.form.get('stops')
        stops = 1 if stops == "1" else 0

        avg_price = predictPrice(sday, smonth, country, stops)
        avg_price=round(avg_price, 2)
        
        return render_template("prediction.html", result1 = form_selected_date , result2 = country, result3 =avg_price)
    else:
        return render_template("search.html")


if __name__ == "__main__":
    app.debug = True
    app.run()
    
