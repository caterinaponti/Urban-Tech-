import folium
from flask import Flask
from math import radians, sin, cos, sqrt, atan2


app = Flask(__name__)
app.debug = True

def calculate_distance(coord1, coord2):

    R = 6371.0

    lat1 = radians(coord1[0])
    lat2 = radians(coord2[0])
    lon1 = radians(coord1[1])
    lon2 = radians(coord2[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    distance = R * c
    
    return distance

def km_to_minutes(distance):
    walking_speed = 5.0 #average walking speed 
    time_hours = distance /walking_speed
    time_minutes = time_hours * 60

    return time_minutes

def create_marker(coord, name, url=None, color=None):
    if color:
        icon = folium.Icon(color=color)
        marker = folium.Marker(location=coord, tooltip=name, icon=icon)
    else:
        marker = folium.Marker(location=coord, tooltip=name)
    if url:
        popup = f'<a href="{url}" target="_blank">{name}</a>'
        marker.add_child(folium.Popup(popup))
    return marker

@app.route("/map")
def display_map():
    mapObj = folium.Map(location=[37.7797807,-122.4329079], zoom_start=15)

    # List of coordinates for markers
    marker_coordinates = [
        (37.776360, -122.449898, 'University of San Francisco',  'https://www.usfca.edu'),
        (37.742870, -122.476450, 'Waste', 'https://www.google.com/maps/dir/37.7683968,-122.4572928/Titan+Junk+Removal+Inc.,+945+Taraval+St+Suite+1081,+San+Francisco,+CA+94116/@37.7556169,-122.4882594,14z/data=!3m1!4b1!4m9!4m8!1m1!4e1!1m5!1m1!1s0x2c22379db5e7c6dd:0xfea1e1472b35cebd!2m2!1d-122.4764775!2d37.7428405?entry=ttu'  ),
        (37.804430, -122.413370, 'Water', 'https://www.google.com/maps/place/San+Francisco+Water+Department/@37.7810731,-122.4218213,17z/data=!3m1!4b1!4m6!3m5!1s0x808f7f00c18d6df7:0xaf9b1f7f76595df6!8m2!3d37.7810731!4d-122.4192464!16s%2Fg%2F1tjmdw_z?entry=ttu'),
        (37.775145,-122.4539253, 'Health', 'https://myusf.usfca.edu/hps/health-clinic/dignity-medical-services' ),
        (37.7724895,-122.4565344, 'Safety', 'https://www.sanfranciscopolice.org/stations/park-station'),
        (37.775400, -122.449730, 'Transportation, Muni: 5', 'https://www.sfmta.com/routes/5-fulton'),
        (37.7820461,-122.4491252, 'Shopping', "https://www.google.com/maps?sca_esv=09421e5d5db007db&output=search&q=city+center+shopping+mall&source=lnms&entry=mc&ved=1t:200715&ictx=111" ),
        (37.7738489,-122.4526904, 'Food', 'https://www.tripadvisor.com/Restaurants-g60713-zfn7222620-San_Francisco_California.html'),
        (37.7703713,-122.4483282, 'Outdoors', 'https://sfrecpark.org/facilities/facility/details/Buena-Vista-Park-155' ),
        (37.7690194,-122.4572928, 'Shopping', 'https://www.sfjapantown.org/japan-center-malls/'),
        (37.7726187,-122.4602558, 'Outdoors', 'https://sfrecpark.org/770/Golden-Gate-Park'),
        (37.7762203,-122.4557959, 'Food', "https://www.sfvelorouge.com/"),
        (37.774591,-122.4649513, 'Entertainment', 'https://www.voguemovies.com/'),
        (37.7762726,-122.44138, 'Food', 'https://www.themillsf.com/'),
        (37.7807178,-122.4390234, 'Shopping', 'https://www.yelp.com/biz/pearl-market-san-francisco'),
        (37.7791871,-122.4610244, 'Outdoors', 'https://sfrecpark.org/1000/Rossi-Playground-Picnic-Area'),
        (37.7791897,-122.4546622, 'Food', 'https://melsdrive-in.com/'),

    ]   
    walkable_marker_coordinates = [
        (37.776360, -122.449898, 'University of San Francisco'),
        (37.775145,-122.4539253, 'St. Mary Helath Clinic'),
        (37.7724895,-122.4565344, 'Police Department'),
        (37.775400, -122.449730, 'Transportation, Muni: 5'),
        (37.7820461,-122.4491252, 'City Center'),
        (37.7738489,-122.4526904, 'Haight-Ashbury'),
        (37.7703713,-122.4483282, 'Buena Vista Park'),
        (37.7690194,-122.4572928, 'Japan Town'),
        (37.7726187,-122.4602558, 'Golden Gate Park'),
        (37.7762203,-122.4557959, 'Velo Rouge Cafe'),
        (37.774591,-122.4649513, 'The Vogue Theater'),
        (37.7762726,-122.44138, 'The Mill'),
        (37.7807178,-122.4390234,'Pearl Market'),
        (37.7791871,-122.4610244, 'Rossi Park'),
        (37.7791897,-122.4546622, 'Mels Drive In'),
    ]   
    sf_coords = (37.776360, -122.449898)
  
    
    for coords in marker_coordinates:
        if coords[2] == 'University of San Francisco':
            create_marker(coords[:2], coords[2], coords[3], color='green').add_to(mapObj)
        else:
            create_marker(coords[:2], coords[2], coords[3]).add_to(mapObj)

    for i in range(len(walkable_marker_coordinates)):
        coords = walkable_marker_coordinates[i][:2]
        distance = calculate_distance(sf_coords, coords[:2])
        time_minutes = km_to_minutes(distance)

        folium.PolyLine(locations=[sf_coords, coords[:2]], color='blue', popup=f'Walking Time: {time_minutes:.2f} minutes').add_to(mapObj)

    mapObj.get_root().width = "1300px"
    mapObj.get_root().height = "650px"


    mapObj.save("san_francisco_map.html")

if __name__ == "__main__":
    display_map()
    
