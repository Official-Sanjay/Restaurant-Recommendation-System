


from flask import Flask, jsonify, render_template, request
import pandas as pd
from math import radians, sin, cos, sqrt, atan2

app = Flask(__name__)

# Function to load restaurant data from an Excel file
def load_data_from_excel(file_path):
    df = pd.read_excel(file_path)
    return df.to_dict('records')

# Load restaurant data from the Excel file
restaurants = load_data_from_excel('D:/studies/amcat/data.xlsx')  # Update with your restaurant data file path

# Route for rendering the index page
@app.route('/')
def index():
    return render_template('index.html')

# Route for finding nearby restaurants
@app.route('/nearby_restaurants/<float:user_lat>/<float:user_lon>')
def nearby_restaurants(user_lat, user_lon):
    nearby_restaurants = []
    for restaurant in restaurants:
        restaurant_lat = restaurant['Latitude']
        restaurant_lon = restaurant['Longitude']
        distance = haversine(user_lat, user_lon, restaurant_lat, restaurant_lon)
        if distance <= 1:  # Change the distance as per your requirement
            nearby_restaurants.append({
                "name": restaurant['name'],
                "distance_km": distance,
                "rating": restaurant['ratings'],
                "latitude": restaurant['Latitude'],
                "longitude": restaurant['Longitude']
            })

    # Sort nearby restaurants by rating (descending order)
    nearby_restaurants = sorted(nearby_restaurants, key=lambda x: x['rating'], reverse=True)

    return jsonify(nearby_restaurants)

# Function to calculate distance using Haversine formula
def haversine(lat1, lon1, lat2, lon2):
    # convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = 6371 * c  # Radius of Earth in kilometers
    return distance

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
