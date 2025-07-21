#This tutorial is provided by TomoDesign / https://www.instagram.com/tomo_designs/ 
import time
import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

kbd = Keyboard(usb_hid.devices)

# define buttons. these can be any physical switches/buttons, but the values
button = digitalio.DigitalInOut(board.GP5)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.DOWN

while True:
    # Push Keycode(The letter that you want to use Make sure that they are always Capital letters)
    if button.value:
        kbd.send(Keycode.C, Keycode.O, Keycode.O, Keycode.L,)

    time.sleep(0.1)