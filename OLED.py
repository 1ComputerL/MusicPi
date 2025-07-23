### IMPORTS ###
import time
import os
import sys
from PIL import Image, ImageDraw, ImageFont
import logging

# get the parent directory of this file
parentdir = os.path.dirname(os.path.abspath(__file__))
# path variables
picdir = parentdir + "/OLED/pic"
libdir = parentdir + "/OLED/lib"

# add OLED library path to system path so that we can import it
sys.path.append(libdir)

# import the OLED library
from waveshare_OLED import OLED_0in91

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
        self.disp = OLED_0in91.OLED_0in91()
        self.disp.Init()
# set font path and load default fonts
        self.font_path = picdir + '/Font.ttc'
        self.fontItem = ImageFont.truetype(self.font_path, 14)
        self.fontTitle = ImageFont.truetype(self.font_path, 10)
        self.fontNotif = ImageFont.truetype(self.font_path, 14)
# logging
        log.info("OLED: initialized;")

# function to fit the text into max_width by reducing font size
# returns the largest font that fits
    def fit_text(self, text, max_width, max_size=14, min_size=8):
# loop from max_size down to min_size
        for font_size in range(max_size, min_size - 1, -1):
# create a font object with the current size
            font = ImageFont.truetype(self.font_path, font_size)
# measure the width of the text with this font
            width, _ = ImageDraw.Draw(Image.new('1', (1, 1))).textsize(text, font=font)
# if the text fits, return this font
            if width <= max_width:
                return font
# if no font fits, return the smallest font
        return ImageFont.truetype(self.font_path, min_size)

# function to fallback to squeezing font only if text is too long
# preserves default font unless squeezing is needed
# icon_width parameter added to compensate for symbols like '•', '▶', or '||'
    def squeeze_text_if_needed(self, draw, text, default_font, max_width, max_size=14, min_size=8, icon_width=0):
# adjust available width by subtracting space taken by icons
        adjusted_width = max_width - icon_width
# measure the width using the default font
        width, _ = draw.textsize(text, font=default_font)
# if it fits, use default
        if width <= adjusted_width:
            return default_font, width
# if it doesn't fit, find a smaller font
        else:
            font = self.fit_text(text, adjusted_width, max_size, min_size)
            new_width, _ = draw.textsize(text, font=font)
            return font, new_width

# function to display a notification with a title and message
# title is usually at the top, message below
    def notification(self, title, notification):
# clear the display
        self.disp.clear()
# create new image
        img = Image.new('1', (self.disp.width, self.disp.height), "WHITE")
# create new draw object
        draw = ImageDraw.Draw(img)
# adjust title font only if needed
        font_title, widthTitle = self.squeeze_text_if_needed(draw, title, self.fontTitle, self.disp.width)
# adjust notification font only if needed
        font_notif, widthNotif = self.squeeze_text_if_needed(draw, notification, self.fontNotif, self.disp.width)
# center title text
        xTitle = (self.disp.width - widthTitle) // 2
# center notification text
        xNotif = (self.disp.width - widthNotif) // 2
# draw the title and notification
        draw.text((xTitle, 0), title, font=font_title, fill=0)
        draw.text((xNotif, 16), notification, font=font_notif, fill=0)
# make sure image is rotated correctly
        img = img.rotate(0)
# show the image 
        self.disp.ShowImage(self.disp.getbuffer(img))
# logging
        log.info("OLED: displayed notification;")

# function to display menu with title and selected item
    def menu(self, menu, current_item, item_count):
# clear the display
        self.disp.clear()
# create new image
        img = Image.new('1', (self.disp.width, self.disp.height), "WHITE")
# create new draw object
        draw = ImageDraw.Draw(img)
# get title of the menu
        title = menu["title"]
# get the menu item at current selection
        item = menu["items"][f"{current_item-1}"]["title"]
# estimated width of the play/pause/dot icon in pixels
        icon_width = 12
# adjust fonts if text is too wide (compensate for icon width on item)
        font_title, widthTitle = self.squeeze_text_if_needed(draw, title, self.fontTitle, self.disp.width)
        font_item, widthItem = self.squeeze_text_if_needed(draw, item, self.fontItem, self.disp.width, icon_width=icon_width)
# calculate x positions to center text
        xTitle = (self.disp.width - widthTitle) // 2
        xItem = (self.disp.width - widthItem) // 2
# display the title at the top
        draw.text((xTitle, 0), title, font=font_title, fill=0)
# if playing song
        if "state" in menu:
# if the song is currently playing
            if menu["state"] == "playing":
# display a pause symbol
                draw.text((0, 16), '||', font=self.fontItem, fill=0)
            else:
# display a play symbol with adjusted font
                play_font = self.fit_text('▶', 16, max_size=24)
                draw.text((0, 16), '▶', font=play_font, fill=0)
        else:
# display a regular dot to mark position
            draw.text((0, 16), '•', font=self.fontItem, fill=0)
# display the current menu item
        draw.text((xItem, 16), item, font=font_item, fill=0)
# rotate and show image
        img = img.rotate(0)
        self.disp.ShowImage(self.disp.getbuffer(img))
# logging
        log.info("OLED: displayed menu;")

# display impending power status
    def power(self, state):
# if power state is on
        if state == "on":
# change text to indicate that
            state = "Welcome"
# if power state is off
        elif state == "off":
# change text to indicate that
            state = "powering off"
# if power state is reboot
        elif state == "reboot":
# change text to indicate that
            state = "rebooting"
# if system program is off
        elif state == "sys-off":
# change text to indicate that
            state = "system prog off"
# fallback for unexpected state values
        else:
            pass
# display power status using notification method
        self.notification("MusicPi", state)
# logging
        log.info(f"OLED: displayed power state: {state};")

# function to clear the display
    def clear(self):
# clear the display
        self.disp.clear()
# logging
        log.info("OLED: cleared display;")
