from flask import Flask, request
import googlemaps

app = Flask(__name__)

# Requires API key
gmaps = googlemaps.Client(key='AIzaSyDgUK5W99p5QmoNWC3zI09sLN3GOwH7Ruk')

category_destinations = {
    'education': (37.776360, -122.449898),  # University of San Francisco
    'food': (37.7738489, -122.4526904),      # Haight-Ashbury
    'safety': (37.7724895, -122.4565344),    # Police Department Park Station
    'health': (37.775145, -122.4539253),     # St. Mary Health Clinic
    'transportation': (37.775400, -122.449730),  # Transportation, Muni: 5
    'shopping': (37.7820461, -122.4491252),  # City Center
    'outdoors': (37.7703713, -122.4483282)   # Buena Vista Park
}

def get_distance(origin_lat, origin_lng, destination_lat, destination_lng):
    distance_matrix = gmaps.distance_matrix((origin_lat, origin_lng), 
                                            (destination_lat, destination_lng),
                                            mode="walking")
    distance = distance_matrix['rows'][0]['elements'][0]['distance']['text']
    
    return distance

@app.route('/')
def main():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Green Tech</title>
    </head>
    <body style = "background: linear-gradient(90deg, rgba(138,248,161,1) 0%, rgba(2,33,8,0.946298984034833) 100%);">
        <h3>The Golden Gate Project</h3>
        <form method="POST" action="form_input">
        <label for="category">Select What Service You Need:</label>
        <select name ="category" id="category">
        <option value="education">Education</option>
        <option value="food">Food</option>
        <option value="safety">Safety</option>
        <option value="health">Health</option>
        <option value="shopping">Shopping</option>
        <option value="education">Education</option>
        <option value="outdoors">Outdoors</option>
        <option value="transportation">Transportation</option>
        </select>
        <br>
        <input type="submit" value="Submit"> 
        </form>
    </body>
    </html>
    """

def calculate_distance():
    category = request.form.get('category')
    if category not in category_destinations:
        return "Invalid category selected."

    origin_lat = 37.776360
    origin_lng = -122.449898 #USF
    destination_lat, destination_lng = category_destinations[category]
    distance = get_distance(origin_lat, origin_lng, destination_lat, destination_lng)

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Distance Result</title>
    </head>
    <body style = "background: linear-gradient(90deg, rgba(138,248,161,1) 0%, rgba(2,33,8,0.946298984034833) 100%);">
        <img style="border:5px double black; float:right" src="https://images.pexels.com/photos/1118873/pexels-photo-1118873.jpeg?auto=compress&cs=tinysrgb&w=800" width="300" height="150">
        <hr>
        <br>
        <br>
        <p>The distance between the University of San Francisco and {category} is {distance}.</p>
        <br>
        <input type="button" onclick="location.href='/'" value="Start Again" />
        <hr>
        <br>
    </body>
    </html>
    """

@app.route('/form_input', methods=['POST'])
def form_input():
    category = request.form.get('category')

    destination_lat, destination_long = category_destinations[category]
    distance = get_distance(37.776360, -122.449898, destination_lat, destination_long)
    result = f'The distance to {category} is {distance}.'
    
    # Retrieve the link for the selected category
    link = {
        'education': 'https://www.usfca.edu',
        'food': 'https://www.tripadvisor.com/Restaurants-g60713-zfn7222620-San_Francisco_California.html',
        'health': 'https://myusf.usfca.edu/hps/health-clinic/dignity-medical-services',
        'safety': 'https://www.sanfranciscopolice.org/stations/park-station',
        'transportation': 'https://www.sfmta.com/routes/5-fulton',
        'shopping': 'https://www.sfjapantown.org/japan-center-malls/',
        'outdoors': 'https://sfrecpark.org/facilities/facility/details/Buena-Vista-Park-155'
    }.get(category, '')

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Distance Result</title>
    </head>
    <body style = "background: linear-gradient(90deg, rgba(138,248,161,1) 0%, rgba(2,33,8,0.946298984034833) 100%);">
        <img style="border:5px double black; float:right" src="https://static.dw.com/image/61391638_1004.jpeg" width="900" height="450">
        <hr>
        <br>
        <br>
        <p>The distance to {category} is {distance}.</p>
        <p>For more information, visit: <a href="{link}" target="_blank">{category}</a></p>
        <br>
        <input type="button" onclick="location.href='/'" value="Start Again" />
        <hr>
        <br>
    </body>
    </html>
    """

    return html


if __name__ == '__main__':
    app.run(debug=True)
