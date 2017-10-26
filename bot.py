"""
    There's a description

"""



import telebot
from telebot import types
import googlemaps



from processing import *
import config


gmaps = googlemaps.Client(key=config.GGL_API_TOKEN)
bot = telebot.TeleBot(config.BOT_TOKEN)

location = {}




@bot.message_handler(commands=["help"])
def helpme(message):
    bot.send_message(message.chat.id, config.HELP_TEXT, parse_mode='HTML')     
    
    
@bot.message_handler(commands=["start"])
def start(message):
    if get_key(message.chat.id) in location.keys():
        bot.send_message(message.chat.id, "You have already started")
    else:
        location[get_key(message.chat.id)] = [[0]]
        bot.send_message(message.chat.id, "Hi. I'm a bot that collect sneezes statistics")
        helpme(message)
        
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="SNEEZED!! !", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id, "Tap when sneezed", reply_markup=keyboard)
    
    
@bot.message_handler(commands=["reset"])
def reset(message):
    bot.send_message(message.chat.id, "Your sneezes history is empty")
    location[get_key(message.chat.id)] = [[0]]
 
   
@bot.message_handler(content_types=['location'])
def locat(message):
    if (get_key(message.chat.id) not in location.keys()):
        location[get_key(message.chat.id)] = pickle_load(get_key(message.chat.id)+'.pickle')[-10:]
    try:
        user_key = get_key(message.chat.id)
        location[get_key(message.chat.id)].append([location[user_key][-1][0] + 1, message.location.longitude, \
                                                    message.location.latitude, message.date])
        bot.send_message(message.chat.id, "Bless you! It's your {} sneezes".format(str(location[user_key][-1][0])))
        if location[user_key][-1][0] % 10 == 0 :
            bot.send_sticker(message.chat.id, config.PLANTAIN_STICK) #send podorojnik sticker
        pickle_dump(user_key, location)
        location[user_key] = location[user_key][-10:] 
    except:
        bot.send_message(message.chat.id, 'Try /start')
        pass  
    
    
@bot.message_handler(commands=['sneeze'])
def sneeze(message):
    if (get_key(message.chat.id) not in location.keys()):
        location[get_key(message.chat.id)] = pickle_load(get_key(message.chat.id)+'.pickle')[-10:]
    
    try:
        user_key = get_key(message.chat.id)
        location[user_key].append([location[user_key][-1][0] + 1, 'None', 'None', message.date])
                                         # add sneeze count
        bot.send_message(message.chat.id, "Bless you! It's your {} sneezes".format(str(location[user_key][-1][0])))
        if location[user_key][-1][0] % 10 == 0 :
            bot.send_sticker(message.chat.id, config.PLANTAIN_STICK) #send podorojnik sticker
        pickle_dump(user_key, location)
        location[user_key] = location[user_key][-10:]               
    except:
        bot.send_message(message.chat.id, 'Try /start')

    
@bot.message_handler(commands=["getgeo"])
def getgeo(message):
    if (get_key(message.chat.id) not in location.keys()):
        location[get_key(message.chat.id)] = pickle_load(get_key(message.chat.id)+'.pickle')[-10:]
    try:
        bot.send_message(message.chat.id, coord_to_md(location[get_key(message.chat.id)][-5:], gmaps), parse_mode='HTML')

    except:
        pass

    
# @bot.message_handler(commands=["getlocation"])
# def getlocation(message):
#     if (get_key(message.chat.id) not in location.keys()):
#         location[get_key(message.chat.id)] = pickle_load(get_key(message.chat.id)+'.pickle')[-10:]
#     try:
#         if location[get_key(message.chat.id)][-1][2] != 'None':
#             bot.send_location(message.chat.id, location[get_key(message.chat.id)][-1][2], \
#                                         location[get_key(message.chat.id)][-1][1])
#         else:
#             bot.send_message(message.chat.id, 'Your last sneeze have no location')

#     except:
#         bot.send_message(message.chat.id, 'Your last sneeze have no location')
#         pass
    
    
    
    
bot.polling(none_stop=True)