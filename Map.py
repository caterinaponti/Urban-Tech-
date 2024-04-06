import folium
from flask import Flask, render_template_string

app = Flask(__name__)
app.debug = True

@app.route("/map")
def display_map():
  # Initializes a Folium map centered at San Francisco with a specified zoom level
    mapObj = folium.Map(location=[37.7749, -122.4194], zoom_start=12)

    # List of coordinates for markers
    marker_coordinates = [
        (37.776360, -122.449898, 'University of San Francisco'),
        (37.742870, -122.476450, 'Waste'),
        # Add more coordinates as needed
    ]   
  
    for coords in marker_coordinates:
        folium.Marker(location= [coords[0], coords[1]], tooltip=coords[2]).add_to(mapObj)
    
    # Set iframe width and height
    mapObj.get_root().width = "1300px"
    mapObj.get_root().height = "650px"


    mapObj.save("san_francisco_map.html")

if __name__ == "__main__":
    display_map()
    
