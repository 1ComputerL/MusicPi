### IMPORTS ###
import sys
import os
# get the parent directory of this file
parentdir = os.path.dirname(os.path.abspath(__file__))
# add the MusicPi directory to the system path
sys.path.append(parentdir)
import os
import subprocess
import traceback
import signal
import logging
import OLED as oled
import music_player
import evdevlib
import json
import time
from urllib.parse import urlparse
import tkinter as tk
import random

### SETUP SECTION 1 ###
# create new logger
log = logging.getLogger('my_logger')
# configure the logger
logging.basicConfig(filename=parentdir+'/musicpilog.log', level=logging.INFO, format='%(asctime)s - %(message)s')
log.info("got past logging setup")
# update the menus.json file
os.system("/bin/python " + parentdir + "/generate_albums_json.py")
# delay
time.sleep(.5)
log.info("got past updating menus.jsonn")
# set up the OLED display
OLED = oled.OLED()
log.info("got past OLED setup")
# set up the music player
player=music_player.Player()
log.info("got past music player setup")

### VARIABLES ###
# open menus.json file for reading
with open(parentdir + '/menus.json', 'r') as menus_json:
# load the json data into a variable
    menus = json.load(menus_json)
# current menu location
current_menu = menus["0"]
# read how many items are in the current menu
current_item_count = len(current_menu["items"])
# current selected menu item
current_item = 1
# set up a menu change event variable
menuChange=True
# set up a menu history array
menuHist=[current_menu]
# OLED off time variable
timeTillOledOff=5.00

# logging
log.info("MusicSys: Started; imports, setup1 (generate_albums_json.py, OLED on, log), variables;")

### FUNCTIONS ###
# function to handle stop signals
def handle_stop_signal(signum, frame):
# display powering off message on the OLED
    OLED.power("sys-off")
# delay
    time.sleep(2)
# terminate sysstem subprocesses
    volumeprogram.terminate()
    player.stop()
    OLED.clear()
# logging
    log.info("MusicSys: received stop signal; terminated subprocesses and now exiting;")
# exit the program
    sys.exit(0)

# function to handle key presses from pico
def press (key):
# define global variables
    global menus, current_menu, menuHist, current_item, current_item_count, menuChange
# sanitize the key input
    key=str(key)
# if the key pressed was not a function
    if "Key.f" not in key:
# do nothing
        pass

# if the key pressed is function 1 (backward)
    elif key == "Key.f1":
# if currently playing items
        if current_menu["title"] == "Playing Item":
# start playing previous item
            player.previous()

# reset the current playing song variable
            current="nothing"
# get the actual current playing song with a while loop
            while current == "nothing":
# get the current playing song
                current=player.get()
# delay
                time.sleep(.01)

# update the menu to show current song
            current_menu["items"]["0"]["title"] = current
# update the current item count
            current_item_count = len(current_menu["items"])
# update the current item
            current_item = 1
# update the display
            menuChange=True

# if the current highlight is not already at the top of the menu
        elif current_item != 1:
# move the highlight up one
            current_item -= 1
# update the display
            menuChange=True

# if the key pressed is function 2 (play/pause)
    elif key == "Key.f2":
# if currently playing items
        if current_menu["title"] == "Playing Item":
# toggle the player
            player.toggle()

# block to determine whether song has been paused or resumed
# if the state of the song was playing
            if current_menu["state"] == "playing":
# since the player was toggled, now the state should be paused
                current_menu["state"] = "paused"
# update the display
                menuChange=True
# else, the state of the song was paused

            else:
# and since the player was toggled, now the state should be playing
                current_menu["state"] = "playing"
# update the display
                menuChange=True

        else:
# set the current menu to the one clicked into
            current_menu = current_menu["items"][f"{current_item-1}"]
# update menu history
            menuHist.append(current_menu)
# check to see if there is an action in the current menu, which would be mpv
            if "action" in list(current_menu.keys()):
# reorganize the current menu to allow for song playing
                current_menu={
                    "title":"Playing Item",
                    "path":current_menu["action"]["path"],
                    "state":"playing",
                    "items":{
                        "0":{"title":current_menu["title"]}
                    }
                }
# start playing item
                player.play(current_menu["path"])
# reset the current playing song variable
                current="nothing"
# get the actual current playing song with a while loop
                while current == "nothing":
# get the current playing song
                    current=player.get()
# delay
                    time.sleep(.01)

# update the dict 
                current_menu["items"]["0"]["title"] = current
# update the current item count
                current_item_count = len(current_menu["items"])
# update the current item
                current_item = 1
# update the display
                menuChange=True
# update menu history
                #menuHist.pop()

            else:
# update the current item count
                current_item_count = len(current_menu["items"])
# update the current item
                current_item = 1
# update the display
                menuChange=True

# if the key pressed is function 4 (forward)
    elif key == "Key.f4":
# if currently playing itmes
        if current_menu["title"] == "Playing Item":
# start playing next item
                player.next()

# reset the current playing song variable
                current="nothing"
# get the actual current playing song with a while loop
                while current == "nothing":
# get the current playing song
                    current=player.get()
# delay
                    time.sleep(.01)


# update the menu to show current song
                current_menu["items"]["0"]["title"] = current
# update the current item count
                current_item_count = len(current_menu["items"])
# update the current item
                current_item = 1
# update the display
                menuChange=True

# if the current highlight is not already at the top of the menu
        elif current_item != current_item_count:
# move the highlight down one
            current_item += 1
# update the display
            menuChange=True

# if the key pressed is function 6 (play mode)
    elif key == "Key.f6":
# set the current menu to the main menu
        current_menu = menus["0"]
# update the current item count
        current_item_count = len(current_menu["items"])
# update the curent item
        current_item = 1
# update the display
        menuChange=True

# if the key pressed is function 7 (display / enter)
    elif key == "Key.f7":
# display powering off message on the OLED
        OLED.power("off")
# delay
        time.sleep(2)
# terminate sysstem subprocesses
        volumeprogram.terminate()
        player.stop()
        OLED.clear()
# logging
        log.info("MusicSys: received power-off button press; terminated subprocesses and now powering off the computer;")
# poweroff the whole system
        os.system("sudo poweroff")

# if the key pressed is function 8 (stop)
    elif key == "Key.f8":
# if currently playing items
        if current_menu["title"] == "Playing Item":
# stop the player
            player.stop()
# change the current menu to the menu displayed before the song was clicked on
            current_menu=menuHist[-1]

# if the current menu (which is still in history) isn't the main menu
            if len(menuHist) != 1:
# remove the current menu from history
                menuHist.pop()

# if currently in the main menu
        if current_menu["title"] == "Main Menu":
# do nothing
            pass
        
# else, just clicking through the menus
        else:
# set the current menu to the menu displayed previously
            current_menu=menuHist[-1]

# if the current menu (which is still in history) isn't the main menu
            if len(menuHist) != 1:
# remove the current menu from history
                menuHist.pop()

# update the current item count
            current_item_count = len(current_menu["items"])
# update the current item
            current_item = 1
# update the display
            menuChange=True
       
### SETUP SECTION 2 ###
# create listener to monitor all key presses
key_listener = evdevlib.Listener(on_press=press)
# start the listener
key_listener.start()
# register the signal handler for SIGTERM
signal.signal(signal.SIGTERM, handle_stop_signal)
# register the signal handler for SIGTSTP
signal.signal(signal.SIGTSTP, handle_stop_signal)
# start volume handling subprocess
volumeprogram = subprocess.Popen(
    ['/bin/python', parentdir+ '/handle_volume.py'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# logging
log.info("MusicSys: setup2; signal handlers, volume handling subprocess;")

### START OF MUSICPI SYSTEM ###
# display powering on message on the OLED
OLED.power("on")
# delay
time.sleep(2)

# logging
log.info("MusicSys: start of musicpi system; now starting loop;")

### MAIN LOOP ###
# loop variables
oledOffCounter=0
refreshPlayingCounter=0

# loop
while True:
# if the menu has changed
    if menuChange==True:
# reset the screen off counter
        oledOffCounter=0
# display the current menu
        OLED.menu(current_menu, current_item, current_item_count)
# reset the menu change variable
        menuChange=False

# if the oledOffCounter gets past 5 seconds
    if oledOffCounter > timeTillOledOff:
# reset the oledOffCounter
        oledOffCounter=0
# turn off the screen temporarily
        OLED.clear()
    
# if currently playing items
    if current_menu["title"] == "Playing Item":

# if the refreshPlayingCounter gets past 20 seconds
        if refreshPlayingCounter > 5:
# reset the current playing song variable
            current="nothing"
# reset the refreshPlayingCounter
            refreshPlayingCounter=0
# get the actual current playing song with a while loop
            while current == "nothing":
# get the current playing song
                current=player.get()
# delay
                time.sleep(.01)

# create a variable to hold the displayed current playing song
            song=current_menu["items"]["0"]["title"]

# if the current playing song is not the same as the one displayed
            if current != song:
# delay
                time.sleep(.5)
# update the playing dict (refresh playing song)
                current_menu["items"]["0"]["title"] = current
# update the current item count
                current_item_count = len(current_menu["items"])
# update the current item
                current_item = 1
# reset the screen off counter
                oledOffCounter=0
# update the display
                OLED.menu(current_menu, current_item, current_item_count)

# else, if refreshPlayingCounter is less than 20 seconds
        else:
# increment the refreshPlayingCounter
            refreshPlayingCounter+=.01

# increment the oledOffCounter
    oledOffCounter+=.01

# delay
    time.sleep(.01)