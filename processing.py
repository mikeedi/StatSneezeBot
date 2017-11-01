"""
    -*- coding: utf-8 -*-
   Some function for processing data 
"""


import time
from hashlib import md5
import pickle
import os
import googlemaps

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


# use pickle instead database
def pickle_load(user_hash):
    filename = 'pickles/{}.pickle'.format(user_hash)
    with open(filename, 'rb') as f:
        obj = pickle.load(f)
    return obj

def pickle_dump(user_hash, last):
    filename = 'pickles/{}.pickle'.format(user_hash)
    if exist(filename):
        obj = pickle_load(filename)
        obj.append(last)
    else:
        obj = [last]
    with open(filename, 'wb') as f:
        pickle.dump(obj, f)
              
# get hash of user id 
def get_key(user_id):
    return md5(str(user_id).encode()).hexdigest()

def unix_to_local(t):
    return time.strftime("%D %H:%M", time.gmtime(int(t+10800))) # we use GMT + 3 time zone.

def get_last_location(coord):
    for c in coord[-1:]:
        if c[2] != 'None' and c[1] != 'None':
            return c[2], c[1]
        return 'None', 'None'