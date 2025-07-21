"""
### -MICROPYTHON- ###

### IMPORTS ###
import machine
import utime

### POTENTIOMETERS ###
vol_potent = machine.ADC(26) # set pin as analog input
tone_potent = machine.ADC(27) # set pin as analog input

### VARIABLES ###
conv= 100 / (65535) # conversion factor variable contains the mathematical operation to perform on the potentiometer values

### ACTION ###
while True: # loop
    ### POTENTIOMETER STATE VARIABLES (0-100%) ###
    vol_potent_val = int(100 - vol_potent.value * conv) # get potentiometer state as percentage
    tone_potent_val = int(100 - tone_potent.value * conv) # get potentiometer state as percentage
    
    print("Volume:", vol_potent_val, "%", "\nTone", tone_potent_val, "%") # print the potentiometer states out nicely
    
    utime.sleep(.1) # delay
"""

### -CIRCUITPYTHON- ###

### IMPORTS ###
import time
import board
import analogio

### POTENTIOMETERS ###
vol_potent = analogio.AnalogIn(board.GP26) # set pin as analog input
tone_potent = analogio.AnalogIn(board.GP27) # set pin as analog input

### VARIABLES ###
conv = 100 / (65535) # conversion factor variable contains the mathematical operation to perform on the potentiometer values

### ACTION ###
while True: #loop
    ### POTENTIOMETER STATE VARIABLES (0-100%) ###
    vol_potent_val = int(100 - vol_potent.value * conv) # get potentiometer state as percentage
    tone_potent_val = int(100 - tone_potent.value * conv) # get potentiometer state as percentage
    
    print("Volume:", vol_potent_val, "%", "\nTone", tone_potent_val, "%") # print the potentiometer states out nicely    
    
    time.sleep(.1) # delay