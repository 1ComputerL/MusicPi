# intended for use with Raspberry Pi Pico
### IMPORTS ###
import time
import board
import digitalio
import analogio
import rotaryio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

### POTENTIOMETERS ###
vol_potent = analogio.AnalogIn(board.GP26) # set pin as analog input
tone_potent = analogio.AnalogIn(board.GP27) # set pin as analog input

### BUTTONS ###
bbackward = digitalio.DigitalInOut(board.GP0) # assign gpio pin
bbackward.direction = digitalio.Direction.INPUT # set as input
bbackward.pull = digitalio.Pull.DOWN # set to use resistor

bplay = digitalio.DigitalInOut(board.GP1) # assign gpio pin
bplay.direction = digitalio.Direction.INPUT # set as input
bplay.pull = digitalio.Pull.DOWN # set to use resistor

bforward = digitalio.DigitalInOut(board.GP2) # assign gpio pin
bforward.direction = digitalio.Direction.INPUT # set as input
bforward.pull = digitalio.Pull.DOWN # set to use resistor

bmode = digitalio.DigitalInOut(board.GP3) # assign gpio pin
bmode.direction = digitalio.Direction.INPUT # set as input
bmode.pull = digitalio.Pull.DOWN # set to use resistor

bdisplay = digitalio.DigitalInOut(board.GP4) # assign gpio pin
bdisplay.direction = digitalio.Direction.INPUT # set as input
bdisplay.pull = digitalio.Pull.DOWN # set to use resistor

bstop = digitalio.DigitalInOut(board.GP5) # assign gpio pin
bstop.direction = digitalio.Direction.INPUT # set as input
bstop.pull = digitalio.Pull.DOWN # set to use resistor

bpower = digitalio.DigitalInOut(board.GP6) # assign gpio pin
bpower.direction = digitalio.Direction.INPUT # set as input
bpower.pull = digitalio.Pull.DOWN # set to use resistor

bcd = digitalio.DigitalInOut(board.GP7) # assign gpio pin
bcd.direction = digitalio.Direction.INPUT # set as input
bcd.pull = digitalio.Pull.DOWN # set to use resistor

### DEVICE ###
device_control_consumer = ConsumerControl(usb_hid.devices)
device_control_keyboard = Keyboard(usb_hid.devices)

### VARIABLES ###
dl = 0.2 # delay variable
conv = 100 / (65535) # conversion factor variable contains the mathematical operation to perform on the potentiometer values

cd_state_previous = False # state of cd thing, True is closed, False is open
power_state_previous = False # state of power button, True is pressed, False is depressed
cd_newon = True
power_newon = True
vol_potent_val_previous =  0
tone_potent_val_previous = 0

### ACTION ###
while True: # loop
### POTENTIOMETER STATE VARIABLES (0-100%) ###
    vol_potent_val_ = int(str(100 - vol_potent.value * conv).split(".")[0]) # get potentiometer state
    tone_potent_val = int(str(100 - tone_potent.value * conv).split(".")[0]) # get potentiometer state
    
    vol_potent_val = round(((vol_potent_val_ - 1) / (100 - 1)) * (50 - 1) + 1) # format volume to send
    
### EVALUATE POTENTIOMETER POSITIONS AND ADJUST VOLUME ACCORDINGLY ###
    if vol_potent_val != vol_potent_val_previous: # if volume potentiometer was turned
        print("vol:"+str(vol_potent_val))
        
        vol_potent_val_previous = vol_potent_val # set the previous variable to the current state of active variable
    
    if tone_potent_val != tone_potent_val_previous: # if tone potentiometer was turned
        print("tone")
        
        tone_potent_val_previous = tone_potent_val # set the previous variable to the current state of active variable

### CHECK BUTTON STATES, RESPOND TO PRESSES BY SENDING KEYPRESS SIGNALS TO DEVICE ###
    if bbackward.value: # check for button press
        
        device_control_keyboard.send(Keycode.F1) # send keypad code to device
        time.sleep(dl) # button press delay
        
    if bplay.value: # check for button press
        
        device_control_keyboard.send(Keycode.F2) # send keypad code to device
        time.sleep(dl) # button press delay
        
    if bforward.value: # check for button press
        
        device_control_keyboard.send(Keycode.F4) # send keypad code to device
        time.sleep(dl) # button press delay
        
    if bmode.value: # check for button press
        
        device_control_keyboard.send(Keycode.F6) # send keypad code to device
        time.sleep(dl) # button press delay
        
    if bdisplay.value: # check for button press
        
        device_control_keyboard.send(Keycode.F7) # send keypad code to device
        time.sleep(dl) # button press delay
        
    if bstop.value: # check for button press
        
        device_control_keyboard.send(Keycode.F8) # send keypad code to device
        time.sleep(dl) # button press delay
    
    if bpower.value != power_state_previous: # check for change in button state compared to last check
        if power_newon == True and bpower.value == False: # check if the system was just turned on if button is off avoid sending signal to pi to avoid confusion
            power_newon = False
            continue
        
        else:
            device_control_keyboard.send(Keycode.F9)
            
        power_state_previous = bpower.value # set the previous variable to the current state of active variable
        time.sleep(dl) # button press delay
        
    if bcd.value != cd_state_previous: # check for change in button state compared to last check
            device_control_keyboard.send(Keycode.F12)
            
        cd_state_previous = bcd.value # set the previous variable to the current state of active variable
        time.sleep(dl) # button press delay
        
    time.sleep(0.1) # delay
