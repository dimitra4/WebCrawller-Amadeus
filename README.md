# FlightViz Web App

### ✈️ Flight Price Prediction & Dashboard

A web application that integrates data from the Amadeus for Developers API to provide:

- An interactive dashboard with visualizations.
- A search form to explore airfare data.
- A prediction model for airfare trends.
- A web crawler to collect and store flight offers in a MongoDB database.

This project combines data engineering (web crawling, APIs, databases) with data science (prediction modeling, visualization) to help users explore and forecast flight prices.

### 🚀 Features

- Amadeus API Integration – Fetch real-time flight offers (origin, destination, price, carrier, etc.).
- MongoDB Storage – Store flight offers efficiently with duplication checks.
- CSV Export – Automatically write new results into CSV for further processing.
- Data Pipeline – Flight offers → MongoDB → CSV → Dashboard.
- Interactive Dashboard – Visualize flight prices, destinations, carriers, and trends.
- Prediction Model – Forecast airfare prices based on collected data.

### 🛠️ Tech Stack

- Python 3
- Amadeus Python SDK (for API calls to collect airfare data)
- Flask (for Api calls to the FlightViz Web Application)
- MongoDB Atlas (cloud database)
- CSV Storage (backup/export)
- Tableau (for dashboard visualizations)
- Scikit-learn (for airfare prediction model)
