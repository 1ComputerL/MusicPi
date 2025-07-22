### IMPORTS ###
import time
import sys
from PIL import Image,ImageDraw,ImageFont
import logging
# path variables
picdir = "/home/me/System/OLED/pic"
libdir = "/home/me/System/OLED/lib"
# add OLED libary path to system path so that we can import it
sys.path.append(libdir)
# import the OLED library
from waveshare_OLED import OLED_0in91

### VARIABLES ###
# set up the OLED display
disp = OLED_0in91.OLED_0in91()
# font variables
fontItem = ImageFont.truetype(picdir + '/Font.ttc', 14)
fontTitle = ImageFont.truetype(picdir +'/Font.ttc', 10)
fontNotif = ImageFont.truetype(picdir +'/Font.ttc', 14)

### LOGGING SETUP ###
# create new logger
log = logging.getLogger('my_logger')
# configure the logger
logging.basicConfig(filename='musicpilog.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# OLED class
class OLED:
# constructor
    def __init__(self):
# initialize the display
        disp.Init()
# logging
        log.info("OLED: initialized;")

# function to find the largest font size that fits the text within the display width
    def fit_text(self, text, max_width, font_path, max_size, min_size=8):
# loop from max_size down to min_size
        for font_size in range(max_size, min_size - 1, -1):
# create a font object with the current size
            font = ImageFont.truetype(font_path, font_size)
# measure the width of the text with this font
            width, _ = ImageDraw.Draw(Image.new('1', (1, 1))).textsize(text, font=font)
# if the text fits, return this font
            if width <= max_width:
                return font
# if no font fits, return the smallest font
        return ImageFont.truetype(font_path, min_size)
    
    def notification (self, title, notification):
# clear the display
        disp.clear()
# create new image
        img = Image.new('1', (disp.width, disp.height), "WHITE")
# create new draw object
        imgdraw = ImageDraw.Draw(img)
# calculate the width of the title
        widthTitle, heightTitle = imgdraw.textsize(title, font=fontTitle)
# calculate the width of the state text
        widthNotif, heightNotif = imgdraw.textsize(notification, font=fontNotif)
# calculate the x position to center the title
        xTitle= (disp.width - widthTitle) // 2
# calculate the x position to center the notification text
        xNotif= (disp.width - widthNotif) // 2        
# display the title
        imgdraw.text((xTitle,0), f'{title}', font = fontTitle, fill = 0)
# display the notification
        imgdraw.text((xNotif, 16), f'{notification}', font = fontNotif, fill = 0)
# make sure image is rotated correctly
        img=img.rotate(0)
# show the image 
        disp.ShowImage(disp.getbuffer(img))
# logging
        log.info("OLED: displayed notification;")

# function to display menus
    def menu (self, menu, current_item, item_count):
# clear the display
        disp.clear()
# create new image
        img = Image.new('1', (disp.width, disp.height), "WHITE")
# create new draw object
        imgdraw = ImageDraw.Draw(img)
# define the title to display
        title = menu["title"]
# get the menu item
        item= menu["items"][f"{current_item-1}"]["title"]
# calculate the width of the title
        widthTitle, heightTitle = imgdraw.textsize(title, font=fontTitle)
# calculate the width of the item text
        widthItem, heightItem = imgdraw.textsize(item, font=fontItem)
# calculate the x position to center the text
        xTitle= (disp.width - widthTitle) // 2
# calculate the x position to center the text
        xItem= (disp.width - widthItem) // 2
# display the title
        imgdraw.text((xTitle,0), f'{title}', font = fontTitle, fill = 0)
# if playing song
        if "state" in list(menu.keys()):
# if the song is currently playing
            if menu["state"] == "playing":
# display a pause symbol
                imgdraw.text((0,16), '||', font = fontItem, fill = 0)
            else:
# display a play symbol
                imgdraw.text((0,16), '▶', font = ImageFont.truetype(picdir +'/Font.ttc', 24), fill = 0)
        else:
# display the regular dot at the side
            imgdraw.text((0,16), '•', font = fontItem, fill = 0)
# display the menu item
        imgdraw.text((xItem,16), f'{item}', font = fontItem, fill = 0)
# make sure image is rotated correctly
        img=img.rotate(0)
# show the image 
        disp.ShowImage(disp.getbuffer(img))
# logging
        log.info("OLED: displayed menu;")

# display impending power status
    def power (self, state):
# if power state is on
        if state == "on":
# change text to indicate that
            state="Welcome"
# if power state is off
        elif state == "off":
# change text to indicate that
            state="powering off"
# if power state is reboot
        elif state == "reboot":
# change text to indicate that
            state="rebooting"
        elif state == "sys-off":
# change text to indicate that
            state="system prog off"
# if a different value was given
        else:
# pass for now
            pass

        self.notification("MusicPi", state)
# logging
        log.info(f"OLED: displayed power state: {state};")

# function to clear the display
    def clear (self):
# clear the display
        disp.clear()
# logging
        log.info("OLED: cleared display;")

"""
Himage2 = Image.new('1', (disp.width, disp.height), 255)
bmp = Image.open(picdir+'/0in91.bmp'))
Himage2.paste(bmp, (0,0))
"""

"""
# loop through the menu items and display them
        for i in range(item_count):
# get the menu item posistion
                y = 12 + (i * 12)
# get the menu item
                item=menu["items"][f"{i}"]["title"]
# calculate the width of the item text
                itemWidth, itemHeight = imgdraw.textsize(item, font=fontItem)
# calculate the x position to center the text
                xItem= (disp.width - itemWidth) // 2
# display the menu item
                imgdraw.text((xItem,y), f'{item}', font = fontItem, fill = 0)
"""