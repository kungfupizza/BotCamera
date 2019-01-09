import datetime  # Importing the datetime library
import telepot   # Importing the telepot library
from telepot.loop import MessageLoop    # Library function to communicate with telegram bot
from time import sleep      # Importing the time library to provide the delays in program
import picamera
import time
import os
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

markup = ReplyKeyboardMarkup(keyboard=[
                     ['Hi', KeyboardButton(text='How you doin?')],
                     [dict(text='Picture Time'), KeyboardButton(text='Live feed')],
                     [dict(text='Upcoming feature1'), KeyboardButton(text='Upcoming feature2')]
                        ])

video_reply = ReplyKeyboardMarkup(keyboard=[
                     ['5', KeyboardButton(text='10')],
                     [dict(text='15'), KeyboardButton(text='Back')],
                        ])

p_res={1024,768}        #Photo resolution
v_res={640,480}         #Video resolution
p_name= "click"         #Name for photo file
v_name= "video"         #Name for video file

#get your own token from Telegram, it's easy
telegram_key='Enter your Telegram Token'


def handle(msg):
    chat_id = msg['chat']['id'] # Extract chat_id from the message
    command = msg['text']   # Extract command from the message
    name= msg['from']['first_name'] #get the first name
    print ('Received:')
    print(command)

    # Comparing the incoming message to send a reply according to it
    if command== '/start':
 	bot.sendMessage(chat_id, 'Hurray! You are here!', reply_markup=markup)
    elif command == 'hi' or command== 'Hi':
        bot.sendMessage (chat_id, str("Hi! "+name), reply_markup=markup)
    elif command == 'Picture Time':
        bot.sendMessage(chat_id, str("One moment please"))
        camera= picamera.PiCamera()
        camera.resolution= (p_res)
        camera.start_preview()
        time.sleep(3)
        camera.capture(p_name+'.jpg')
        camera.close()
        bot.sendPhoto(chat_id, photo=open((p_name+'.jpg'), 'rb'), caption='Click click', reply_markup=markup)
        os.system("rm "+ p_name + ".jpg") #remove the picture file, save memory
    elif command== 'How you doin?':
        bot.sendMessage(chat_id, str("I am alive. Test me."), reply_markup=markup)
    elif command== 'Live feed':
        bot.sendMessage(chat_id, str("How many seconds of video?"), reply_markup=video_reply)
    elif command== '5' or command== '10' or command== '15':
        bot.sendMessage(chat_id, str("Getting back at you in " + str(int(command)+3) + " seconds"), reply_markup=markup)
        camera=picamera.PiCamera()
	camera.resolution = (v_res)
        camera.framerate=30
        camera.start_recording(v_name + '.h264')
        camera.wait_recording(int(command))
        camera.stop_recording()
        camera.close()
        os.system("MP4Box  -fps 30  -add " + v_name + ".h264 " + v_name + ".mp4")       #Telegram does not take h264 videos, convert it to mp4 using this
        bot.sendVideo(chat_id, video=open(v_name + '.mp4', 'rb'), caption='I took this', reply_markup=markup)
        os.system("rm " + v_name + ".*")        #delete the picture, save memory
    elif command== 'Back':
        bot.sendMessage(chat_id, str("Back to Main Menu"), reply_markup=markup)
    elif command== 'Upcoming feature1' or command== 'Upcoming feature2':        #I will add the new features asap
        bot.sendMessage(chat_id, str("We'll get new things working soon. Thank you for waiting"), reply_markup=markup)
    else :
        bot.sendMessage(chat_id, str("I didn't understand. Is the command from Mars? \xF0\x9F\x98\x89"), reply_markup=markup)

# Insert your telegram token below
bot = telepot.Bot(telegram_key)
print (bot.getMe())

# Start listening to the telegram bot and whenever a message is  received, the handle function will be called.
MessageLoop(bot, handle).run_as_thread()
print ('Waiting for message...')

while 1:
    sleep(10)