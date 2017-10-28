"""
    -*- coding: utf-8 -*-
    There's a description

"""



import telebot
from telebot import types
import googlemaps
import gmplot


from processing import *
import config


gmaps = googlemaps.Client(key=config.GGL_API_TOKEN)
bot = telebot.TeleBot(config.BOT_TOKEN)
bot.set_webhook()
location = {}




@bot.message_handler(commands=["help"])
def helpme(message):
    bot.send_message(message.chat.id, config.HELP_TEXT, parse_mode='HTML')     
    
    
@bot.message_handler(commands=["start"])
def start(message):
    if exist("{}.pickle".format(get_key(message.chat.id))):
        bot.send_message(message.chat.id, "You have already started")
    else:
        location[get_key(message.chat.id)] = [[0]]
        bot.send_message(message.chat.id, "Hi. I'm a bot that collect sneezes statistics")
        helpme(message)
        
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="SNEEZED!! !", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id, "Tap when sneezed", reply_markup=keyboard)
    
    

 
   
@bot.message_handler(content_types=['location'])
def locat(message):
    user_key = get_key(message.chat.id)
    if user_key not in location.keys():
        location[user_key] = pickle_load('{}.pickle'.format(user_key))[-10:]
    try:
        location[user_key].append([location[user_key][-1][0] + 1, message.location.longitude, \
                                                    message.location.latitude, message.date])
        bot.send_message(message.chat.id, "Bless you! It's your {} sneezes".format(str(location[user_key][-1][0])))        
        pickle_dump(user_key, location[get_key(message.chat.id)][-1])
        location[user_key] = pickle_load("{}.pickle".format(user_key))[-10:] 
        if location[user_key][-1][0] % 10 == 0 :
            bot.send_sticker(message.chat.id, config.PLANTAIN_STICK) #send podorojnik sticker
    except:
        bot.send_message(message.chat.id, 'Sorry, something went wrong')
        pass  
    
    
@bot.message_handler(commands=['sneeze'])
def sneeze(message):
    user_key = get_key(message.chat.id)
    if (get_key(message.chat.id) not in location.keys()):
        location[user_key] = pickle_load('{}.pickle'.format(user_key))[-10:]
    
    try:
        location[user_key].append([location[user_key][-1][0] + 1, 'None', 'None', message.date])
                                         # add sneeze count
        bot.send_message(message.chat.id, "Bless you! It's your {} sneezes".format(str(location[user_key][-1][0])))
        pickle_dump(user_key, location[get_key(message.chat.id)][-1])
        location[user_key] = pickle_load("{}.pickle".format(user_key))[-10:] 

        if location[user_key][-1][0] % 10 == 0 :
            bot.send_sticker(message.chat.id, config.PLANTAIN_STICK) #send podorojnik sticker
                         
    except:
        bot.send_message(message.chat.id, 'Sorry, something went wrong')

    
@bot.message_handler(commands=["getgeo"])
def getgeo(message):
    try:
        bot.send_message(message.chat.id, coord_to_md(pickle_load(get_key(message.chat.id)+'.pickle')[-5:], gmaps), parse_mode='HTML')

    except:
        bot.send_message(message.chat.id, 'Sorry, something went wrong')
        pass

@bot.message_handler(commands=["getall"])
def getgeo(message):
    try:
        bot.send_message(message.chat.id, coord_to_md(pickle_load(get_key(message.chat.id)+'.pickle'), gmaps), parse_mode='HTML')
    except:
        bot.send_message(message.chat.id, 'Sorry, something went wrong')
        pass
    

@bot.message_handler(commands=["getmap"])
def getlocation(message):
    coord = pickle_load(get_key(message.chat.id)+'.pickle')
    try:
        lat, lon = get_last_location(coord)
        if lat == 'None' or lon == 'None':
            raise TypeError
        gmap = gmplot.GoogleMapPlotter(lat, lon, 16, apikey=config.GGL_API_TOKEN)
        for c in coord:
            lat = c[2]
            lon = c[1]
            if lat == "None" or lon == "None":
                continue


            gmap.heatmap([lat], [lon])#, '#3B0B39', size=40, marker=False)
        gmap.draw("{}.html".format(get_key(message.chat.id)))
        with open("{}.html".format(get_key(message.chat.id)), 'rb') as f:
            bot.send_document(message.chat.id, f)
    except:
        bot.send_message(message.chat.id, 'You have no location')
        pass
    
    
    
    
bot.polling(none_stop=True)