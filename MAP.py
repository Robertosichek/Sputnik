import overpass
from geopy.geocoders import Nominatim
import osmnx as ox
import networkx as nx
import os
from selenium import webdriver
import time
geolocator = Nominatim(user_agent="OOOOOOO")
adress = input()
location = geolocator.geocode(adress)
api = overpass.API()
response_1 = api.Get(f'node["amenity"="doctors"](around:5000,{location.latitude}, {location.longitude});out;')['features']
response_2 = api.Get(f'node["amenity"="clinic"](around:5000,{location.latitude}, {location.longitude});out;')['features']
response_3 = api.Get(f'node["amenity"="hospital"](around:5000,{location.latitude}, {location.longitude});out;')['features']
clinic, doctors = [], []
for i in response_1:
    if 'name' in i["properties"]:
        a = i['geometry']['coordinates']
        doctors.append([a, i["properties"]['name']])
for i in response_2:
    if 'name' in i["properties"]:
        a = i['geometry']['coordinates']
        doctors.append([a, i["properties"]['name']])

for i in response_3:
    if 'name' in i["properties"]:
        a = i['geometry']['coordinates']
        doctors.append([a, i["properties"]["name"]])
for i in doctors:
    if i not in clinic:
        clinic.append(i)

print(clinic[0])
end_point = (clinic[0][0][1], clinic[0][0][0])
start_point = (location.latitude, location.longitude)
print(end_point, start_point)
G = ox.graph_from_point(start_point, dist=5000, network_type='walk')

orig_node = ox.nearest_nodes(G, start_point[1], start_point[0], False)

dest_node = ox.nearest_nodes(G, end_point[1], end_point[0], False)

route = nx.shortest_path(G,
                         orig_node,
                         dest_node,
                         weight='length')

shortest_route_map = ox.plot_route_folium(G, route,
                                          tiles='openstreetmap')
shortest_route_map.save('maaap.html')
mapFname = 'maaap.html'
mapUrl = 'file://{0}/{1}'.format(os.getcwd(), mapFname)
driver = webdriver.Firefox()
driver.get(mapUrl)
# wait for 5 seconds for the maps and other assets to be loaded in the browser
time.sleep(5)
driver.save_screenshot('output.png')
driver.quit()