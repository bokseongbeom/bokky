import folium
import pandas as pd
import json
import numpy as np
import requests
import branca

m = folium.Map(
    location=[33.5097942063513,126.506073082089],
    tiles='Stamen Terrain',
    zoom_start=10,
)
tooltip = "click me!"

folium.Marker(
    [33.5097942063513,126.506073082089],
    popup="<b>떡볶이집</b>",
    tooltip=tooltip,
    icon=folium.Icon(color='red', icon='bookmark')
).add_to(m)

folium.Marker(
    [33.5097942063513,126.516073082089],
    popup="<b>떡볶이찝?</b>",
    tooltip=tooltip,
    icon=folium.Icon(color='blue', icon='flag')
).add_to(m)

m.save("map.html")