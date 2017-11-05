# StatSneezeBot
Would you like to collect, perhaps, useless statistics about something? [@StatSneezeBot](https://t.me/statsneezebot) can help in this.
![](gif/chat.gif)
## What is used
- [pytelegrambotapi](https://github.com/eternnoir/pyTelegramBotAPI)
- [flask](http://flask.pocoo.org/)
- [googlemaps](https://github.com/googlemaps/google-maps-services-python)
- [Botan (Yandex metric)](https://github.com/MasterGroosha/telegram-tutorial/blob/master/lesson_06/botan.py)
## Simple function
- /help
``` Python
@bot.message_handler(commands=["help"])
def helpme(message):
    bot.send_message(message.chat.id, config.HELP_TEXT, parse_mode='HTML')  # Help text is contained in config.py
```
- /start
``` Python
@bot.message_handler(commands=["start"])
def start(message):
    if exist("pickles/{}.pickle".format(get_key(message.chat.id))):   # use piclkes file instead database
        bot.send_message(message.chat.id, "You have already started")
    else:
        location[get_key(message.chat.id)] = [[0]] # initialize 
        bot.send_message(message.chat.id, "Hi. I'm a bot that collect sneezes statistics")
        helpme(message)  # send command description

    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)  # button class
    button_geo = types.KeyboardButton(text="SNEEZED!! !", request_location=True) # button
    keyboard.add(button_geo) # create button
    bot.send_message(message.chat.id, "Tap when sneezed", reply_markup=keyboard) # add button
```
- /sneeze
``` Python
@bot.message_handler(commands=['sneeze'])
def sneeze(message): 
    user_key = get_key(message.chat.id)  # get_key return hash string from user id
    if (get_key(message.chat.id) not in location.keys()):  # load last 5 location
        location[user_key] = pickle_load(user_key)[-5:]   # it is need if program will failed
    location[user_key].append([location[user_key][-1][0] + 1, 'None', 'None', message.date])
                                     # add sneeze count
    bot.send_message(message.chat.id, "Bless you! It's your {} sneezes".format(str(location[user_key][-1][0])))
    pickle_dump(user_key, location[get_key(message.chat.id)][-1]) # after recording rewrite to pickles
    location[user_key] = pickle_load(user_key)[-5:] 
    if location[user_key][-1][0] % 10 == 0 : 
        bot.send_sticker(message.chat.id, config.PLANTAIN_STICK) #send podorojnik sticker
```
- /location
``` Python
@bot.message_handler(content_types=['location'])
def locat(message):
    ...
    location[user_key].append([location[user_key][-1][0] + 1, message.location.longitude, \
                                                message.location.latitude, message.date])  # add sneeze count
    ...
```
- /getgeo
``` Python
# get last 5 sneezes location
@bot.message_handler(commands=["getgeo"])
def getgeo(message):
    bot.send_message(message.chat.id, coord_to_md(pickle_load(get_key(message.chat.id))[-5:]), parse_mode='HTML') # coord md return html-like text with location
```

- /getall
``` Python
# get all data
@bot.message_handler(commands=["getall"])
def getall(message):
    bot.send_message(message.chat.id, coord_to_md(pickle_load(get_key(message.chat.id))), parse_mode='HTML')
``` 
## What's next?
* Visualizing location for user
* Heatmap (sneezes-warning places)
