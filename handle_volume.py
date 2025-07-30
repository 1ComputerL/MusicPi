# Copyright (c) 2025 ComputerL (@1ComputerL)
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

# This program connects to a Raspberry Pi Pico via serial port and receives volume control commands
# It then adjusts the system volume based on the received commands
# The pico sends these volume control commands based on the position of a potetentiometer connected to it
# The program could be edited to get volume control commands from other sources
# It is run by music_system.py
# Created by ComputerL

### IMPORTS ###
import sys
import os
import serial
import time
import json
import signal
import time
import signal
import logging

### PATH SETUP ###
# get the parent directory of this file
parentdir = os.path.dirname(os.path.abspath(__file__))
# add the MusicPi directory to the system path
sys.path.append(parentdir)

### LOGGING SETUP ###
# create new logger
log = logging.getLogger('my_logger')
# configure the logger
logging.basicConfig(filename=parentdir+'/musicpilog.log', level=logging.INFO, format='%(asctime)s - %(message)s')

### SIGNAL HANDLER ###
# handler function for stop signals
def handle_stop_signal(signum, frame):
# logging
    log.info("VolHandler: recieved stop signal, exiting now;")
# exit the program
    sys.exit(0)

# register the signal handler for SIGTERM
signal.signal(signal.SIGTERM, handle_stop_signal)
# register the signal handler for SIGTSTP
signal.signal(signal.SIGTSTP, handle_stop_signal)

log.info("VolHandler: VolHandler started; initiated things;;")

### CONNECT TO PICO ###
# fetch the serial port that the pico is connected to
with open(parentdir+'/settings.json', 'r') as file:
    data = json.load(file)

picoPort = data["picoPort"]

# open the serial port to connect to pico
ser = serial.Serial(picoPort, 115200, timeout=1)

# give pico some time to initialize
time.sleep(2)

log.info("VolHandler: connected to pico;")

### MAIN LOOP ###
while True:
### VOLUME CONTROL ###
# if receiving data from pico
    if ser.in_waiting > 0:
# read and decode the data
        data = ser.readline().decode('utf-8').strip()
        
# check if the data contains 'vol'
        if 'vol' in data:

            try:
# extract the volume value from the data
                volume_value = int(data.replace('vol:', '').strip())
                
# if the value is 1
                if volume_value == 1:
# mute the system volume
                    os.system("pactl set-sink-mute @DEFAULT_SINK@ 1")

# otherwise, if the value is between 2 and 50
                elif 1 < volume_value <= 50:
# make sure the system volume is unmuted
                    os.system("pactl set-sink-mute @DEFAULT_SINK@ 0")
# convert the value to a percentage
                    volume_percentage = volume_value * 2
# set the system volume to the value
                    os.system(f"pactl set-sink-volume @DEFAULT_SINK@ {volume_percentage}%")

# if the data given is not a number
                else:
                    print(f"Invalid volume value: {volume_value}")

# if error
            except ValueError:
                print(f"Error parsing volume value from data: {data}")

# if the data from pico is not a volume change command
        else:
            print(f"irregular data received: {data}")