from flask import Flask, request
import googlemaps

app = Flask(__name__)

# Requires API key
gmaps = googlemaps.Client(key='AIzaSyDgUK5W99p5QmoNWC3zI09sLN3GOwH7Ruk')

def get_distance(origin_lat, origin_lng, destination_lat, destination_lng):
    # Calculate distance using Haversine formula
    # Alternatively, you can use the Google Maps Distance Matrix API
    # But for simplicity, let's calculate it here
    earth_radius = 6371  # Radius of the Earth in kilometers
    dlat = origin_lat - destination_lat
    dlng = origin_lng - destination_lng
    a = (dlat / 180) ** 2 + (dlng / 180) ** 2 * (origin_lat / 180) * (destination_lat / 180)
    c = 2 * earth_radius * a**0.5
    distance = c * 1000  # Convert to meters
    return distance

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Distance Calculator</title>
    </head>
    <body>
        <h1>Calculate Distance between Places within the Same City</h1>
        <form action="/calculate" method="post">
            <label for="origin_lat">Origin Latitude:</label>
            <input type="text" id="origin_lat" name="origin_lat"><br><br>
            <label for="origin_lng">Origin Longitude:</label>
            <input type="text" id="origin_lng" name="origin_lng"><br><br>
            <label for="destination_lat">Destination Latitude:</label>
            <input type="text" id="destination_lat" name="destination_lat"><br><br>
            <label for="destination_lng">Destination Longitude:</label>
            <input type="text" id="destination_lng" name="destination_lng"><br><br>
            <input type="submit" value="Calculate Distance">
        </form>
    </body>
    </html>
    """

@app.route('/calculate', methods=['POST'])
def calculate_distance():
    origin_lat = 37.776360
    origin_lng = -122.449898
    destination_lat = 37.742870
    destination_lng = -122.476450
    distance = get_distance(origin_lat, origin_lng, destination_lat, destination_lng)
    return f"The distance between the two places is {distance:.2f} meters."

if __name__ == '__main__':
    app.run(debug=True)
