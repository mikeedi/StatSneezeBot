"""
    -*- coding: utf-8 -*-
   Some function for processing data 
"""


import time
from hashlib import md5
import pickle
import os
import googlemaps
import config
import gmplot

#translation coordinate to street names and return html-like text
gmaps = googlemaps.Client(key=config.GGL_API_TOKEN)
def coord_to_md(coord_list, gmaps=gmaps):
    if coord_list[0][0] == 0:
        del coord_list[0]
        
        
    text = ''
    for coord in coord_list:
        street = 'None None'
        if coord[1] != 'None':
            street = gmaps.reverse_geocode((coord[2], coord[1]))[0]['formatted_address']
        text +="<b># {}</b> {} {} \n".format(coord[0], street, unix_to_local(coord[3]))
    return text

#check exist of file
def exist(path):
    try:
        os.stat(path)
    except OSError:
        return False
    return True  


# use pickle instead database (maybe it is bad way)
def pickle_load(user_hash, filename=None):
    if filename == None:
        filename = 'pickles/{}.pickle'.format(user_hash)
    with open(filename, 'rb') as f:
        obj = pickle.load(f)
    return obj

def pickle_dump(user_hash, last, filename=None):
    if filename == None:
        filename = 'pickles/{}.pickle'.format(user_hash)
    if exist(filename):
        obj = pickle_load(user_hash=None, filename=filename)
        obj.append(last)
    else:
        obj = [last]
    with open(filename, 'wb') as f:
        pickle.dump(obj, f)
              
# get hash of user id 
def get_key(user_id):
    return md5(str(user_id).encode()).hexdigest()

# translate of time
def unix_to_local(t):
    return time.strftime("%D %H:%M", time.gmtime(int(t+10800))) # we use GMT + 3 time zone.

def get_last_location(coord):
    for c in reversed(coord):
        if type(c[2]) == float  and type(c[1]) == float:
            return c[2], c[1]
    return 'None', 'None'

def map_render(user_hash):
    location = pickle_load(user_hash)
    lat, lon = get_last_location(location)
    if lat == 'None' or lon == 'None':
        return 'You have no location'

    else:
        gmap = gmplot.GoogleMapPlotter(lat, lon, 16, apikey=config.GGL_MAPS_TOKEN)
        gmap.coloricon = "http://www.googlemapsmarkers.com/v1/%s/"
        for c in location:
            lat = c[2]
            lon = c[1]
            if lat == "None" or lon == "None":
                continue
            gmap.marker(lat, lon, title=unix_to_local(c[-1]) + " UTC/GMT +3")
        gmap.draw("../templates/{}.html".format(user_hash))
        return "http://188.166.88.76/{}.html".format(user_hash)
