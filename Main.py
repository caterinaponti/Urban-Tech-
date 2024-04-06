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
        (37.742870, -122.476450),
        # Add more coordinates as needed
    ]   
  
    for coords in marker_coordinates:
        folium.Marker(coords).add_to(mapObj)
    
    # Set iframe width and height
    mapObj.get_root().width = "1300px"
    mapObj.get_root().height = "650px"
    
    # Creates an HTML content string representing the Folium map
    iframe = mapObj.get_root()._repr_html_()

    return render_template_string( #allows you to pass variables to the HTML template. 
      """
          <!DOCTYPE html>
          <html>
              <head></head>
              <body style = "background: linear-gradient(115deg, #56d8e4 10%, #9f01ea 90%); font-family: serif;">
                  <h1 style = "color:Purple; border-color: Black">San Francisco Map</h1>
                  {{ iframe|safe }}
              </body>
          </html>
      """,
      iframe=iframe,
  )

if __name__ == "__main__":
    app.run()