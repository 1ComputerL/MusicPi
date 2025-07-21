"""
### -MICROPYTHON- ###

### IMPORTS ###
import machine
import utime

### BUTTONS ###
bbackward = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_DOWN) # set pin as input using a resistor
bplay = machine.Pin(1, machine.Pin.IN, machine.Pin.PULL_DOWN) # set pin as input using a resistor
bforward = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_DOWN) # set pin as input using a resistor
bmode = machine.Pin(3, machine.Pin.IN, machine.Pin.PULL_DOWN) # set pin as input using a resistor
bdisplay = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_DOWN) # set pin as input using a resistor
bstop = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_DOWN) # set pin as input using a resistor
bpower = machine.Pin(6, machine.Pin.IN, machine.Pin.PULL_DOWN) # set pin as input using a resistor
bcd = machine.Pin(7, machine.Pin.IN, machine.Pin.PULL_DOWN) # set pin as input using a resistor

### ACTION ###
while True: # loop
    ### CHECK AND DISPLAY BUTTON STATES ###
    if bbackward.value: # check for button press
        print("backward") # print the name of the button pressed
        
    if bplay.value: # check for button press
        print("play") # print the name of the button pressed
        
    if bforward.value: # check for button press
        print("forward") # print the name of the button pressed
        
    if bmode.value: # check for button press
        print("mode") # print the name of the button pressed
        
    if bdisplay.value: # check for button press
        print("display") # print the name of the button pressed
        
    if bstop.value: # check for button press
        print("stop") # print the name of the button pressed
        
    if bpower.value: # check for button press
        print("power") # print the name of the button pressed
        
    if bcd.value: # check for button press
        print("bcd") # print the name of the button pressed
        
    utime.sleep(0.1) # loop delay
"""

### -CIRCUITPYTHON- ###

### IMPORTS ###
import time
import board
import digitalio

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

### VARIABLES ###
dl = 0.2 # button delay

""" ACTION """

while True: # loop
    ### DISPLAY BUTTON STATES ###
    if bbackward.value: # check for button press
        print("backward") # print the name of the button pressed
        
    if bplay.value: # check for button press
        print("play") # print the name of the button pressed
        
    if bforward.value: # check for button press
        print("forward") # print the name of the button pressed
        
    if bmode.value: # check for button press
        print("mode") # print the name of the button pressed
        
    if bdisplay.value: # check for button press
        print("display") # print the name of the button pressed
        
    if bstop.value: # check for button press
        print("stop") # print the name of the button pressed
        
    if bpower.value: # check for button press
        print("power") # print the name of the button pressed
        
    if bcd.value: # check for button press
        print("bcd") # print the name of the button pressed
        
    time.sleep(0.1) # loop delay